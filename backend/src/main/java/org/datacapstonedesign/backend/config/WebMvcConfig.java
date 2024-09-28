package org.datacapstonedesign.backend.config;

import org.datacapstonedesign.backend.interceptor.UserIdHeaderInterceptor;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * Configuration class for registering custom interceptors.
 * This class sets up the UserIdHeaderInterceptor to be applied to all incoming requests.
 */
@Configuration
public class WebMvcConfig implements WebMvcConfigurer {

    private final UserIdHeaderInterceptor userIdHeaderInterceptor;

    public WebMvcConfig(UserIdHeaderInterceptor userIdHeaderInterceptor) {
        this.userIdHeaderInterceptor = userIdHeaderInterceptor;
    }

    /**
     * Adds the UserIdHeaderInterceptor to the interceptor registry.
     * This method is called by Spring to configure interceptors.
     *
     * @param registry The InterceptorRegistry to which we add our custom interceptor
     */
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(userIdHeaderInterceptor)
            .addPathPatterns("/**");  // Apply to all paths
    }
}