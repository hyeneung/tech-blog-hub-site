package service

import (
	"context"
	"encoding/json"
	"log"
	"os"
	"searchAPI/internal/model"
	"searchAPI/internal/utils"
	"strconv"
	"strings"
	"time"

	"github.com/aws/aws-xray-sdk-go/xray"
	"github.com/go-redis/redis/v8"
	"github.com/opensearch-project/opensearch-go"
	"github.com/opensearch-project/opensearch-go/opensearchapi"
)

func PerformSearch(ctx context.Context, openSearchClient *opensearch.Client, redisClient *redis.Client, params utils.SearchParams) model.Content {
	var content model.Content
	cacheKey := generateCacheKey(params)

	// Read from cache
	xray.Capture(ctx, "CacheRead", func(ctx context.Context) error {
		cachedResult, err := redisClient.Get(ctx, cacheKey).Result()
		if err == nil {
			if err := json.Unmarshal([]byte(cachedResult), &content); err == nil {
				return nil
			}
		}
		return err
	})

	// If data is not found in cache, execute DB query
	if content.ArticleInfos == nil {
		xray.Capture(ctx, "DBQuery", func(ctx context.Context) error {
			articleInfos, totalElements := queyOpenSearch(ctx, openSearchClient, params)
			content = model.Content{
				ArticleInfos: articleInfos,
				Pageable: model.Pageable{
					PageNumber:    params.Page,
					PageSize:      params.Size,
					TotalElements: totalElements,
					TotalPages:    (totalElements + params.Size - 1) / params.Size,
				},
			}
			return nil
		})

		// Write to cache
		xray.Capture(ctx, "CacheWrite", func(ctx context.Context) error {
			cacheData, _ := json.Marshal(content)
			expirationTime := calculateCacheExpiration()

			err := redisClient.Set(ctx, cacheKey, cacheData, 0).Err()
			if err != nil {
				return err
			}

			return redisClient.ExpireAt(ctx, cacheKey, expirationTime).Err()
		})
	}

	return content
}

func generateCacheKey(params utils.SearchParams) string {
	return strings.Join([]string{
		strings.Join(params.Hashtags, ","),
		params.Company,
		params.Query,
		strconv.Itoa(params.Page),
		strconv.Itoa(params.Size),
	}, ":")
}

// calculateCacheExpiration determines the expiration time for cache entries
// It returns 19:00 KST of the current day if the current time is before 19:00,
// or 19:00 KST of the next day if the current time is after 19:00
// This timing is aligned with the daily crawler execution at 19:00 KST,
// ensuring that cached data remains valid until the next crawler run.
func calculateCacheExpiration() time.Time {
	koreaLocation, _ := time.LoadLocation("Asia/Seoul")
	now := time.Now().In(koreaLocation)
	expirationTime := time.Date(now.Year(), now.Month(), now.Day(), 19, 0, 0, 0, koreaLocation)

	if now.Hour() >= 19 {
		expirationTime = expirationTime.Add(24 * time.Hour)
	}

	return expirationTime
}

func queyOpenSearch(ctx context.Context, client *opensearch.Client, params utils.SearchParams) ([]model.ArticleInfo, int) {
	indexName := os.Getenv("OPENSEARCH_INDEX_NAME")

	searchBody := buildSearchQuery(params)

	body, err := json.Marshal(searchBody)
	if err != nil {
		log.Fatal("error marshaling search body: %w", err)
	}

	req := opensearchapi.SearchRequest{
		Index: []string{indexName},
		Body:  strings.NewReader(string(body)),
	}

	res, err := req.Do(ctx, client)
	if err != nil {
		log.Fatal("error performing search: %w", err)
	}
	defer res.Body.Close()

	var result map[string]interface{}
	if err := json.NewDecoder(res.Body).Decode(&result); err != nil {
		log.Fatal("error parsing the response body: %w", err)
	}

	hits := result["hits"].(map[string]interface{})["hits"].([]interface{})
	totalHits := int(result["hits"].(map[string]interface{})["total"].(map[string]interface{})["value"].(float64))

	var articles []model.ArticleInfo
	for _, hit := range hits {
		source := hit.(map[string]interface{})["_source"].(map[string]interface{})
		article := model.ArticleInfo{
			Title:          source["title"].(string),
			PubDate:        source["pub_date"].(string),
			CompanyName:    source["company_name"].(string),
			URL:            source["url"].(string),
			SummarizedText: source["summarized_text"].(string),
			Hashtags:       parseStringSlice(source["hashtags"]),
		}
		articles = append(articles, article)
	}

	return articles, totalHits
}

func buildSearchQuery(params utils.SearchParams) map[string]interface{} {
	var filterClauses []map[string]interface{}
	var mustClauses []map[string]interface{}

	// Hashtags query (AND condition) using keyword field
	if len(params.Hashtags) > 0 {
		var hashtagClauses []map[string]interface{}
		for _, hashtag := range params.Hashtags {
			hashtagClauses = append(hashtagClauses, map[string]interface{}{
				"term": map[string]interface{}{
					"hashtags.keyword": hashtag,
				},
			})
		}
		filterClauses = append(filterClauses, map[string]interface{}{
			"bool": map[string]interface{}{
				"filter": hashtagClauses,
			},
		})
	}

	// Company name query
	if params.Company != "" {
		filterClauses = append(filterClauses, map[string]interface{}{
			"term": map[string]interface{}{
				"company_name": params.Company,
			},
		})
	}

	// Determine the sorting criteria based on the presence of a search query
	var sortCriteria []map[string]interface{}
	// General search query
	if params.Query != "" {
		mustClauses = append(mustClauses, map[string]interface{}{
			"multi_match": map[string]interface{}{
				"query":          params.Query,
				"fields":         []string{"title^3", "summarized_text^2", "hashtags"},
				"type":           "best_fields",
				"operator":       "or",
				"fuzziness":      "AUTO",
				"prefix_length":  3,
				"max_expansions": 10,
			},
		})
		// If a search query is provided, prioritize relevance (score) then publication date
		sortCriteria = []map[string]interface{}{
			{"_score": map[string]interface{}{"order": "desc"}},
			{"pub_date": map[string]interface{}{"order": "desc"}},
		}
	} else {
		// If no search query, sort by publication date only
		sortCriteria = []map[string]interface{}{
			{"pub_date": map[string]interface{}{"order": "desc"}},
		}
	}

	query := map[string]interface{}{
		"bool": map[string]interface{}{
			"filter": filterClauses,
			"must":   mustClauses,
		},
	}

	return map[string]interface{}{
		"query": query,
		"from":  params.Page * params.Size,
		"size":  params.Size,
		"sort":  sortCriteria,
	}
}

func parseStringSlice(value interface{}) []string {
	if slice, ok := value.([]interface{}); ok {
		result := make([]string, len(slice))
		for i, v := range slice {
			result[i] = v.(string)
		}
		return result
	}
	return []string{}
}
