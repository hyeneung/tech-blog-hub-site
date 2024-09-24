package org.datacapstonedesign.backend.config;

import java.util.List;
import org.datacapstonedesign.backend.interceptor.UserIdHeaderInterceptor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
@Configuration
public class CorsConfig {
    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration corsConfiguration = new CorsConfiguration();
        // TODO - change mydomain.com to real domain name
        corsConfiguration.setAllowedOrigins(List.of("http://localhost:3000", "https://mydomain.com"));
        // Using custom header "X-User-ID" to identify the user with local storage data
        corsConfiguration.setAllowedHeaders(List.of("Content-Type", "Accept", UserIdHeaderInterceptor.CustomHeaderNameForLogging));
        corsConfiguration.setAllowedMethods(List.of("GET"));
        corsConfiguration.setMaxAge(3600L);

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", corsConfiguration);
        return source;
    }
}
