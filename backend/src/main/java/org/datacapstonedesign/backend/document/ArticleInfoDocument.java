package org.datacapstonedesign.backend.document;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import org.datacapstonedesign.backend.generated.dto.ArticleInfo;
import org.springframework.data.annotation.Id;
import org.springframework.data.elasticsearch.annotations.Document;
import org.springframework.data.elasticsearch.annotations.Field;

@Document(indexName = "#{@environment.getProperty('spring.elasticsearch.index.name')}")
public record ArticleInfoDocument(
    @JsonProperty("id")
    @Id
    String id,
    @JsonProperty("title")
    String title,
    @JsonProperty("pub_date")
    @Field(name = "pub_date")
    String pubDate,
    @JsonProperty("company_name")
    @Field(name = "company_name")
    String companyName,
    @JsonProperty("url")
    String url,
    @JsonProperty("content")
    String content,
    @JsonProperty("summarized_text")
    @Field(name = "summarized_text")
    String summarizedText,
    @JsonProperty("hashtags")
    List<String> hashtags
) {
    public static ArticleInfo toArticleInfo(ArticleInfoDocument articleInfoDocument) {
        return new ArticleInfo(
            articleInfoDocument.title(),
            articleInfoDocument.pubDate(),
            articleInfoDocument.companyName(),
            articleInfoDocument.url(),
            articleInfoDocument.summarizedText(),
            articleInfoDocument.hashtags()
        );
    }
}