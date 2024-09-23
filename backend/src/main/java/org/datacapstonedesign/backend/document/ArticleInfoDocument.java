package org.datacapstonedesign.backend.document;

import java.util.List;
import org.datacapstonedesign.backend.generated.dto.ArticleInfo;
import org.springframework.data.annotation.Id;
import org.springframework.data.elasticsearch.annotations.Document;
import org.springframework.data.elasticsearch.annotations.Field;

@Document(indexName = "#{@environment.getProperty('spring.elasticsearch.index.name')}")
public record ArticleInfoDocument(
    @Id
    String id,

    String title,

    @Field(name = "pub_date")
    String pubDate,

    @Field(name = "company_name")
    String companyName,

    String url,

    String content,

    @Field(name = "summarized_text")
    String summarizedText,

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