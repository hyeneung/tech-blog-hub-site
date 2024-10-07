package org.datacapstonedesign.backend.mapper.impl;

import co.elastic.clients.elasticsearch.core.SearchResponse;
import co.elastic.clients.elasticsearch.core.search.Hit;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import org.datacapstonedesign.backend.document.ArticleInfoDocument;
import org.datacapstonedesign.backend.generated.dto.ArticleInfo;
import org.datacapstonedesign.backend.generated.dto.PageInfo;
import org.datacapstonedesign.backend.generated.dto.SearchResponseBody;
import org.datacapstonedesign.backend.mapper.ArticleInfoMapper;
import org.springframework.stereotype.Component;

@Component
public class ArticleInfoMapperImpl implements ArticleInfoMapper {

    @Override
    public SearchResponseBody toSearchResponseBody(
        SearchResponse<ArticleInfoDocument> searchResponse,
        int page,
        int size
    ) {
        List<ArticleInfo> articleInfos = searchResponse.hits().hits().stream()
            .map(Hit::source)
            .filter(Objects::nonNull)
            .map(ArticleInfoDocument::toArticleInfo)
            .collect(Collectors.toList());

        long totalHits = searchResponse.hits().total().value();
        int totalPages = (int) Math.ceil((double) totalHits / size);

        PageInfo pageInfo = new PageInfo()
            .pageNumber(page)
            .pageSize(size)
            .totalElements((int) totalHits)
            .totalPages(totalPages);

        return new SearchResponseBody()
            .articleInfos(articleInfos)
            .page(pageInfo);
    }
}
