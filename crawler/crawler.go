package main

import (
	"context"
	"crawler/utils"
	"io"
	"time"

	pb "crawler/generated"
)

type Crawler struct {
	Company     string `yaml:"company"`
	URL         string `yaml:"url"`
	LastUpdated int64  `yaml:"lastUpdated"`
}

type CrawlerArray struct {
	Crawlers []Crawler `yaml:"crawlers"`
}

type TextSummarized struct {
	Content        string
	SummarizedText string
	Hashtags       []string
}

func getTextSummary(stub *pb.CrawlerTextHandlerClient, posts *[]utils.Post, lastIdxToUpdate int) *[]TextSummarized {
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*30)
	defer cancel()
	logger := utils.GetLoggerSingletonInstance()

	// connect to grpc server
	stream, err := (*stub).StreamUrlSummaries(ctx)
	if err != nil {
		logger.LogError(err.Error())
		return nil
	}

	results := make([]TextSummarized, 0, lastIdxToUpdate+1)
	resultChan := make(chan TextSummarized, lastIdxToUpdate+1)
	errorChan := make(chan error, 1)
	doneChan := make(chan bool)

	// Goroutine for sending requests
	go func() {
		for i := 0; i <= lastIdxToUpdate; i++ {
			err := stream.Send(&pb.UrlRequest{Url: (*posts)[i].Link})
			if err != nil {
				logger.LogError("Error sending request: " + err.Error())
				errorChan <- err
				return
			}
			logger.LogInfo("Sent request for URL: " + (*posts)[i].Link)
		}
		if err := stream.CloseSend(); err != nil {
			logger.LogError("Error closing send stream: " + err.Error())
			errorChan <- err
		}
	}()

	// Goroutine for receiving responses
	go func() {
		for {
			res, err := stream.Recv()
			if err == io.EOF {
				close(doneChan)
				return
			}
			if err != nil {
				logger.LogError("Error receiving response: " + err.Error())
				errorChan <- err
				return
			}
			resultChan <- TextSummarized{
				Content:        res.Content,
				SummarizedText: res.SummarizedText,
				Hashtags:       res.Hashtags,
			}
		}
	}()

	// Main goroutine for collecting results
	for {
		select {
		case result := <-resultChan:
			results = append(results, result)
		case <-doneChan:
			logger.LogInfo("All data received")
			return &results
		case err := <-errorChan:
			logger.LogError("Error in stream processing: " + err.Error())
			return &results
		case <-ctx.Done():
			logger.LogError("Context deadline exceeded")
			return &results
		}
	}
}

// Run the crawler
func (c *Crawler) Run(stub *pb.CrawlerTextHandlerClient) {
	var postNumToUpdate int = 0
	var postNumUpdated uint32 = 0
	var posts []utils.Post
	var err error

	// read RSS file
	posts, err = utils.GetPostArrayFromUrl(c.URL)
	if err != nil {
		return
	}

	// Determine the range of posts that need to be inserted in the database
	var lastIdxToUpdate int = utils.GetOldestPostIndexForUpdate(posts, c.LastUpdated)
	logger := utils.GetLoggerSingletonInstance()
	// If there are no new posts to update, log the result and exit
	if lastIdxToUpdate < 0 {
		logger.LogCrawlerResult(c.Company, postNumToUpdate, postNumUpdated)
		return
	}

	// get text analysis results (grpc bidirectional)
	var textInfos *[]TextSummarized = getTextSummary(stub, &posts, lastIdxToUpdate)

	// insert results to DB
	postNumUpdated = InsertDB(&posts, textInfos, lastIdxToUpdate)

	// update crawler execution time info
	c.LastUpdated = time.Now().Unix()

	// log the result
	postNumToUpdate = lastIdxToUpdate + 1
	logger.LogCrawlerResult(c.Company, postNumToUpdate, postNumUpdated)
}
