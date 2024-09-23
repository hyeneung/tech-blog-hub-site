package org.datacapstonedesign.backend.delegate;

import java.net.URI;
import org.datacapstonedesign.backend.generated.api.RedirectApiDelegate;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
public class RedirectApiDelegateImpl implements RedirectApiDelegate {

    @Override
    public ResponseEntity<Void> redirectToUrl(
        final String xUserID,
        final String url
    ) {
        // TODO - implement logging
        HttpHeaders headers = new HttpHeaders();
        headers.setLocation(URI.create(url));
        return new ResponseEntity<>(headers, HttpStatus.FOUND);
    }
}
