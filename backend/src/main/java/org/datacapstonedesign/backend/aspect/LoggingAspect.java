package org.datacapstonedesign.backend.aspect;

import jakarta.servlet.http.HttpServletRequest;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.datacapstonedesign.backend.interceptor.UserIdHeaderInterceptor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;


/**
 * This aspect is responsible for logging incoming requests and outgoing responses
 * for all controller methods in the application.
 */
@Aspect
@Component
public class LoggingAspect {

    private static final Logger logger = LoggerFactory.getLogger(LoggingAspect.class);

    // This pointcut applies to the execution of all methods in all classes within the package and its subpackages
    @Pointcut("execution(* org.datacapstonedesign.backend.generated.api..*.*(..))")
    public void controllerPointcut() {}

    /**
     * Around advice that logs information before and after the execution of controller methods.
     * This advice is applied to all methods matched by the controllerPointcut().
     *
     * @param joinPoint Provides access to the executed method and allows proceeding with the method execution
     * @return The result of the method execution
     * @throws Throwable If any exception occurs during the method execution
     */
    @Around("controllerPointcut()")
    public Object logControllerExecution(ProceedingJoinPoint joinPoint) throws Throwable {
        // prevent duplicated log : ArticleInfosApi.getArticleInfos calls ArticleInfoApiDelegateImpl.getArticleInfos
        if (joinPoint.getSignature().getDeclaringType().getSimpleName().endsWith("Api")) {
            ServletRequestAttributes attributes = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
            HttpServletRequest request = attributes.getRequest();

            String userId = (String) request.getAttribute(UserIdHeaderInterceptor.CustomHeaderNameForLogging);
            String method = request.getMethod();
            String uri = request.getRequestURI();
            String queryString = request.getQueryString();

            logger.info("User ID: {}. Request: {} {}{}",
                userId != null ? userId : "Not provided",
                method,
                uri,
                queryString != null ? "?" + queryString : ""
            );

            long startTime = System.currentTimeMillis();
            // Execute the controller method
            Object result = joinPoint.proceed();
            long endTime = System.currentTimeMillis();

            logger.info("User ID: {}. Response: {} {} ({}ms)",
                userId != null ? userId : "Not provided",
                method,
                uri,
                endTime - startTime
            );
            return result;
        }
        return joinPoint.proceed();
    }
}