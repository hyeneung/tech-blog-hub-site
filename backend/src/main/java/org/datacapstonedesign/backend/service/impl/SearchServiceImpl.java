package org.datacapstonedesign.backend.service.impl;

import java.util.List;
import java.util.stream.Collectors;
import org.datacapstonedesign.backend.document.ArticleInfoDocument;
import org.datacapstonedesign.backend.generated.dto.ArticleInfo;
import org.datacapstonedesign.backend.generated.dto.PageInfo;
import org.datacapstonedesign.backend.generated.dto.ResponseDtoBody;
import org.datacapstonedesign.backend.repository.SearchRepository;
import org.datacapstonedesign.backend.service.SearchService;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.elasticsearch.core.SearchHit;
import org.springframework.data.elasticsearch.core.SearchHits;
import org.springframework.stereotype.Service;

@Service
public class SearchServiceImpl implements SearchService {

    private final SearchRepository searchRepository;

    public SearchServiceImpl(SearchRepository searchRepository) {
        this.searchRepository = searchRepository;
    }

    @Override
    public ResponseDtoBody getArticleInfos(
        final List<String> hashtags,
        final String company,
        final String query,
        final Integer page,
        final Integer size
    ) {
        Pageable pageable = PageRequest.of(page, size);

        SearchHits<ArticleInfoDocument> searchHits = searchRepository.findByQueryParams(
            hashtags,
            company,
            query,
            pageable
        );

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

        return new ResponseDtoBody()
            .articleInfos(articleInfos)
            .page(pageInfo);
    }
}
