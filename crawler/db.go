package main

import (
	"crawler/utils"
	"crypto/tls"
	"log"
	"net/http"

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
	return 0

	// 데이터 삽입 구현
}
