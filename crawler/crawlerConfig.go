package main

import (
	"io"
	"log"
	"os"

	"gopkg.in/yaml.v2"
)

func getCrawlerArrayAddressFromFile(filePath string) *CrawlerArray {
	file, err := os.Open(filePath)
	if err != nil {
		log.Fatalf("error opening file: %v", err)
	}
	defer file.Close()

	var data []byte
	data, err = io.ReadAll(file)
	if err != nil {
		log.Fatalf("error reading file: %v", err)
	}

	var crawlerArray CrawlerArray
	err = yaml.Unmarshal(data, &crawlerArray)
	if err != nil {
		log.Fatalf("error unmarshalling YAML: %v", err)
	}
	return &crawlerArray
}

func writeCrawlerInfoToFile(filePath string, crawlerArrayPointer *CrawlerArray) {
	yamlData, err := yaml.Marshal(&crawlerArrayPointer)
	if err != nil {
		log.Fatalf("error marshalling YAML: %v", err)
	}

	file, err := os.OpenFile(filePath, os.O_WRONLY|os.O_TRUNC, 0644)
	if err != nil {
		log.Fatalf("error opening file for writing: %v", err)
	}
	defer file.Close()

	_, err = file.Write(yamlData)
	if err != nil {
		log.Fatalf("error writing file: %v", err)
	}
}
