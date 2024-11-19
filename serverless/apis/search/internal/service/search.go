package service

import (
	"context"
	"encoding/json"
	"log"
	"os"
	"searchAPI/internal/model"
	"strings"

	"github.com/opensearch-project/opensearch-go"
	"github.com/opensearch-project/opensearch-go/opensearchapi"
)

func PerformSearch(ctx context.Context, client *opensearch.Client, hashtags []string, company, query string, page, size int) ([]model.ArticleInfo, int) {
	indexName := os.Getenv("OPENSEARCH_INDEX_NAME")

	searchBody := buildSearchQuery(hashtags, company, query, page, size)

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

func buildSearchQuery(hashtags []string, company, query string, page, size int) map[string]interface{} {
	var mustClauses []map[string]interface{}

	// Hashtags query (AND condition) using keyword field
	if len(hashtags) > 0 {
		var hashtagClauses []map[string]interface{}
		for _, hashtag := range hashtags {
			hashtagClauses = append(hashtagClauses, map[string]interface{}{
				"term": map[string]interface{}{
					"hashtags.keyword": hashtag,
				},
			})
		}
		mustClauses = append(mustClauses, map[string]interface{}{
			"bool": map[string]interface{}{
				"must": hashtagClauses,
			},
		})
	}

	// Company name query
	if company != "" {
		mustClauses = append(mustClauses, map[string]interface{}{
			"term": map[string]interface{}{
				"company_name": company,
			},
		})
	}

	// Determine the sorting criteria based on the presence of a search query
	var sortCriteria []map[string]interface{}
	// General search query
	if query != "" {
		mustClauses = append(mustClauses, map[string]interface{}{
			"multi_match": map[string]interface{}{
				"query":          query,
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

	return map[string]interface{}{
		"query": map[string]interface{}{
			"bool": map[string]interface{}{
				"must": mustClauses,
			},
		},
		"from": page * size,
		"size": size,
		"sort": sortCriteria,
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
