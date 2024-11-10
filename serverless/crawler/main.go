package main

import (
	"context"
	"sync"

	config "crawler/config"
	crawlerUtils "crawler/internal/crawler"

	"github.com/aws/aws-lambda-go/lambda"
	"github.com/aws/aws-xray-sdk-go/xray"
)

var (
	cfg *config.Config
)

func init() {
	cfg = config.GetConfigSingletonInstance()
}

func handleRequest(ctx context.Context, event interface{}) {
	// Start the main segment
	ctx, seg := xray.BeginSegment(ctx, "crawler")
	defer seg.Close(nil) // Ensure the segment is closed after processing

	// read crawler info from config file
	configFilePath := cfg.CrawlerConfigFilePath
	crawlerArrayAddress := crawlerUtils.GetCrawlerArrayAddressFromFile(ctx, configFilePath)

	// run all crawlers
	var wg sync.WaitGroup
	for i := range crawlerArrayAddress.Crawlers {
		wg.Add(1)
		// Pass by pointer to reflect changes and avoid memory copying of the full struct size
		go func(crawler *crawlerUtils.Crawler) {
			defer wg.Done()
			crawler.Run(ctx)
		}(&crawlerArrayAddress.Crawlers[i])
	}
	wg.Wait()

	// save changed crawler info
	crawlerUtils.WriteCrawlerInfoToFile(ctx, configFilePath, crawlerArrayAddress)
}

func main() {
	lambda.Start(handleRequest)
}
