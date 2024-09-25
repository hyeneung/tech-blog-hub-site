package org.datacapstonedesign.backend.repository;

import java.util.Optional;
import org.datacapstonedesign.backend.document.ArticleInfoDocument;
import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;

public interface ArticleInfoRepository extends NativeQueryRepository, ElasticsearchRepository<ArticleInfoDocument, String>{
    Optional<ArticleInfoDocument> findByUrl(String url);
}
