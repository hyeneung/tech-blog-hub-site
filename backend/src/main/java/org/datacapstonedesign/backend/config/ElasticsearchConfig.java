package org.datacapstonedesign.backend.config;

import javax.net.ssl.SSLContext;
import org.apache.http.conn.ssl.TrustAllStrategy;
import org.apache.http.ssl.SSLContextBuilder;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.elasticsearch.client.ClientConfiguration;
import org.springframework.data.elasticsearch.client.elc.ElasticsearchConfiguration;
import org.springframework.lang.NonNull;

@Configuration
public class ElasticsearchConfig extends ElasticsearchConfiguration {

    @Value("${spring.elasticsearch.uris}")
    private String[] elasticsearchUrls;

    @Value("${spring.elasticsearch.username}")
    private String username;

    @Value("${spring.elasticsearch.password}")
    private String password;

    @Override
    public @NonNull ClientConfiguration clientConfiguration() {
        return ClientConfiguration.builder()
            // TODO - connectedTo(elasticsearchUrls)
            .connectedToLocalhost()
            .usingSsl(buildSSLContext())
            .withBasicAuth(username, password)
            .build();
    }
    private SSLContext buildSSLContext() {
        try {
            return new SSLContextBuilder()
                .loadTrustMaterial(null, TrustAllStrategy.INSTANCE)
                .build();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}