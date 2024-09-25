package org.datacapstonedesign.backend.util;

import java.net.MalformedURLException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import org.datacapstonedesign.backend.exception.UrlInvalidException;

public class UrlValidator {
    private static final String[] ALLOWED_PROTOCOLS = {"http", "https"};
    private static final int MAX_URL_LENGTH = 2000;

    private UrlValidator() {
        // Utility class, hide constructor
    }

    public static boolean isValidHttpUrl(String url) {
        if (url == null || url.isEmpty() || url.length() > MAX_URL_LENGTH) {
            return false;
        }

        try {
            new URI(url);
            URL u = new URL(url);
            return isAllowedProtocol(u.getProtocol()) && !containsXssPayload(url);
        } catch (URISyntaxException | MalformedURLException e) {
            return false;
        }
    }

    public static void validateHttpUrl(String url) throws UrlInvalidException {
        if (!isValidHttpUrl(url)) {
            throw new UrlInvalidException("Invalid HTTP URL: " + url);
        }
    }

    private static boolean isAllowedProtocol(String protocol) {
        for (String allowedProtocol : ALLOWED_PROTOCOLS) {
            if (allowedProtocol.equalsIgnoreCase(protocol)) {
                return true;
            }
        }
        return false;
    }

    private static boolean containsXssPayload(String url) {
        String lowercaseUrl = url.toLowerCase();
        return lowercaseUrl.contains("<script>") ||
            lowercaseUrl.contains("javascript:") ||
            lowercaseUrl.contains("data:") ||
            lowercaseUrl.contains("vbscript:") ||
            lowercaseUrl.contains("onload=") ||
            lowercaseUrl.contains("onerror=");
    }
}
