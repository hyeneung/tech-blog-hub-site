package db

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"strings"
	"sync"
	"sync/atomic"
	"time"

	config "crawler/config"
	types "crawler/internal/types"
	utils "crawler/internal/utils"

	"github.com/elastic/go-elasticsearch/v8"
)

type postData struct {
	Title          string   `json:"title"`
	PubDate        string   `json:"pub_date"`
	CompanyName    string   `json:"company_name"`
	URL            string   `json:"url"`
	Content        string   `json:"content"`
	SummarizedText string   `json:"summarized_text"`
	Hashtags       []string `json:"hashtags"`
	CreatedAt      string   `json:"created_at"`
}

func InsertDB(companyName string, posts *[]types.Post, textInfos *[]types.TextSummarized, lastIdxToUpdate int) uint32 {
	logger := utils.GetLoggerSingletonInstance()
	config := config.GetConfigSingletonInstance()

	es, err := elasticsearch.NewClient(config.ElasticsearchConfig)

	if err != nil {
		logger.LogError("Error creating the client: " + err.Error())
	}

	res, err := es.Info()
	if err != nil {
		logger.LogError("Error getting response from Elasticsearch: " + err.Error())
	}
	defer res.Body.Close()

	ctx, cancel := context.WithTimeout(context.Background(), time.Second*60)
	defer cancel()

	var successCount uint32 = 0

	var wg sync.WaitGroup
	resultChan := make(chan bool, lastIdxToUpdate+1)

	worker := func(post types.Post, textInfo types.TextSummarized) {
		defer wg.Done()
		data := postData{
			Title:          post.Title,
			PubDate:        post.PubDate,
			CompanyName:    companyName,
			URL:            post.Link,
			Content:        textInfo.Content,
			SummarizedText: textInfo.SummarizedText,
			Hashtags:       textInfo.Hashtags,
			CreatedAt:      time.Now().UTC().Format(time.RFC3339),
		}

		jsonData, err := json.Marshal(data)
		if err != nil {
			logger.LogError("Error marshaling data: " + err.Error())
			resultChan <- false
			return
		}

		hasher := sha256.New()
		hasher.Write([]byte(post.Link))
		documentID := hex.EncodeToString(hasher.Sum(nil)) // URL should be unique

		res, err := es.Create(
			config.IndexName,
			documentID,
			strings.NewReader(string(jsonData)),
			es.Create.WithContext(ctx),
			es.Create.WithRefresh("true"),
		)
		if err != nil {
			if err == context.Canceled {
				logger.LogError("Request was canceled by context")
			} else if err == context.DeadlineExceeded {
				logger.LogError("Request timed out")
			} else {
				logger.LogError("Error creating document: " + err.Error())
			}
			resultChan <- false
			return
		}
		defer res.Body.Close()

		if res.StatusCode == 409 {
			logger.LogInfo(fmt.Sprintf("Document already exists: Link=%s, DocumentID=%s", post.Link, documentID))
			resultChan <- false
		} else if res.IsError() {
			logger.LogError("Error creating document: " + res.String())
			resultChan <- false
		} else {
			resultChan <- true
		}
	}

	for i := 0; i <= lastIdxToUpdate && i < len(*posts); i++ {
		wg.Add(1)
		go worker((*posts)[i], (*textInfos)[i])
	}

	go func() {
		wg.Wait()
		close(resultChan)
	}()
	for success := range resultChan {
		if success {
			atomic.AddUint32(&successCount, 1)
		}
	}

	return successCount
}
