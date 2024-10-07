package org.datacapstonedesign.backend.mapper;

import co.elastic.clients.elasticsearch.core.SearchResponse;
import org.datacapstonedesign.backend.document.ArticleInfoDocument;
import org.datacapstonedesign.backend.generated.dto.SearchResponseBody;

public interface ArticleInfoMapper {
    SearchResponseBody toSearchResponseBody(
        SearchResponse<ArticleInfoDocument> searchResponse,
        int page,
        int size
    );
}
