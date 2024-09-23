package org.datacapstonedesign.backend.repository;

import org.datacapstonedesign.backend.document.ArticleInfoDocument;
import org.springframework.data.elasticsearch.repository.ElasticsearchRepository;

public interface ArticleInfoRepository extends NativeQueryRepository, ElasticsearchRepository<ArticleInfoDocument, String>{

}
