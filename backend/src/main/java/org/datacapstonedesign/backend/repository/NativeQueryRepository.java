package org.datacapstonedesign.backend.repository;

import co.elastic.clients.elasticsearch.core.SearchResponse;
import java.io.IOException;
import java.util.List;
import org.datacapstonedesign.backend.document.ArticleInfoDocument;
import org.springframework.data.domain.Pageable;
public interface NativeQueryRepository{
    SearchResponse<ArticleInfoDocument> findByQueryParams(
        final List<String> hashtags,
        final String company,
        final String query,
        final Pageable pageable
    ) throws IOException;
}
