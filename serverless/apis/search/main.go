package main

import (
	"context"
	"log"
	"os"
	"searchAPI/internal/handler"

	awsConfig "github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-xray-sdk-go/xray"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/go-redis/redis/v8"
	"github.com/opensearch-project/opensearch-go"
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

func getRedisConfig() *redis.Options {
	return &redis.Options{
		Addr: os.Getenv("REDIS_ENDPOINT"),
		DB:   0, // use default DB
	}
}

var openSearchClient *opensearch.Client
var redisClient *redis.Client

func init() {
	var err error
	openSearchClient, err = opensearch.NewClient(getOpenSearchConfig())
	if err != nil {
		log.Fatal("Error creating the client: " + err.Error())
	}
	redisClient = redis.NewClient(getRedisConfig())
	_, err = redisClient.Ping(context.Background()).Result()
	if err != nil {
		log.Fatal("Error connecting to Redis: " + err.Error())
	}
}

func main() {
	lambda.Start(func(request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
		// Start the main segment
		ctx, seg := xray.BeginSegment(context.Background(), "searchAPI")
		defer seg.Close(nil) // Ensure the segment is closed after processing
		return handler.HandleRequest(ctx, request, openSearchClient, redisClient)
	})
}
