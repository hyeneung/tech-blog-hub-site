package org.datacapstonedesign.backend.service.impl;

import co.elastic.clients.elasticsearch.core.SearchResponse;
import java.io.IOException;
import java.util.List;
import org.datacapstonedesign.backend.document.ArticleInfoDocument;
import org.datacapstonedesign.backend.exception.ElasticsearchIOException;
import org.datacapstonedesign.backend.generated.dto.CompaniesResponseBody;
import org.datacapstonedesign.backend.generated.dto.SearchResponseBody;
import org.datacapstonedesign.backend.mapper.ArticleInfoMapper;
import org.datacapstonedesign.backend.repository.ArticleInfoRepository;
import org.datacapstonedesign.backend.service.ArticleInfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
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
    public SearchResponseBody getArticleInfosByQueryParams(
        final List<String> hashtags,
        final String company,
        final String query,
        final Integer page,
        final Integer size
    ) {
        try {
            SearchResponse<ArticleInfoDocument> searchResponse = articleInfoRepository.findByQueryParams(
                hashtags,
                company,
                query,
                PageRequest.of(page, size)
            );
            return articleInfoMapper.toSearchResponseBody(searchResponse, page, size);
        } catch (IOException e){
            throw new ElasticsearchIOException("Failed to fetch results for user query", e);
        }
    }
    @Transactional(readOnly = true)
    @Override
    public CompaniesResponseBody getCompanyNames(){
        try {
            SearchResponse<Void> searchResponse = articleInfoRepository.findAllUniqueCompanyNames();
            return articleInfoMapper.toCompaniesResponseBody(searchResponse);
        } catch (IOException e) {
            throw new ElasticsearchIOException("Failed to fetch company names", e);
        }
    }
}
