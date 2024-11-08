package types

type ParsedData struct {
	Data []Post `xml:"channel>item"`
}

type Post struct {
	Title   string `xml:"title"`
	Link    string `xml:"link"`
	PubDate string `xml:"pubDate"`
}

type TextAnalysisResult struct {
	SummarizedText string   `json:"summarized_text"`
	Hashtags       []string `json:"hashtags"`
}
