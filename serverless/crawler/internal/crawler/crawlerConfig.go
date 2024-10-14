package crawler

import (
	"bytes"
	"context"
	config "crawler/config"
	"io"
	"log"
	"strings"

	"github.com/aws/aws-sdk-go-v2/aws"
	awsConfig "github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/aws/aws-sdk-go-v2/service/s3/types"
	"gopkg.in/yaml.v2"
)

type Crawler struct {
	Company     string `yaml:"company"`
	URL         string `yaml:"url"`
	LastUpdated int64  `yaml:"lastUpdated"`
}

type CrawlerArray struct {
	Crawlers []Crawler `yaml:"crawlers"`
}

func GetCrawlerArrayAddressFromFile(s3Path string) *CrawlerArray {
	bucket, key := parseS3Path(s3Path)

	cfg, err := awsConfig.LoadDefaultConfig(context.TODO())
	if err != nil {
		log.Fatal("Failed to load AWS config:", err)
	}

	client := s3.NewFromConfig(cfg)

	result, err := client.GetObject(context.TODO(), &s3.GetObjectInput{
		Bucket: aws.String(bucket),
		Key:    aws.String(key),
	})
	if err != nil {
		log.Fatal("Failed to get object from S3:", err)
	}
	defer result.Body.Close()

	data, err := io.ReadAll(result.Body)
	if err != nil {
		log.Fatal("Failed to read S3 object body:", err)
	}

	var crawlerArray CrawlerArray
	err = yaml.Unmarshal(data, &crawlerArray)
	if err != nil {
		log.Fatal("Failed to unmarshal YAML:", err)
	}
	return &crawlerArray
}

func WriteCrawlerInfoToFile(s3Path string, crawlerArrayPointer *CrawlerArray) {
	bucket, key := parseS3Path(s3Path)

	yamlData, err := yaml.Marshal(crawlerArrayPointer)
	if err != nil {
		log.Fatal("Failed to marshal YAML:", err)
	}

	cfg, err := awsConfig.LoadDefaultConfig(context.TODO())
	if err != nil {
		log.Fatal("Failed to load AWS config:", err)
	}

	client := s3.NewFromConfig(cfg)

	_, err = client.PutObject(context.TODO(), &s3.PutObjectInput{
		Bucket:               aws.String(bucket),
		Key:                  aws.String(key),
		Body:                 bytes.NewReader(yamlData),
		ServerSideEncryption: types.ServerSideEncryptionAwsKms,
		SSEKMSKeyId:          aws.String(config.GetConfigSingletonInstance().KMSKeyARN),
	})
	if err != nil {
		log.Fatal("Failed to write object to S3:", err)
	}
}

func parseS3Path(s3Path string) (string, string) {
	parts := strings.SplitN(strings.TrimPrefix(s3Path, "s3://"), "/", 2)
	if len(parts) != 2 {
		log.Fatal("Invalid S3 path format")
	}
	if parts[0] != config.GetConfigSingletonInstance().S3BucketName {
		log.Fatal("Invalid S3 bucket name")
	}
	return parts[0], parts[1]
}
