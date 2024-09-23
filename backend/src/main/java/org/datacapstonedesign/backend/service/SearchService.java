package org.datacapstonedesign.backend.service;

import java.util.List;
import org.datacapstonedesign.backend.generated.dto.SearchResponseBody;

public interface SearchService {
    SearchResponseBody getArticleInfos(
        final List<String> hashtags,
        final String company,
        final String query,
        final Integer page,
        final Integer size
    );
}
