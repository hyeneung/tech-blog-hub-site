package utils

import (
	"encoding/xml"
	"fmt"
	"io"
	"net/http"
	"runtime"
	"sync"
)

type ParsedData struct {
	Data []Post `xml:"channel>item"`
}

type Post struct {
	Title   string `xml:"title"`
	Link    string `xml:"link"`
	PubDate string `xml:"pubDate"`
}

func GetPostArrayFromUrl(url string) ([]Post, error) {
	res, err := http.Get(url)
	if err != nil {
		GetLoggerSingletonInstance().LogError(err.Error())
		return nil, err
	}
	if res.StatusCode != http.StatusOK {
		GetLoggerSingletonInstance().LogHttpResponseError(res)
		return nil, fmt.Errorf("failed to parse XML")
	}
	defer res.Body.Close()

	data, err := io.ReadAll(res.Body)
	if err != nil {
		GetLoggerSingletonInstance().LogError(err.Error())
		return nil, err
	}
	var posts ParsedData
	xmlerr := xml.Unmarshal(data, &posts)
	if xmlerr != nil {
		GetLoggerSingletonInstance().LogError(xmlerr.Error())
		return nil, xmlerr
	}

	return posts.Data, nil
}

// Returns the index of the oldest post that needs to be updated.
// The index starts from 0. If there are no posts to update, it returns -1.
func GetOldestPostIndexForUpdate(posts []Post, updatedDate int64) int {
	lastUpdatedDate := UnixTime2Time(updatedDate)
	numPosts := len(posts)
	numWorkers := runtime.NumCPU()
	chunkSize := (numPosts + numWorkers - 1) / numWorkers

	resultCh := make(chan int, numWorkers)
	var wg sync.WaitGroup

	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		start := i * chunkSize
		end := min(start+chunkSize, numPosts)
		go func(start, end int) {
			defer wg.Done()
			var lastIdx int = -1
			for i := start; i < end; i++ {
				post := posts[i]
				if posts[i].PubDate == "" {
					continue
				}
				pubDate := Str2time(post.PubDate)
				if pubDate.Compare(lastUpdatedDate) == 1 {
					lastIdx = i
				} else {
					break
				}
			}
			resultCh <- lastIdx
		}(start, end)
	}
	go func() {
		wg.Wait()
		close(resultCh)
	}()
	maxIdx := -1
	for i := 0; i < numWorkers; i++ {
		if idx := <-resultCh; idx > maxIdx {
			maxIdx = idx
		}
	}

	return maxIdx
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
