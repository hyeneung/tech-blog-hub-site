package org.datacapstonedesign.backend.repository.impl;

import co.elastic.clients.elasticsearch._types.FieldValue;
import co.elastic.clients.elasticsearch._types.query_dsl.TermsQuery;
import co.elastic.clients.elasticsearch._types.query_dsl.TermsQuery.Builder;
import co.elastic.clients.util.ObjectBuilder;
import java.util.List;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.datacapstonedesign.backend.document.ArticleInfoDocument;
import org.datacapstonedesign.backend.repository.NativeQueryRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.elasticsearch.client.elc.NativeQuery;
import org.springframework.data.elasticsearch.client.elc.NativeQueryBuilder;
import org.springframework.data.elasticsearch.core.ElasticsearchOperations;
import org.springframework.data.elasticsearch.core.SearchHits;
import org.springframework.data.elasticsearch.core.query.Query;
import org.springframework.stereotype.Repository;
import org.springframework.data.domain.Pageable;

@Repository
public class NativeQueryRepositoryImpl implements NativeQueryRepository {
    private final ElasticsearchOperations elasticsearchOperations;

    @Autowired
    public NativeQueryRepositoryImpl(ElasticsearchOperations elasticsearchOperations) {
        this.elasticsearchOperations = elasticsearchOperations;
    }

    @Override
    public SearchHits<ArticleInfoDocument> findByQueryParams(
        final List<String> hashtags,
        final String company,
        final String query,
        final Pageable pageable
    ) {
        NativeQueryBuilder nativeQueryBuilder = NativeQuery.builder().withPageable(pageable);

        // Use terms query for hashtags
        if (hashtags != null && !hashtags.isEmpty()) {
            Function<Builder, ObjectBuilder<TermsQuery>> termsQuery = termsBuilder -> termsBuilder
                .field("hashtags.keyword")
                .terms(termsValueBuilder -> termsValueBuilder.value(
                    hashtags.stream()
                        .map(FieldValue::of)
                        .collect(Collectors.toList())
                ));

            nativeQueryBuilder.withQuery(q -> q.terms(termsQuery));
        }

        // Company name search logic
        if (company != null && !company.isEmpty()) {
            Function<TermsQuery.Builder, ObjectBuilder<TermsQuery>> termsQuery = termsBuilder -> termsBuilder
                .field("company_name")
                .terms(termsValueBuilder -> termsValueBuilder.value(
                    // Convert the company name of String type to FieldValue type and wrap it in a list
                    List.of(FieldValue.of(company))
                ));

            nativeQueryBuilder.withQuery(q -> q.terms(termsQuery));
        }

        // General search query logic
        if (query != null && !query.isEmpty()) {
            nativeQueryBuilder.withQuery(q -> q.multiMatch(m -> m
                .fields("title", "content")
                .query(query)
            ));
        }

        Query searchQuery = nativeQueryBuilder.build();
        return elasticsearchOperations.search(searchQuery, ArticleInfoDocument.class);
    }
}
