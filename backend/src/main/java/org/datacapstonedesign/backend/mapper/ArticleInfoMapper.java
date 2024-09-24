package org.datacapstonedesign.backend.mapper;

import org.datacapstonedesign.backend.document.ArticleInfoDocument;
import org.datacapstonedesign.backend.generated.dto.SearchResponseBody;
import org.springframework.data.elasticsearch.core.SearchHits;

public interface ArticleInfoMapper {
    SearchResponseBody toSearchResponseBody(
        SearchHits<ArticleInfoDocument> searchHits,
        int page,
        int size
    );
}
