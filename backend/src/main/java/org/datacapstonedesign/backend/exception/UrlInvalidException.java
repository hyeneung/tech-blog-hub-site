package org.datacapstonedesign.backend.exception;

public class UrlInvalidException extends RuntimeException {
    public UrlInvalidException(String message) {
        super(message);
    }

    public UrlInvalidException(String message, Throwable cause) {
        super(message, cause);
    }
}