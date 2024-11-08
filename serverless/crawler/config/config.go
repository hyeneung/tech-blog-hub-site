package config

import (
	"context"
	"log"
	"os"
	"sync"

	awsConfig "github.com/aws/aws-sdk-go-v2/config"
	"github.com/opensearch-project/opensearch-go/v2"
	"github.com/opensearch-project/opensearch-go/v2/signer/awsv2"
)

type Config struct {
	CrawlerConfigFilePath string
	IndexName             string
	OpenSearchConfig      opensearch.Config
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
			OpenSearchConfig:      getOpenSearchConfig(os.Getenv("OPENSEARCH_ENDPOINT")),
			S3BucketName:          os.Getenv("S3_BUCKET_NAME"),
			KMSKeyARN:             os.Getenv("KMS_KEY_ARN"),
			TextHandlerLambdaName: os.Getenv("TEXT_HANDLER_LAMBDA_NAME"),
		}
	})
	return instance
}

func getOpenSearchConfig(endpointUrl string) opensearch.Config {
	// AWS 설정 로드
	cfg, err := awsConfig.LoadDefaultConfig(context.TODO(), awsConfig.WithRegion("ap-northeast-2"))
	if err != nil {
		log.Fatal("Failed to load AWS config: " + err.Error())
	}

	// AWS 서명자 생성
	signer, err := awsv2.NewSignerWithService(cfg, "es")
	if err != nil {
		log.Fatal("Failed to create signer: " + err.Error())
	}

	return opensearch.Config{
		Addresses: []string{endpointUrl},
		Signer:    signer,
	}
}
