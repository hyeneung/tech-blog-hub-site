package service

import (
	"context"
	"encoding/json"
	"log"
	"os"
	"searchAPI/internal/model"
	"strings"

	awsConfig "github.com/aws/aws-sdk-go-v2/config"
	"github.com/opensearch-project/opensearch-go/opensearchapi"
	"github.com/opensearch-project/opensearch-go/v2"
	"github.com/opensearch-project/opensearch-go/v2/signer/awsv2"
)

func getOpenSearchConfig() opensearch.Config {
	endpointUrl := os.Getenv("OPENSEARCH_ENDPOINT")

	// load AWS config
	cfg, err := awsConfig.LoadDefaultConfig(context.TODO(), awsConfig.WithRegion("ap-northeast-2"))
	if err != nil {
		log.Fatal("Failed to load AWS config: " + err.Error())
	}
	signer, err := awsv2.NewSignerWithService(cfg, "es")
	if err != nil {
		log.Fatal("Failed to create signer: " + err.Error())
	}

	return opensearch.Config{
		Addresses: []string{endpointUrl},
		Signer:    signer,
	}
}

func PerformSearch(hashtags []string, company, query string, page, size int) ([]model.ArticleInfo, int) {
	indexName := os.Getenv("OPENSEARCH_INDEX_NAME")

	client, err := opensearch.NewClient(getOpenSearchConfig())
	if err != nil {
		log.Fatal("Error creating the client: " + err.Error())
	}

	searchBody := buildSearchQuery(hashtags, company, query, page, size)

	body, err := json.Marshal(searchBody)
	if err != nil {
		log.Fatal("error marshaling search body: %w", err)
	}

	req := opensearchapi.SearchRequest{
		Index: []string{indexName},
		Body:  strings.NewReader(string(body)),
	}

	res, err := req.Do(context.Background(), client)
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

	// Hashtags query
	if len(hashtags) > 0 {
		for _, hashtag := range hashtags {
			mustClauses = append(mustClauses, map[string]interface{}{
				"term": map[string]interface{}{
					"hashtags.keyword": hashtag,
				},
			})
		}
	}

	// Company name query
	if company != "" {
		mustClauses = append(mustClauses, map[string]interface{}{
			"term": map[string]interface{}{
				"company_name": company,
			},
		})
	}

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
	}

	return map[string]interface{}{
		"query": map[string]interface{}{
			"bool": map[string]interface{}{
				"must": mustClauses,
			},
		},
		"from": page * size,
		"size": size,
		"sort": []map[string]interface{}{
			{
				"pub_date": map[string]interface{}{
					"order": "desc",
				},
			},
		},
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
