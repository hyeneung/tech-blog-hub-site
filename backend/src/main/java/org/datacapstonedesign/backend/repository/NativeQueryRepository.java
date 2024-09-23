package org.datacapstonedesign.backend.repository;

import java.util.List;
import org.datacapstonedesign.backend.document.ArticleInfoDocument;
import org.springframework.data.elasticsearch.core.SearchHits;
import org.springframework.data.domain.Pageable;
public interface NativeQueryRepository{
    SearchHits<ArticleInfoDocument> findByQueryParams(
        final List<String> hashtags,
        final String company,
        final String query,
        final Pageable pageable
    );
}
