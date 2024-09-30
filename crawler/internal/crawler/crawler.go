package crawler

import (
	"context"
	"io"
	"time"

	pb "crawler/generated"
	db "crawler/internal/db"
	types "crawler/internal/types"
	utils "crawler/internal/utils"
)

// Run the crawler
func (c *Crawler) Run(stub *pb.CrawlerTextHandlerClient) {
	var postNumToUpdate int = 0
	var postNumUpdated uint32 = 0
	var posts []types.Post
	var err error
	logger := utils.GetLoggerSingletonInstance()
	logger.LogDebug("starting " + c.Company + " crawler")
	// read RSS file
	posts, err = utils.GetPostArrayFromUrl(c.URL)
	if err != nil {
		return
	}
	// Determine the range of posts that need to be inserted in the database
	var lastIdxToUpdate int = getOldestPostIndexForUpdate(posts, c.LastUpdated)
	// If there are no new posts to update, log the result and exit
	if lastIdxToUpdate < 0 {
		logger.LogCrawlerResult(c.Company, postNumToUpdate, postNumUpdated)
		return
	}

	// get text analysis results (grpc bidirectional)
	var textInfos *[]types.TextSummarized = getTextSummary(stub, &posts, lastIdxToUpdate)

	// insert results to DB
	postNumUpdated = db.InsertDB(c.Company, &posts, textInfos, lastIdxToUpdate)

	// update crawler execution time info
	c.LastUpdated = time.Now().Unix()

	// log the result
	postNumToUpdate = lastIdxToUpdate + 1
	logger.LogCrawlerResult(c.Company, postNumToUpdate, postNumUpdated)
}

// The posts are assumed to be sorted in descending order by date (newest first).
// Returns the index of the oldest post that needs to be updated.
// The index starts from 0. If there are no posts to update, it returns -1.
func getOldestPostIndexForUpdate(posts []types.Post, lastUpdatedDateUnixTime int64) int {
	logger := utils.GetLoggerSingletonInstance()
	for i, post := range posts {
		if post.PubDate == "" {
			continue
		}
		standardizedDate := utils.GetRFC3339TimeFormat(posts[i].PubDate)
		if standardizedDate == "" {
			logger.LogError("Failed to standardize date: " + posts[i].PubDate)
			continue
		}
		posts[i].PubDate = standardizedDate

		unixTime, err := utils.RFC3339TimeToUnixTime(standardizedDate)
		if err != nil {
			logger.LogError("Failed to convert to Unix time: " + err.Error())
			continue
		}
		if unixTime <= lastUpdatedDateUnixTime {
			return i - 1 // last one that needs updating
		}
	}
	return len(posts) - 1 // all posts need to be updated
}

func getTextSummary(stub *pb.CrawlerTextHandlerClient, posts *[]types.Post, lastIdxToUpdate int) *[]types.TextSummarized {
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*30)
	defer cancel()
	logger := utils.GetLoggerSingletonInstance()

	// connect to grpc server
	stream, err := (*stub).StreamUrlSummaries(ctx)
	if err != nil {
		logger.LogError(err.Error())
		return nil
	}

	results := make([]types.TextSummarized, 0, lastIdxToUpdate+1)
	resultChan := make(chan types.TextSummarized, lastIdxToUpdate+1)
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
			logger.LogDebug("Sent request for URL: " + (*posts)[i].Link)
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
			resultChan <- types.TextSummarized{
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
			logger.LogDebug("All data received")
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
