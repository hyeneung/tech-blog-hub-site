package main

import (
	"context"
	"encoding/json"
	"log"
	"net/url"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	"github.com/google/uuid"
)

type LogEntry struct {
	UserID      string `json:"user_id"`
	RedirectURL string `json:"redirect_url"`
}

func HandleRequest(ctx context.Context, request events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	redirectUrl := request.QueryStringParameters["url"]
	if redirectUrl == "" {
		return events.APIGatewayProxyResponse{
			StatusCode: 400,
			Body:       "Missing 'url' parameter",
		}, nil
	}
	// Validate URL
	if _, err := url.ParseRequestURI(redirectUrl); err != nil {
		return events.APIGatewayProxyResponse{
			StatusCode: 400,
			Body:       "Invalid URL",
		}, nil
	}

	// Log the request
	userId := request.Headers["x-user-id"]
	if userId == "" {
		userId = uuid.New().String()
	}
	logEntry := LogEntry{
		UserID:      userId,
		RedirectURL: redirectUrl,
	}
	jsonLog, err := json.Marshal(logEntry)
	if err != nil {
		log.Printf("Error marshaling log entry: %v", err)
	} else {
		log.Println(string(jsonLog))
	}

	// Return a response with redirect status and Location header
	return events.APIGatewayProxyResponse{
		StatusCode: 302,
		Headers: map[string]string{
			"Location":  redirectUrl,
			"X-User-Id": userId,
		},
	}, nil
}

func main() {
	lambda.Start(HandleRequest)
}
