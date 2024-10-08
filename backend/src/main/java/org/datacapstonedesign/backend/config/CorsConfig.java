package org.datacapstonedesign.backend.config;

import java.util.List;
import org.datacapstonedesign.backend.interceptor.UserIdHeaderInterceptor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;

@Configuration
public class CorsConfig {
    private static final List<String> COMMON_ALLOWED_HEADERS = List.of("Content-Type", "Accept", UserIdHeaderInterceptor.CustomHeaderNameForLogging);
    private static final List<String> COMMON_ALLOWED_METHODS = List.of("GET");
    private static final List<String> EXPOSE_HEADERS = List.of(UserIdHeaderInterceptor.CustomHeaderNameForLogging);
    @Bean
    public CorsFilter corsFilter() {
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        // Apply different CORS configurations based on the API path
        source.registerCorsConfiguration("/api/v1/frontend/**", createFrontendConfig());
        source.registerCorsConfiguration("/api/v1/extension/**", createExtensionConfig());

        return new CorsFilter(source);
    }

    private CorsConfiguration createFrontendConfig() {
        // Configuration for frontend API requests
        // This allows requests from the main web application
        CorsConfiguration config = createBaseConfig();
        config.setAllowedOrigins(List.of(
            "http://localhost:5173",
            "https://my-frontend-domain.com"  // TODO - change mydomain.com to real domain name
        ));
        return config;
    }

    private CorsConfiguration createExtensionConfig() {
        // Configuration for Chrome extension API requests
        // This allows requests only from the specific Chrome extension
        CorsConfiguration config = createBaseConfig();
        config.setAllowedOrigins(List.of(
            "http://localhost:5173",
            "chrome-extension://<my-extension-id>"  // TODO - Replace with actual extension ID
        ));
        return config;
    }

    private CorsConfiguration createBaseConfig() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedHeaders(COMMON_ALLOWED_HEADERS);
        config.setAllowedMethods(COMMON_ALLOWED_METHODS);
        config.setExposedHeaders(EXPOSE_HEADERS);
        return config;
    }
}
