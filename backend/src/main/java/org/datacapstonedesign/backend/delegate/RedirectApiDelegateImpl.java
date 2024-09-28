package org.datacapstonedesign.backend.delegate;

import java.net.URI;
import org.datacapstonedesign.backend.generated.api.RedirectApiDelegate;
import org.datacapstonedesign.backend.util.UrlValidator;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
public class RedirectApiDelegateImpl implements RedirectApiDelegate {

    @Override
    public ResponseEntity<Void> redirectToUrl(
        final String url,
        final String xUserID
    ) {
        UrlValidator.validateHttpUrl(url);
        HttpHeaders headers = new HttpHeaders();
        headers.setLocation(URI.create(url));
        return new ResponseEntity<>(headers, HttpStatus.FOUND);
    }
}
