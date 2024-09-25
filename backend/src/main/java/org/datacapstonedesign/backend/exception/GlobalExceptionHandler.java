package org.datacapstonedesign.backend.exception;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.ConstraintViolation;
import jakarta.validation.ConstraintViolationException;
import java.util.List;
import java.util.Map;
import org.datacapstonedesign.backend.generated.dto.ApiResult;
import org.datacapstonedesign.backend.interceptor.UserIdHeaderInterceptor;
import org.datacapstonedesign.backend.util.CustomLogger;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

@RestControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {

    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(ConstraintViolationException.class)
    public ResponseEntity<ApiResult> handleConstraintViolationException(
        ConstraintViolationException ex,
        HttpServletRequest request
    ) {
        List<String> errors = ex.getConstraintViolations()
            .stream()
            .map(ConstraintViolation::getMessage)
            .toList();

        return handleException(new ExceptionContext(ex, request, "Validation", errors.toString(), HttpStatus.BAD_REQUEST, LogLevel.WARN));
    }

    @ExceptionHandler(UrlInvalidException.class)
    public ResponseEntity<ApiResult> handleUrlInvalidException(
        UrlInvalidException ex,
        HttpServletRequest request
    ) {
        return handleException(new ExceptionContext(ex, request, "URL Validation", ex.getMessage(), HttpStatus.BAD_REQUEST, LogLevel.WARN));
    }


    @ExceptionHandler(ElasticsearchIOException.class)
    public ResponseEntity<ApiResult> handleElasticsearchIOException(
        ElasticsearchIOException ex,
        HttpServletRequest request
    ) {
        String detailedError = (ex.getCause() != null) ? ex.getCause().getMessage() : "No additional details available";
        String errorDetails = String.format("Message: %s, Details: {%s}", ex.getMessage(), detailedError);
        return handleException(new ExceptionContext(ex, request, "Elasticsearch I/O operation", errorDetails, HttpStatus.INTERNAL_SERVER_ERROR, LogLevel.ERROR));
    }

    private String getUserId(HttpServletRequest request) {
        return (String) request.getAttribute(UserIdHeaderInterceptor.CustomHeaderNameForLogging);
    }

    private enum LogLevel {
        ERROR, WARN, INFO, DEBUG
    }

    private record ExceptionContext(
        Exception exception,
        HttpServletRequest request,
        String operation,
        String message,
        HttpStatus status,
        LogLevel logLevel
    ) {
    }

    private ResponseEntity<ApiResult> handleException(ExceptionContext context) {
        String userId = getUserId(context.request);

        switch (context.logLevel) {
            case ERROR:
                CustomLogger.logError(logger, context.operation, userId, context.message);
                break;
            case WARN:
                CustomLogger.logWarn(logger, context.operation, userId, context.message);
                break;
        }

        ApiResult apiResult = new ApiResult()
            .status(context.status.value())
            .message(context.operation + " failed")
            .content(Map.of("errors", context.message));
        return ResponseEntity.status(context.status).body(apiResult);
    }
}