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
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

@RestControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {

    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(ConstraintViolationException.class)
    public ResponseEntity<Object> handleConstraintViolationException(
        ConstraintViolationException ex,
        WebRequest request
    ) {
        List<String> errors = ex.getConstraintViolations()
            .stream()
            .map(ConstraintViolation::getMessage)
            .toList();

        HttpServletRequest httpRequest = ((ServletRequestAttributes) RequestContextHolder.currentRequestAttributes()).getRequest();
        String userId = (String) httpRequest.getAttribute(UserIdHeaderInterceptor.CustomHeaderNameForLogging);

        logger.error("User ID: {}. Validation failed. Errors: {}",
            userId != null ? userId : "Unknown",
            String.join(", ", errors)
        );

        ApiResult apiResult = new ApiResult()
            .status(HttpStatus.BAD_REQUEST.value())
            .message("Validation failed")
            .content(Map.of("errors", errors));

        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(apiResult);
    }

}
