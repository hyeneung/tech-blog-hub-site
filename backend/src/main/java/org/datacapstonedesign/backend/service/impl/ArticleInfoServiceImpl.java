package org.datacapstonedesign.backend.service.impl;

import java.util.List;
import org.datacapstonedesign.backend.document.ArticleInfoDocument;
import org.datacapstonedesign.backend.generated.dto.SearchResponseBody;
import org.datacapstonedesign.backend.mapper.ArticleInfoMapper;
import org.datacapstonedesign.backend.repository.ArticleInfoRepository;
import org.datacapstonedesign.backend.service.ArticleInfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.elasticsearch.core.SearchHits;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class ArticleInfoServiceImpl implements ArticleInfoService {

    private final ArticleInfoRepository articleInfoRepository;
    private final ArticleInfoMapper articleInfoMapper;
    @Autowired
    public ArticleInfoServiceImpl(
        ArticleInfoRepository articleInfoRepository,
        ArticleInfoMapper articleInfoMapper
    ) {
        this.articleInfoRepository = articleInfoRepository;
        this.articleInfoMapper = articleInfoMapper;
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

        return articleInfoMapper.toSearchResponseBody(searchHits, page, size);
    }
}
