package model

import "encoding/json"

type SearchResponse struct {
	Status  int     `json:"status"`
	Message string  `json:"message"`
	Content Content `json:"content"`
}

type Content struct {
	ArticleInfos []ArticleInfo `json:"articleInfos"`
	Pageable     Pageable      `json:"page"`
}

type ArticleInfo struct {
	Title          string   `json:"title"`
	PubDate        string   `json:"pubDate"`
	CompanyName    string   `json:"companyName"`
	URL            string   `json:"url"`
	SummarizedText string   `json:"summarizedText"`
	Hashtags       []string `json:"hashtags"`
}

type Pageable struct {
	PageNumber    int `json:"pageNumber"`
	PageSize      int `json:"pageSize"`
	TotalElements int `json:"totalElements"`
	TotalPages    int `json:"totalPages"`
}

func NewErrorResponse(status int, message string) []byte {
	resp, _ := json.Marshal(SearchResponse{Status: status, Message: message, Content: Content{}})
	return resp
}
