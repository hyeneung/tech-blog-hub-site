package org.datacapstonedesign.backend.interceptor;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import com.fasterxml.uuid.Generators;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

@Component
public class UserIdHeaderInterceptor implements HandlerInterceptor {

    public static final String CustomHeaderNameForLogging = "X-User-ID";

    /**
     * This method is part of the HandlerInterceptor interface and is executed before the actual handler method.
     * It runs before any AOP logging aspects and controller methods.
     *
     * Execution order:
     * 1. Interceptor's preHandle method (this method)
     * 2. AOP aspects (e.g., logging aspects)
     * 3. Controller method
     *
     * This makes it ideal for tasks that need to be performed at the very beginning of request processing,
     * such as setting up request-scoped resources or performing initial request validation.
     */
    @Override
    public boolean preHandle(
        HttpServletRequest request,
        HttpServletResponse response,
        Object handler
    ) {
        String userId = request.getHeader(CustomHeaderNameForLogging);
        if (userId == null || userId.isEmpty()) {
            userId = Generators.timeBasedGenerator().generate().toString();
        }
        // Set the User ID as a request attribute for logging in AOP
        // This allows the AOP logging aspect to access the User ID
        request.setAttribute(CustomHeaderNameForLogging, userId);

        // Set the User ID in the response header
        // This allows the client to use it in subsequent requests
        response.setHeader(CustomHeaderNameForLogging, userId);
        return true;
    }
}