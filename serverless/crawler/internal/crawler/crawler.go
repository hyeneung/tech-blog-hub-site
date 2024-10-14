package crawler

import (
	"math/rand"
	"strings"
	"sync"
	"time"

	db "crawler/internal/db"
	types "crawler/internal/types"
	utils "crawler/internal/utils"
)

// Run the crawler
func (c *Crawler) Run() {
	var postNumToUpdate int = 0
	var postNumUpdated uint32 = 0
	var posts []types.Post
	var err error
	logger := utils.GetLoggerSingletonInstance()
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

	// get text analysis results
	var textInfos *[]types.TextSummarized = getTextSummary(&posts, lastIdxToUpdate)

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

func getTextSummary(posts *[]types.Post, lastIdxToUpdate int) *[]types.TextSummarized {
	results := make([]types.TextSummarized, lastIdxToUpdate+1)
	var wg sync.WaitGroup

	for i := 0; i <= lastIdxToUpdate; i++ {
		wg.Add(1)
		go func(i int, url string) {
			defer wg.Done()
			results[i] = performSummarization(url)
		}(i, (*posts)[i].Link)
	}

	wg.Wait()
	return &results
}

func performSummarization(url string) types.TextSummarized {
	summarizedText := getSummarizedText(url)
	hashtags := getRandomHashtags(url)

	return types.TextSummarized{
		SummarizedText: summarizedText,
		Hashtags:       hashtags,
	}
}

func getRandomHashtags(url string) []string {
	hashtags := []string{
		"Frontend", "Backend", "Infra", "Mobile", "AI", "DataScience",
		"DataEngineering", "DevOps", "React", "UI/UX", "Spring",
		"Architecture", "DB", "IOS", "ReactNative", "Kubernetes", "Security",
	}

	indices := rand.Perm(len(hashtags))[:5]

	result := make([]string, 5)
	for i, idx := range indices {
		result[i] = hashtags[idx]
	}

	return result
}

func getSummarizedText(url string) string {
	return strings.Repeat("요약된 글입니다.", 50)
}
