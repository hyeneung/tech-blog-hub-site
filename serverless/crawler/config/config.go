package config

import (
	"crypto/tls"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"sync"

	"github.com/elastic/go-elasticsearch/v8"
)

type Config struct {
	CrawlerConfigFilePath string
	IndexName             string
	ElasticSearchConfig   elasticsearch.Config
	S3BucketName          string
	KMSKeyARN             string
	TextHandlerLambdaName string
}

var (
	instance *Config
	once     sync.Once
)

func GetConfigSingletonInstance() *Config {
	once.Do(func() {
		instance = &Config{
			CrawlerConfigFilePath: os.Getenv("CRAWLER_CONFIG_FILE_PATH"),
			IndexName:             os.Getenv("INDEX_NAME"),
			ElasticSearchConfig:   getElasticsearchConfig(),
			S3BucketName:          os.Getenv("S3_BUCKET_NAME"),
			KMSKeyARN:             os.Getenv("KMS_KEY_ARN"),
			TextHandlerLambdaName: os.Getenv("TEXT_HANDLER_LAMBDA_NAME"),
		}
	})
	return instance
}

func getElasticsearchConfig() elasticsearch.Config {
	host := os.Getenv("ELASTICSEARCH_HOST")
	portStr := os.Getenv("ELASTICSEARCH_PORT")
	username := os.Getenv("ELASTICSEARCH_USERNAME")
	password := os.Getenv("ELASTICSEARCH_PASSWORD")

	port, err := strconv.Atoi(portStr)
	if err != nil {
		log.Fatalf("Invalid port number: %s", err)
	}

	return elasticsearch.Config{
		Addresses: []string{fmt.Sprintf("https://%s:%d", host, port)},
		Username:  username,
		Password:  password,
		Transport: &http.Transport{
			TLSClientConfig: &tls.Config{
				InsecureSkipVerify: true,
			},
		},
	}
}
