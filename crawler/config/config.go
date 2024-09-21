package config

import (
	"crypto/tls"
	"net/http"
	"os"
	"strconv"
	"sync"

	"github.com/elastic/go-elasticsearch/v8"
)

type Config struct {
	GRPCServerAddress     string
	CrawlerConfigFilePath string
	LogFolderPath         string
	IndexName             string
	ElasticsearchConfig   elasticsearch.Config
}

var (
	instance *Config
	once     sync.Once
)

func GetConfigSingletonInstance() *Config {
	once.Do(func() {
		instance = &Config{
			GRPCServerAddress:     getEnv("GRPC_SERVER_ADDRESS", "localhost:50051"),
			CrawlerConfigFilePath: getEnv("CRAWLER_CONFIG_FILE_PATH", "./config/config-crawler.yaml"),
			LogFolderPath:         getEnv("CRAWLER_LOG_FOLDER_PATH", "./log/"),
			IndexName:             getEnv("ELASTICSEARCH_INDEX_NAME", "articleinfos"),
			ElasticsearchConfig:   getElasticsearchConfig(),
		}
	})
	return instance
}

func getElasticsearchConfig() elasticsearch.Config {
	return elasticsearch.Config{
		Addresses: []string{
			getEnv("ELASTICSEARCH_ADDRESS", "https://localhost:9200"),
		},
		Username: getEnv("ELASTICSEARCH_USERNAME", "elastic"),
		Password: getEnv("ELASTICSEARCH_PASSWORD", "1234"),
		Transport: &http.Transport{
			TLSClientConfig: &tls.Config{
				InsecureSkipVerify: getBoolEnv("ELASTICSEARCH_INSECURE_SKIP_VERIFY", true),
			},
		},
	}
}

func getEnv(key, defaultValue string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return defaultValue
}

func getBoolEnv(key string, defaultValue bool) bool {
	strValue := getEnv(key, strconv.FormatBool(defaultValue))
	boolValue, err := strconv.ParseBool(strValue)
	if err != nil {
		return defaultValue
	}
	return boolValue
}
