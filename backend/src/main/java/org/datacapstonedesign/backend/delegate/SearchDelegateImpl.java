package org.datacapstonedesign.backend.delegate;

import java.util.List;
import org.datacapstonedesign.backend.generated.api.SearchApiDelegate;
import org.datacapstonedesign.backend.generated.dto.ResponseDto;
import org.datacapstonedesign.backend.service.SearchService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
public class SearchDelegateImpl implements SearchApiDelegate {
    private final SearchService searchService;

    @Autowired
    public SearchDelegateImpl(SearchService searchService){
        this.searchService = searchService;
    }

    @Override
    public ResponseEntity<ResponseDto> getPosts(
        final List<String> hashtags,
        final String company,
        final String query,
        final Integer page,
        final Integer size
    ) {
        return ResponseEntity.ok(
            new ResponseDto()
                .status(200)
                .message("ok")
                .responseDtoBody(searchService.getPosts(hashtags, company, query, page, size))
        );
    }
}
