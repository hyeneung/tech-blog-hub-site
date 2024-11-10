package crawler

import (
	"context"
	"sync"
	"time"

	db "crawler/internal/db"

	types "crawler/internal/types"
	utils "crawler/internal/utils"

	"github.com/aws/aws-xray-sdk-go/xray"
)

// Run the crawler
func (c *Crawler) Run(ctx context.Context) {
	var postNumToUpdate int = 0
	var postNumUpdated uint32 = 0
	var posts []types.Post
	var err error

	ctx, segCrawler := xray.BeginSubsegment(ctx, "Run")
	defer segCrawler.Close(nil)

	logger := utils.GetLoggerSingletonInstance()

	// read RSS file
	_, segReadRSS := xray.BeginSubsegment(ctx, "Read RSS")
	posts, err = utils.GetPostArrayFromUrl(c.MetaFileURL)
	segReadRSS.Close(nil)
	if err != nil {
		return
	}

	// Determine the range of posts that need to be inserted in the database
	var lastIdxToUpdate int = getOldestPostIndexForUpdate(&posts, c.LastUpdated)
	// If there are no new posts to update, log the result and exit
	if lastIdxToUpdate < 0 {
		logger.LogCrawlerResult(c.Company, postNumToUpdate, postNumUpdated)
		return
	}

	// get text analysis results
	_, segTextAnalysis := xray.BeginSubsegment(ctx, "Text Analyze")
	var textInfos *[]types.TextAnalysisResult = getTextAnalysisResult(&posts, lastIdxToUpdate)
	segTextAnalysis.Close(nil)

	// insert results to DB
	_, segInsertDB := xray.BeginSubsegment(ctx, "Insert DB")
	postNumUpdated = db.InsertDB(c.Company, &posts, textInfos, lastIdxToUpdate)
	segInsertDB.Close(nil)

	// update crawler execution time info
	c.LastUpdated = time.Now().Unix()

	// log the result
	postNumToUpdate = lastIdxToUpdate + 1
	logger.LogCrawlerResult(c.Company, postNumToUpdate, postNumUpdated)
}

// The posts are assumed to be sorted in descending order by date (newest first).
// Returns the index of the oldest post that needs to be updated.
// The index starts from 0. If there are no posts to update, it returns -1.
func getOldestPostIndexForUpdate(posts *[]types.Post, lastUpdatedDateUnixTime int64) int {
	logger := utils.GetLoggerSingletonInstance()
	for i, post := range *posts {
		if post.PubDate == "" {
			continue
		}
		standardizedDate := utils.GetRFC3339TimeFormat((*posts)[i].PubDate)
		if standardizedDate == "" {
			logger.LogWarn("Failed to standardize date: " + (*posts)[i].PubDate)
			continue
		}
		(*posts)[i].PubDate = standardizedDate

		unixTime, err := utils.RFC3339TimeToUnixTime(standardizedDate)
		if err != nil {
			logger.LogWarn("Failed to convert to Unix time: " + err.Error())
			continue
		}
		if unixTime <= lastUpdatedDateUnixTime {
			return i - 1 // last one that needs updating
		}
	}
	return len((*posts)) - 1 // all posts need to be updated
}

func getTextAnalysisResult(posts *[]types.Post, lastIdxToUpdate int) *[]types.TextAnalysisResult {
	results := make([]types.TextAnalysisResult, lastIdxToUpdate+1)
	var wg sync.WaitGroup

	for i := 0; i <= lastIdxToUpdate; i++ {
		wg.Add(1)
		go func(i int, url string) {
			defer wg.Done()
			results[i] = utils.ExecuteTextHandlerLambda(url)
		}(i, (*posts)[i].Link)
	}

	wg.Wait()
	return &results
}
