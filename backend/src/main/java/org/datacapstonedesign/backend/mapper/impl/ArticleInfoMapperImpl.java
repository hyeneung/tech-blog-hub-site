package org.datacapstonedesign.backend.mapper.impl;

import java.util.List;
import java.util.stream.Collectors;
import org.datacapstonedesign.backend.document.ArticleInfoDocument;
import org.datacapstonedesign.backend.generated.dto.ArticleInfo;
import org.datacapstonedesign.backend.generated.dto.PageInfo;
import org.datacapstonedesign.backend.generated.dto.SearchResponseBody;
import org.datacapstonedesign.backend.mapper.ArticleInfoMapper;
import org.springframework.data.elasticsearch.core.SearchHit;
import org.springframework.data.elasticsearch.core.SearchHits;
import org.springframework.stereotype.Component;

@Component
public class ArticleInfoMapperImpl implements ArticleInfoMapper {

    @Override
    public SearchResponseBody toSearchResponseBody(
        final SearchHits<ArticleInfoDocument> searchHits,
        int page,
        int size
    ) {
        List<ArticleInfo> articleInfos = searchHits.getSearchHits().stream()
            .map(SearchHit::getContent)
            .map(ArticleInfoDocument::toArticleInfo)
            .collect(Collectors.toList());

        long totalHits = searchHits.getTotalHits();
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
