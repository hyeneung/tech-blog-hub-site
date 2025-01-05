package db

import (
	"bytes"
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"time"

	config "crawler/config"
	types "crawler/internal/types"
	utils "crawler/internal/utils"

	"github.com/aws/aws-xray-sdk-go/xray"
	"github.com/elastic/go-elasticsearch/esapi"
	"github.com/elastic/go-elasticsearch/v8"
)

type postData struct {
	Title          string   `json:"title"`
	PubDate        string   `json:"pub_date"`
	CompanyName    string   `json:"company_name"`
	URL            string   `json:"url"`
	SummarizedText string   `json:"summarized_text"`
	Hashtags       []string `json:"hashtags"`
	CreatedAt      string   `json:"created_at"`
}

func InsertDB(client *elasticsearch.Client, ctx context.Context, companyName string, posts *[]types.Post, textInfos *[]types.TextAnalysisResult, lastIdxToUpdate int) uint32 {
	config := config.GetConfigSingletonInstance()

	// prepare bulk insert request
	var bulkRequestBody bytes.Buffer
	for i := 0; i <= lastIdxToUpdate && i < len(*posts); i++ {
		post, textInfo := (*posts)[i], (*textInfos)[i]
		data := postData{
			Title:          post.Title,
			PubDate:        post.PubDate,
			CompanyName:    companyName,
			URL:            post.Link,
			SummarizedText: textInfo.SummarizedText,
			Hashtags:       textInfo.Hashtags,
			CreatedAt:      time.Now().UTC().Format(time.RFC3339),
		}
		appendToBulkRequestBody(&bulkRequestBody, data, config)
	}
	_, segInsertDB := xray.BeginSubsegment(ctx, "Insert DB")
	successCount := executeBulkInsert(client, &bulkRequestBody, ctx)
	segInsertDB.Close(nil)

	return successCount
}

func appendToBulkRequestBody(buf *bytes.Buffer, data postData, config *config.Config) {
	meta := []byte(fmt.Sprintf(`{ "create" : { "_index" : "%s", "_id" : "%s" } }%s`, config.IndexName, getDocumentID(data.URL), "\n"))
	dataJSON, err := json.Marshal(data)
	if err != nil {
		utils.GetLoggerSingletonInstance().LogError("Error marshaling data: " + err.Error())
		return
	}
	dataJSON = append(dataJSON, "\n"...)

	buf.Grow(len(meta) + len(dataJSON))
	buf.Write(meta)
	buf.Write(dataJSON)
}

func executeBulkInsert(client *elasticsearch.Client, bulkBody *bytes.Buffer, ctx context.Context) uint32 {
	logger := utils.GetLoggerSingletonInstance()
	req := esapi.BulkRequest{
		Body: bytes.NewReader(bulkBody.Bytes()),
	}

	res, err := req.Do(ctx, client)
	if err != nil {
		logger.LogError("Error executing bulk request: " + err.Error())
		return 0
	}
	defer res.Body.Close()

	return countSuccessfulInserts(res)
}

func countSuccessfulInserts(res *esapi.Response) uint32 {
	logger := utils.GetLoggerSingletonInstance()

	// parse response
	var bulkResponse struct {
		Items []struct {
			Create struct {
				Status int    `json:"status"`
				Id     string `json:"_id"`
				Error  struct {
					Type   string `json:"type"`
					Reason string `json:"reason"`
				} `json:"error,omitempty"`
			} `json:"create"`
		} `json:"items"`
	}
	if err := json.NewDecoder(res.Body).Decode(&bulkResponse); err != nil {
		logger.LogError("Error parsing bulk response: " + err.Error())
		return 0
	}

	// get success count
	var successCount uint32
	for _, item := range bulkResponse.Items {
		if item.Create.Status == 409 {
			logger.LogWarn(fmt.Sprintf("Document already exists: ID=%s", item.Create.Id))
		} else if item.Create.Status >= 200 && item.Create.Status < 300 {
			successCount++
		} else {
			logger.LogError(fmt.Sprintf("Error creating document: ID=%s, Status=%d, Type=%s, Reason=%s",
				item.Create.Id, item.Create.Status, item.Create.Error.Type, item.Create.Error.Reason))
		}
	}
	return successCount
}

func getDocumentID(url string) string {
	hasher := sha256.New()
	hasher.Write([]byte(url))
	return hex.EncodeToString(hasher.Sum(nil))
}
