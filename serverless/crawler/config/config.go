package config

import (
	"context"
	"log"
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
}

var (
	instance *Config
	once     sync.Once
)

func GetConfigSingletonInstance() *Config {
	once.Do(func() {
		instance = &Config{
			CrawlerConfigFilePath: "s3://tech-blog-hub/config-crawler.yaml",
			IndexName:             "article_infos",
			OpenSearchConfig:      getOpenSearchConfig("https://vpc-opensearch-bdip6fuxrceuqtroiovj234inm.ap-northeast-2.es.amazonaws.com"),
			S3BucketName:          "tech-blog-hub",
			KMSKeyARN:             "arn:aws:kms:ap-northeast-2:051826714237:key/7004defc-09e8-4f1d-8bff-c1aff837ee36",
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
