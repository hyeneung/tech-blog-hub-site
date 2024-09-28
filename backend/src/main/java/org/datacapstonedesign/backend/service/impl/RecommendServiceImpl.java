package org.datacapstonedesign.backend.service.impl;

import java.util.Collections;
import java.util.List;
import org.datacapstonedesign.backend.generated.dto.RecommendResponseBody;
import org.datacapstonedesign.backend.repository.ArticleInfoRepository;
import org.datacapstonedesign.backend.service.RecommendService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class RecommendServiceImpl implements RecommendService {

    private final ArticleInfoRepository articleInfoRepository;
    @Autowired
    public RecommendServiceImpl(ArticleInfoRepository articleInfoRepository) {
        this.articleInfoRepository = articleInfoRepository;
    }

    @Override
    public RecommendResponseBody getRecommend(final String url) {
        return articleInfoRepository.findByUrl(url)
            .map(articleInfo -> new RecommendResponseBody()
                .recommends(List.of("[mock] https://www.a.com", "[mock] https://www.b.com"))
                .summarizedText(articleInfo.summarizedText())
                .hashtags(articleInfo.hashtags()))
            .orElse(new RecommendResponseBody()
                .recommends(Collections.emptyList())
                .summarizedText("")
                .hashtags(Collections.emptyList()));
    }
}
