package org.datacapstonedesign.backend.service.impl;

import java.util.List;
import java.util.stream.Collectors;
import org.datacapstonedesign.backend.document.ArticleInfoDocument;
import org.datacapstonedesign.backend.generated.dto.ArticleInfo;
import org.datacapstonedesign.backend.generated.dto.PageInfo;
import org.datacapstonedesign.backend.generated.dto.SearchResponseBody;
import org.datacapstonedesign.backend.repository.ArticleInfoRepository;
import org.datacapstonedesign.backend.service.ArticleInfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.elasticsearch.core.SearchHit;
import org.springframework.data.elasticsearch.core.SearchHits;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class ArticleInfoServiceImpl implements ArticleInfoService {

    private final ArticleInfoRepository articleInfoRepository;
    @Autowired
    public ArticleInfoServiceImpl(ArticleInfoRepository articleInfoRepository) {
        this.articleInfoRepository = articleInfoRepository;
    }
    @Transactional(readOnly = true)
    @Override
    public SearchResponseBody getArticleInfos(
        final List<String> hashtags,
        final String company,
        final String query,
        final Integer page,
        final Integer size
    ) {
        SearchHits<ArticleInfoDocument> searchHits = articleInfoRepository.findByQueryParams(
            hashtags,
            company,
            query,
            PageRequest.of(page, size)
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

        return new SearchResponseBody()
            .articleInfos(articleInfos)
            .page(pageInfo);
    }
}
