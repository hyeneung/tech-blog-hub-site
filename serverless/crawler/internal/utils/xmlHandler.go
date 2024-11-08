package utils

import (
	"encoding/xml"
	"fmt"
	"io"
	"net/http"

	types "crawler/internal/types"
)

func GetPostArrayFromUrl(url string) ([]types.Post, error) {
	logger := GetLoggerSingletonInstance()
	client := &http.Client{}
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		logger.LogError(err.Error())
		return nil, err
	}
	req.Header.Set("Referer", "https://tech-blog-hub.com")
	req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
	res, err := client.Do(req)
	if err != nil {
		logger.LogError(err.Error())
		return nil, err
	}
	if res.StatusCode != http.StatusOK {
		logger.LogHttpResponseError(res)
		return nil, fmt.Errorf("failed to parse XML")
	}
	defer res.Body.Close()

	data, err := io.ReadAll(res.Body)
	if err != nil {
		logger.LogError(err.Error())
		return nil, err
	}
	var posts types.ParsedData
	xmlerr := xml.Unmarshal(data, &posts)
	if xmlerr != nil {
		logger.LogError(xmlerr.Error())
		return nil, xmlerr
	}

	return posts.Data, nil
}
