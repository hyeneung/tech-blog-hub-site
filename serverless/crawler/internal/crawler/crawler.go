package crawler

import (
	"context"
	"strings"
	"sync"
	"time"

	db "crawler/internal/db"

	types "crawler/internal/types"
	utils "crawler/internal/utils"

	"github.com/aws/aws-xray-sdk-go/xray"
	"github.com/opensearch-project/opensearch-go/v2"
)

// Run the crawler
func (c *Crawler) Run(ctx context.Context, client *opensearch.Client) {
	ctx, segCrawler := xray.BeginSubsegment(ctx, "Run")
	defer segCrawler.Close(nil)
	segCrawler.AddMetadata("Company", c.Company)
	logger := utils.GetLoggerSingletonInstance()

	// read RSS file
	posts, err := utils.GetPostArrayFromUrl(ctx, c.MetaFileURL)
	if err != nil {
		return
	}

	// Reverse RSS file data if necessary
	c.reversePosts(posts)

	// Check for newly uploaded posts
	var postNumToUpdate int = 0
	var postNumUpdated uint32 = 0
	var lastIdxToUpdate int = getOldestPostIndexForUpdate(&posts, c.LastUpdated)
	// If there are no new posts to update, log the result and exit
	if lastIdxToUpdate < 0 {
		logger.LogCrawlerResult(c.Company, postNumToUpdate, postNumUpdated)
		return
	}

	// get text analysis results
	textInfos := getTextAnalysisResult(ctx, &posts, lastIdxToUpdate)

	// insert results to DB
	postNumUpdated = db.InsertDB(client, ctx, c.Company, &posts, textInfos, lastIdxToUpdate)

	// update crawler execution time info
	c.LastUpdated = time.Now().Unix()

	// log the result
	postNumToUpdate = lastIdxToUpdate + 1
	logger.LogCrawlerResult(c.Company, postNumToUpdate, postNumUpdated)
}

// reversePosts checks if the company is KakaoPay and reverses the posts slice if true.
func (c *Crawler) reversePosts(posts []types.Post) {
	// For KakaoPay, the RSS file is structured such that the most recent posts are at the end of the list,
	if c.Company == "카카오페이" {
		reverse(posts) // Reverse the posts order for KakaoPay
	}
}

// reverses the order of the posts slice in place.
func reverse(posts []types.Post) {
	for i, j := 0, len(posts)-1; i < j; i, j = i+1, j-1 {
		posts[i], posts[j] = posts[j], posts[i] // Swap elements
	}
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

		// Trim the link to exclude query parameters
		if strings.Contains(post.Link, "?") {
			linkParts := strings.Split(post.Link, "?")
			(*posts)[i].Link = linkParts[0] // Keep only the part before '?'
			// don't need {url}?source=rss----18356045d353---4
		}

		if unixTime <= lastUpdatedDateUnixTime {
			return i - 1 // last one that needs updating
		}
	}
	return len((*posts)) - 1 // all posts need to be updated
}

func getTextAnalysisResult(ctx context.Context, posts *[]types.Post, lastIdxToUpdate int) *[]types.TextAnalysisResult {
	results := make([]types.TextAnalysisResult, lastIdxToUpdate+1)
	var wg sync.WaitGroup

	for i := 0; i <= lastIdxToUpdate; i++ {
		wg.Add(1)
		go func(i int, url string) {
			defer wg.Done()
			// call text_handler lambda function
			_, segTextAnalysis := xray.BeginSubsegment(ctx, "Text Analyze")
			results[i] = utils.ExecuteTextHandlerLambda(url)
			segTextAnalysis.Close(nil)
		}(i, (*posts)[i].Link)
	}

	wg.Wait()
	return &results
}
