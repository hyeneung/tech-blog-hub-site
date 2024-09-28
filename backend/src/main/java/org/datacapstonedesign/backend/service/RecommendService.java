package org.datacapstonedesign.backend.service;

import org.datacapstonedesign.backend.generated.dto.RecommendResponseBody;

public interface RecommendService {
    RecommendResponseBody getRecommend(String url);
}
