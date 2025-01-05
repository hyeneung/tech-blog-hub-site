package main

import (
	"context"
	"crypto/tls"
	"fmt"
	"log"
	"net/http"
	"os"
	"searchAPI/internal/handler"
	"strconv"

	"github.com/aws/aws-xray-sdk-go/xray"
	"github.com/elastic/go-elasticsearch/v8"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/go-redis/redis/v8"
)

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

func getRedisConfig() *redis.Options {
	return &redis.Options{
		Addr: os.Getenv("REDIS_ENDPOINT"),
		DB:   0, // use default DB
	}
}

var elasticClient *elasticsearch.Client
var redisClient *redis.Client

func init() {
	var err error
	elasticClient, err = elasticsearch.NewClient(getElasticsearchConfig())
	if err != nil {
		log.Fatal("Error creating Elasticsearch client: " + err.Error())
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
		return handler.HandleRequest(ctx, request, elasticClient, redisClient)
	})
}
