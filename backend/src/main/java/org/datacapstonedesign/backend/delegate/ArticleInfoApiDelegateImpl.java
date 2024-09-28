package org.datacapstonedesign.backend.delegate;

import java.util.List;
import org.datacapstonedesign.backend.generated.api.ArticleInfoApiDelegate;
import org.datacapstonedesign.backend.generated.dto.CompaniesResponse;
import org.datacapstonedesign.backend.generated.dto.SearchResponse;
import org.datacapstonedesign.backend.service.ArticleInfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
public class ArticleInfoApiDelegateImpl implements ArticleInfoApiDelegate {
    private final ArticleInfoService articleInfoService;

    @Autowired
    public ArticleInfoApiDelegateImpl(ArticleInfoService articleInfoService){
        this.articleInfoService = articleInfoService;
    }

    @Override
    public ResponseEntity<SearchResponse> getArticleInfos(
        final String xUserID,
        final List<String> hashtags,
        final String company,
        final String query,
        final Integer page,
        final Integer size
    ) {
        return ResponseEntity.ok(
            new SearchResponse()
                .status(HttpStatus.OK.value())
                .message("ok")
                .content(articleInfoService.getArticleInfosByQueryParams(hashtags, company, query, page, size))
        );
    }

    @Override
    public ResponseEntity<CompaniesResponse> getCompanyNames(final String xUserID) {
        return ResponseEntity.ok(
            new CompaniesResponse()
                .status(HttpStatus.OK.value())
                .message("ok")
                .content(articleInfoService.getCompanyNames())
        );
    }
}
