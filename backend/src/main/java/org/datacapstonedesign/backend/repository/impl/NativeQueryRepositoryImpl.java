package org.datacapstonedesign.backend.repository.impl;

import co.elastic.clients.elasticsearch.ElasticsearchClient;
import co.elastic.clients.elasticsearch._types.FieldValue;
import co.elastic.clients.elasticsearch._types.SortOrder;
import co.elastic.clients.elasticsearch._types.query_dsl.BoolQuery;
import co.elastic.clients.elasticsearch._types.query_dsl.MultiMatchQuery;
import co.elastic.clients.elasticsearch._types.query_dsl.Operator;
import co.elastic.clients.elasticsearch._types.query_dsl.TermQuery;
import co.elastic.clients.elasticsearch._types.query_dsl.TermsQuery;
import co.elastic.clients.elasticsearch._types.query_dsl.TermsQueryField;
import co.elastic.clients.elasticsearch._types.query_dsl.TextQueryType;
import co.elastic.clients.elasticsearch.core.SearchRequest;
import co.elastic.clients.elasticsearch.core.SearchResponse;
import java.io.IOException;
import java.util.List;
import org.datacapstonedesign.backend.document.ArticleInfoDocument;
import org.datacapstonedesign.backend.repository.NativeQueryRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Repository;

@Repository
public class NativeQueryRepositoryImpl implements NativeQueryRepository {
    @Value("${spring.elasticsearch.index.name}")
    private String indexName;
    private final ElasticsearchClient elasticsearchClient;

    @Autowired
    public NativeQueryRepositoryImpl(ElasticsearchClient elasticsearchClient) {
        this.elasticsearchClient = elasticsearchClient;
    }

    @Override
    public SearchResponse<ArticleInfoDocument> findByQueryParams(
        final List<String> hashtags,
        final String company,
        final String query,
        final Pageable pageable
    ) throws IOException {
        BoolQuery.Builder boolQueryBuilder = new BoolQuery.Builder();

        // Hashtags query
        if (hashtags != null && !hashtags.isEmpty()) {
            for (String hashtag : hashtags) {
                TermQuery hashtagQuery = TermQuery.of(t -> t
                    .field("hashtags.keyword")
                    .value(hashtag)
                );
                boolQueryBuilder.must(m -> m.term(hashtagQuery));
            }
        }

        // Company name query
        if (company != null && !company.isEmpty()) {
            TermQuery companyQuery = TermQuery.of(t -> t
                .field("company_name")
                .value(company)
            );
            boolQueryBuilder.must(m -> m.term(companyQuery));
        }

        // General search query
        if (query != null && !query.isEmpty()) {
            MultiMatchQuery multiMatchQuery = MultiMatchQuery.of(m -> m
                .fields("title^3", "summarized_text^2", "hashtags")
                .query(query)
                .type(TextQueryType.BestFields)
                .operator(Operator.Or)
                .fuzziness("AUTO")
                .prefixLength(3)
                .maxExpansions(10)
            );
            boolQueryBuilder.must(m -> m.multiMatch(multiMatchQuery));
        }

        // Build the search request
        SearchRequest searchRequest = SearchRequest.of(s -> s
            .index(indexName)
            .query(q -> q.bool(boolQueryBuilder.build()))
            .from(pageable.getPageNumber() * pageable.getPageSize())
            .size(pageable.getPageSize())
            .sort(sort -> sort
                .field(f -> f
                    .field("pub_date")
                    .order(SortOrder.Desc)
                )
            )
        );

        return elasticsearchClient.search(searchRequest, ArticleInfoDocument.class);
    }
}
