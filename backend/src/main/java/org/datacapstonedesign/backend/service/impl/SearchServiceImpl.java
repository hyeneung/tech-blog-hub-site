package org.datacapstonedesign.backend.service.impl;

import co.elastic.clients.elasticsearch._types.FieldValue;
import co.elastic.clients.elasticsearch._types.query_dsl.TermsQuery;
import co.elastic.clients.util.ObjectBuilder;
import java.util.List;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.datacapstonedesign.backend.document.ArticleInfoDocument;
import org.datacapstonedesign.backend.generated.dto.ArticleInfo;
import org.datacapstonedesign.backend.generated.dto.PageInfo;
import org.datacapstonedesign.backend.generated.dto.ResponseDtoBody;
import org.datacapstonedesign.backend.service.SearchService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.elasticsearch.client.elc.NativeQuery;
import org.springframework.data.elasticsearch.client.elc.NativeQueryBuilder;
import org.springframework.data.elasticsearch.core.ElasticsearchOperations;
import org.springframework.data.elasticsearch.core.SearchHit;
import org.springframework.data.elasticsearch.core.SearchHits;
import org.springframework.data.elasticsearch.core.query.Query;
import org.springframework.stereotype.Service;

@Service
public class SearchServiceImpl implements SearchService {
    private final ElasticsearchOperations elasticsearchOperations;

    @Autowired
    public SearchServiceImpl(ElasticsearchOperations elasticsearchOperations) {
        this.elasticsearchOperations = elasticsearchOperations;
    }

    @Override
    public ResponseDtoBody getPosts(
        final List<String> hashtags,
        final String company,
        final String query,
        final Integer page,
        final Integer size
    ) {
        Pageable pageable = PageRequest.of(page, size);

        NativeQueryBuilder nativeQueryBuilder = NativeQuery.builder().withPageable(pageable);

        // Use terms query for hashtags
        if (hashtags != null && !hashtags.isEmpty()) {
            Function<TermsQuery.Builder, ObjectBuilder<TermsQuery>> termsQuery = termsBuilder -> termsBuilder
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

        SearchHits<ArticleInfoDocument> searchHits = elasticsearchOperations.search(searchQuery, ArticleInfoDocument.class);

        List<ArticleInfo> articleInfos = searchHits.getSearchHits().stream()
            .map(SearchHit::getContent)
            .map(ArticleInfoDocument::toArticleInfo)
            .collect(Collectors.toList());

        long totalHits = searchHits.getTotalHits();
        int totalPages = (int) Math.ceil((double) totalHits / size);

        PageInfo pageInfo = new PageInfo()
            .pageNumber(page)
            .pageSize(size)
            .totalElements((int) totalHits)
            .totalPages(totalPages);

        return new ResponseDtoBody()
            .articleInfos(articleInfos)
            .page(pageInfo);
    }
}
