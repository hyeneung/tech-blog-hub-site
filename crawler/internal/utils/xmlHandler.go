package utils

import (
	"encoding/xml"
	"fmt"
	"io"
	"net/http"

	types "crawler/internal/types"
)

func GetPostArrayFromUrl(url string) ([]types.Post, error) {
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
	var posts types.ParsedData
	xmlerr := xml.Unmarshal(data, &posts)
	if xmlerr != nil {
		GetLoggerSingletonInstance().LogError(xmlerr.Error())
		return nil, xmlerr
	}

	return posts.Data, nil
}
