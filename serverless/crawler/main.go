package main

import (
	"context"
	"sync"

	config "crawler/config"
	crawlerUtils "crawler/internal/crawler"

	"github.com/aws/aws-lambda-go/lambda"
)

var (
	cfg *config.Config
)

func init() {
	cfg = config.GetConfigSingletonInstance()
}

func handleRequest(ctx context.Context, event interface{}) {
	// read crawler info from config file
	configFilePath := cfg.CrawlerConfigFilePath
	crawlerArrayAddress := crawlerUtils.GetCrawlerArrayAddressFromFile(configFilePath)

	// run all crawlers
	var wg sync.WaitGroup
	for i := range crawlerArrayAddress.Crawlers {
		wg.Add(1)
		go func(crawler *crawlerUtils.Crawler) {
			defer wg.Done()
			crawler.Run()
		}(&crawlerArrayAddress.Crawlers[i])
	}
	wg.Wait()

	// save changed crawler info
	crawlerUtils.WriteCrawlerInfoToFile(configFilePath, crawlerArrayAddress)
}

func main() {
	lambda.Start(handleRequest)
}
