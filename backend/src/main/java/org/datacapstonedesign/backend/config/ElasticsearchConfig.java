package org.datacapstonedesign.backend.config;

import java.io.IOException;
import java.io.InputStream;
import java.security.cert.CertificateException;
import java.security.cert.CertificateFactory;
import java.security.cert.X509Certificate;
import java.util.Arrays;
import javax.net.ssl.SSLContext;
import org.apache.http.ssl.SSLContextBuilder;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import org.springframework.data.elasticsearch.client.ClientConfiguration;
import org.springframework.data.elasticsearch.client.elc.ElasticsearchConfiguration;
import org.springframework.lang.NonNull;

@Configuration
public class ElasticsearchConfig extends ElasticsearchConfiguration {

    @Value("${spring.elasticsearch.uris}")
    private String elasticsearchUrl;

    @Value("${spring.elasticsearch.username}")
    private String username;

    @Value("${spring.elasticsearch.password}")
    private String password;

    @Override
    public @NonNull ClientConfiguration clientConfiguration() {
        try {
            Resource certResource = new ClassPathResource("certs/elasticsearch.crt");
            X509Certificate cert = loadX509Certificate(certResource);
            SSLContext sslContext = SSLContextBuilder.create()
                .loadTrustMaterial(null, (chain, authType) -> Arrays.asList(chain).contains(cert))
                .build();

            return ClientConfiguration.builder()
                .connectedTo(elasticsearchUrl.replace("https://", ""))
                .usingSsl(sslContext)
                .withBasicAuth(username, password)
                .build();
        } catch (Exception e) {
            throw new RuntimeException("Failed to configure Elasticsearch client", e);
        }
    }

    private X509Certificate loadX509Certificate(Resource resource) throws CertificateException, IOException {
        try (InputStream inputStream = resource.getInputStream()) {
            CertificateFactory factory = CertificateFactory.getInstance("X.509");
            return (X509Certificate) factory.generateCertificate(inputStream);
        }
    }
}