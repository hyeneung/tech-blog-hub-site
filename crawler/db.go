package main

import (
	"bytes"
	"context"
	"crawler/utils"
	"crypto/sha256"
	"crypto/tls"
	"encoding/hex"
	"encoding/json"
	"log"
	"net/http"
	"sync"
	"sync/atomic"
	"time"

	"github.com/elastic/go-elasticsearch/esapi"
	"github.com/elastic/go-elasticsearch/v8"
)

type PostData struct {
	Title          string
	PubDate        string
	Content        string
	SummarizedText string
	Hashtags       []string
}

func InsertDB(posts *[]utils.Post, textInfos *[]TextSummarized, lastIdxToUpdate int) uint32 {
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

	// Elastic Search 사용
	res, err := es.Info()
	if err != nil {
		log.Fatalf("Error getting response: %s", err)
	}
	defer res.Body.Close()
	logger.LogInfo(res.String())

	ctx, cancel := context.WithTimeout(context.Background(), time.Second*60)
	defer cancel()

	var successCount uint32 = 0

	var wg sync.WaitGroup
	resultChan := make(chan bool, lastIdxToUpdate+1)

	worker := func(post utils.Post, textInfo TextSummarized) {
		defer wg.Done()
		data := PostData{
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

		// URL을 해시하여 문서 ID로 사용
		hasher := sha256.New()
		hasher.Write([]byte(post.Link))
		documentID := hex.EncodeToString(hasher.Sum(nil))

		req := esapi.IndexRequest{
			Index:      "posts",
			DocumentID: documentID,
			Body:       bytes.NewReader(jsonData),
			Refresh:    "true",
		}

		res, err := req.Do(ctx, es)
		if err != nil {
			logger.LogError("Error indexing document: " + err.Error())
			resultChan <- false
			return
		}
		defer res.Body.Close()

		if res.IsError() {
			logger.LogError("Error indexing document: " + res.String())
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

	// 결과 집계
	for success := range resultChan {
		if success {
			atomic.AddUint32(&successCount, 1)
		}
	}

	return successCount
}
