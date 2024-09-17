package db

import (
	"context"
	"crypto/sha256"
	"crypto/tls"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"sync"
	"sync/atomic"
	"time"

	types "crawler/internal/types"
	utils "crawler/internal/utils"

	"github.com/elastic/go-elasticsearch/v8"
)

type postData struct {
	Title          string
	PubDate        string
	Content        string
	SummarizedText string
	Hashtags       []string
}

func InsertDB(posts *[]types.Post, textInfos *[]types.TextSummarized, lastIdxToUpdate int) uint32 {
	indexName := "posts"
	logger := utils.GetLoggerSingletonInstance()
	// address := os.Getenv("ELASTICSEARCH_ADDRESS")

	cfg := elasticsearch.Config{
		Addresses: []string{"https://localhost:9200"},
		Username:  "elastic",
		Password:  "1234",
		Transport: &http.Transport{
			TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
		},
	}

	es, err := elasticsearch.NewClient(cfg)
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
			Content:        textInfo.Content,
			SummarizedText: textInfo.SummarizedText,
			Hashtags:       textInfo.Hashtags,
		}

		jsonData, err := json.Marshal(data)
		if err != nil {
			logger.LogError("Error marshaling data: " + err.Error())
			resultChan <- false
			return
		}

		hasher := sha256.New()
		hasher.Write([]byte(post.Link))
		documentID := hex.EncodeToString(hasher.Sum(nil))

		res, err := es.Create(
			indexName,
			documentID,
			strings.NewReader(string(jsonData)),
			es.Create.WithContext(ctx),
			es.Create.WithRefresh("true"),
		)
		if err != nil {
			logger.LogError("Error creating document: " + err.Error())
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
