package handler

import (
	"context"
	"encoding/json"
	"strconv"
	"strings"

	"searchAPI/internal/model"
	"searchAPI/internal/service"
	"searchAPI/internal/utils"

	"github.com/aws/aws-lambda-go/events"
	"github.com/go-redis/redis/v8"
	"github.com/google/uuid"
	"github.com/opensearch-project/opensearch-go"
)

func HandleRequest(ctx context.Context, request events.APIGatewayProxyRequest, openSearchClient *opensearch.Client, redisClient *redis.Client) (events.APIGatewayProxyResponse, error) {
	// Check for X-User-Id in the request headers
	userId := request.Headers["x-user-id"]
	if userId == "" {
		// If X-User-Id is not present, generate a new UUID v4
		userId = uuid.New().String()
	}

	// Log the request with user ID and all query parameters
	utils.LogRequest(userId, request.QueryStringParameters)

	// parse query params that concerns
	page, _ := strconv.Atoi(request.QueryStringParameters["page"])
	size, _ := strconv.Atoi(request.QueryStringParameters["size"])
	searchParams := utils.SearchParams{
		Hashtags: strings.Split(request.QueryStringParameters["hashtags"], ","),
		Company:  request.QueryStringParameters["company"],
		Query:    request.QueryStringParameters["query"],
		Page:     page,
		Size:     size,
	}
	// handle empty hashtags param
	if len(searchParams.Hashtags) == 1 && searchParams.Hashtags[0] == "" {
		searchParams.Hashtags = []string{}
	}

	// Validate input parameters
	if err := utils.ValidateParams(searchParams); err != nil {
		return errorResponse(400, err.Error(), userId)
	}

	// Prepare response
	response := model.SearchResponse{
		Status:  200,
		Message: "Success",
		Content: service.PerformSearch(ctx, openSearchClient, redisClient, searchParams),
	}

	// Serialize response to JSON
	jsonResponse, err := json.Marshal(response)
	if err != nil {
		return errorResponse(500, "Error serializing response", userId)
	}

	// Return successful response
	return events.APIGatewayProxyResponse{
		StatusCode: 200,
		Headers: map[string]string{
			"Content-Type": "application/json",
			"X-User-Id":    userId,
		},
		Body: string(jsonResponse),
	}, nil
}

func errorResponse(statusCode int, message string, userId string) (events.APIGatewayProxyResponse, error) {
	return events.APIGatewayProxyResponse{
		StatusCode: statusCode,
		Headers: map[string]string{
			"X-User-Id": userId,
		},
		Body: string(model.NewErrorResponse(statusCode, message)),
	}, nil
}
