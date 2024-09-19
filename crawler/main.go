package main

import (
	"log"
	"sync"

	config "crawler/config"
	pb "crawler/generated" // {module_name}/package
	crawlerUtils "crawler/internal/crawler"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {
	// Initialize the logger singleton instance
	// This logger is used throughout the application and should only be initialized and closed in the main function
	// Do not call Close() from any other part of the application
	// The logger uses asynchronous logging, so proper initialization and closure are crucial
	logger := utils.GetLoggerSingletonInstance()
	defer logger.Close()

	cfg := config.GetConfigSingletonInstance()

	address := cfg.GRPCServerAddress
	conn, err := grpc.NewClient(address, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	stub := pb.NewCrawlerTextHandlerClient(conn)

	// read crawler info from config file
	configFilePath := cfg.CrawlerConfigFilePath
	crawlerArrayAddress := crawlerUtils.GetCrawlerArrayAddressFromFile(configFilePath)

	// run all crawlers
	var wg sync.WaitGroup
	for i := range crawlerArrayAddress.Crawlers {
		wg.Add(1)
		go func(crawler *crawlerUtils.Crawler) {
			defer wg.Done()
			crawler.Run(&stub)
		}(&crawlerArrayAddress.Crawlers[i])
	}
	wg.Wait() // wait until all crawlers end

	// save changed crawler info
	crawlerUtils.WriteCrawlerInfoToFile(configFilePath, crawlerArrayAddress)
}
