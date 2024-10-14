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
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedHeaders(COMMON_ALLOWED_HEADERS);
        config.setAllowedMethods(COMMON_ALLOWED_METHODS);
        config.setExposedHeaders(EXPOSE_HEADERS);
        config.setAllowedOrigins(List.of(
            "http://localhost:5173",
            "https://www.tech-blog-hub.site",
            "chrome-extension://<my-extension-id>"  // TODO - Replace with actual extension ID
        ));

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/api/v1/**", config);
        return new CorsFilter(source);
    }
}
