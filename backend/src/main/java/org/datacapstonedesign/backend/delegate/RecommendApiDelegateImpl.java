package org.datacapstonedesign.backend.delegate;

import org.datacapstonedesign.backend.generated.api.RecommendApiDelegate;
import org.datacapstonedesign.backend.generated.dto.RecommendResponse;
import org.datacapstonedesign.backend.service.RecommendService;
import org.datacapstonedesign.backend.util.UrlValidator;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
public class RecommendApiDelegateImpl implements RecommendApiDelegate {

    private final RecommendService recommendService;
    @Autowired
    public RecommendApiDelegateImpl(RecommendService recommendService) {
        this.recommendService = recommendService;
    }
    @Override
    public ResponseEntity<RecommendResponse> recommendOtherArticles(
        final String url,
        final String xUserID
    ) {
        UrlValidator.validateHttpUrl(url);
        return ResponseEntity.ok(
            new RecommendResponse()
                .status(HttpStatus.OK.value())
                .message("ok")
                .content(recommendService.getRecommend(url))
        );
    }
}
