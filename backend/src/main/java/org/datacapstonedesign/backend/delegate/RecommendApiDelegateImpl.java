package org.datacapstonedesign.backend.delegate;

import org.datacapstonedesign.backend.generated.api.RecommendApiDelegate;
import org.datacapstonedesign.backend.generated.dto.RecommendResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
public class RecommendApiDelegateImpl implements RecommendApiDelegate {

    @Override
    public ResponseEntity<RecommendResponse> recommendOtherArticles(
        final String xUserID,
        final String url
    ) {
        // TODO - implement concrete functionality
        return RecommendApiDelegate.super.recommendOtherArticles(xUserID, url);
    }
}
