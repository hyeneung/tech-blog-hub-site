package utils

import (
	"crawler/config"
	types "crawler/internal/types"
	"encoding/json"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/lambda"
)

type LambdaResponse struct {
	StatusCode int             `json:"statusCode"`
	Body       json.RawMessage `json:"body"`
}

func ExecuteTextHandlerLambda(url string) types.TextAnalysisResult {
	logger := GetLoggerSingletonInstance()

	// call lambda function
	lambdaResult := invokeTextHandlerLambda(url)

	response, err := parseLambdaResponse(lambdaResult)
	if err != nil {
		logger.LogError("Error parsing Lambda response: " + err.Error())
		return types.TextAnalysisResult{}
	}

	if response.StatusCode != 200 {
		logger.LogError("Lambda function returned non-200 status code")
		return types.TextAnalysisResult{}
	}

	result, err := parseTextAnalysisResult(response.Body)
	if err != nil {
		logger.LogError("Error parsing response body: " + err.Error())
		return types.TextAnalysisResult{}
	}

	return result
}

func invokeTextHandlerLambda(url string) []byte {
	logger := GetLoggerSingletonInstance()
	sess := session.Must(session.NewSessionWithOptions(session.Options{
		SharedConfigState: session.SharedConfigEnable,
	}))

	client := lambda.New(sess)

	payload, err := json.Marshal(map[string]string{"url": url})
	if err != nil {
		logger.LogError("Error creating payload: " + err.Error())
		return nil
	}

	result, err := client.Invoke(&lambda.InvokeInput{
		FunctionName: aws.String(config.GetConfigSingletonInstance().TextHandlerLambdaName),
		Payload:      payload,
	})

	if err != nil {
		logger.LogError("Error calling Lambda function: " + err.Error())
		return nil
	}

	return result.Payload
}

// unmarshals the Lambda response into LambdaResponse struct
func parseLambdaResponse(lambdaResult []byte) (LambdaResponse, error) {
	var response LambdaResponse
	err := json.Unmarshal(lambdaResult, &response)
	return response, err
}

// unmarshals the response body into TextAnalysisResult struct
func parseTextAnalysisResult(body json.RawMessage) (types.TextAnalysisResult, error) {
	// json.RawMessage -> string
	// handle escape sentence.   \\\"summarized_text\\\": ... -> "summarized_text"
	var unescapedBody string
	err := json.Unmarshal(body, &unescapedBody)
	if err != nil {
		return types.TextAnalysisResult{}, err
	}

	// string -> textAnalysisResult
	var result types.TextAnalysisResult
	err = json.Unmarshal([]byte(unescapedBody), &result)
	if err != nil {
		return types.TextAnalysisResult{}, err
	}

	return result, nil
}
