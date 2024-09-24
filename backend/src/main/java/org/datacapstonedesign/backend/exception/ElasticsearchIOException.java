package org.datacapstonedesign.backend.exception;

public class ElasticsearchIOException extends RuntimeException {
    public ElasticsearchIOException(String message){
        super(message);
    }

    public ElasticsearchIOException(String message, Throwable cause) {
        super(message, cause);
    }
}
