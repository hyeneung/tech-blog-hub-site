package org.datacapstonedesign.backend.service;

import java.util.List;
import org.datacapstonedesign.backend.generated.dto.ResponseDtoBody;

public interface SearchService {
    ResponseDtoBody getPosts(
        final List<String> hashtags,
        final String company,
        final String query,
        final Integer page,
        final Integer size
    );
}
