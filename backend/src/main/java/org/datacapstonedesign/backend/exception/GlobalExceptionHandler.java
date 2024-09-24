package org.datacapstonedesign.backend.exception;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.ConstraintViolation;
import jakarta.validation.ConstraintViolationException;
import java.util.List;
import java.util.Map;
import org.datacapstonedesign.backend.generated.dto.ApiResult;
import org.datacapstonedesign.backend.interceptor.UserIdHeaderInterceptor;
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
        HttpServletRequest httpServletRequest
    ) {
        List<String> errors = ex.getConstraintViolations()
            .stream()
            .map(ConstraintViolation::getMessage)
            .toList();

        String userId = (String) httpServletRequest.getAttribute(UserIdHeaderInterceptor.CustomHeaderNameForLogging);

        logger.error("Validation failed. User ID: {}, Errors: {}",
            userId != null ? userId : "Unknown",
            String.join(", ", errors)
        );

        ApiResult apiResult = new ApiResult()
            .status(HttpStatus.BAD_REQUEST.value())
            .message("Validation failed")
            .content(Map.of("errors", errors));

        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(apiResult);
    }

    @ExceptionHandler(ElasticsearchIOException.class)
    public ResponseEntity<ApiResult> handleElasticsearchIOException(
        ElasticsearchIOException ex,
        HttpServletRequest httpServletRequest
    ) {
        String errorMessage = ex.getMessage();
        String detailedError = (ex.getCause() != null) ? ex.getCause().getMessage() : "No additional details available";

        String userId = (String) httpServletRequest.getAttribute(UserIdHeaderInterceptor.CustomHeaderNameForLogging);

        Map<String, String> errorDetails = Map.of(
            "message", errorMessage,
            "details", detailedError
        );

        logger.error("Elasticsearch I/O operation failed. User ID: {}, Errors: {}",
            userId != null ? userId : "Unknown",
            errorDetails
        );

        ApiResult apiResult = new ApiResult()
            .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
            .message("Elasticsearch I/O operation failed")
            .content(Map.of("errors", errorDetails));
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(apiResult);
    }

}
