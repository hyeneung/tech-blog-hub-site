package org.datacapstonedesign.backend.exception;

import jakarta.validation.ConstraintViolation;
import jakarta.validation.ConstraintViolationException;
import java.util.List;
import java.util.Map;
import org.datacapstonedesign.backend.generated.dto.ApiResult;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

@RestControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {

    @ExceptionHandler(ConstraintViolationException.class)
    public ResponseEntity<Object> handleConstraintViolationException(
        ConstraintViolationException ex,
        WebRequest request
    ) {
        // TODO - implement logging
        List<String> errors = ex.getConstraintViolations()
            .stream()
            .map(ConstraintViolation::getMessage)
            .toList();

        ApiResult apiResult = new ApiResult()
            .status(HttpStatus.BAD_REQUEST.value())
            .message("Validation failed")
            .content(Map.of("errors", errors));

        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(apiResult);
    }

}
