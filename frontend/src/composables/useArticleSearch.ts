import { ref } from 'vue'
import { useArticleSearchCriteriaStore } from '@/stores/articleSearchCriteriaStore'
import { usePaginationStore } from '@/stores/paginationStore'
import { getApiConfig } from '@/config/api'
import { ArticleInfoApi } from '@/frontend-ts-axios-package'
import type { ApiResult, SearchResponseBody, ArticleInfo } from '@/frontend-ts-axios-package'
import { validateSearchParams } from '@/utils/validation';

export function useArticleSearch() {
  const articles = ref<ArticleInfo[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const searchCriteriaStore = useArticleSearchCriteriaStore()
  const paginationStore = usePaginationStore()

  const api = new ArticleInfoApi(getApiConfig())

  async function fetchArticles() {
    loading.value = true
    error.value = null

    // validation
    const validationError = validateSearchParams({
      hashtags: searchCriteriaStore.hashtags,
      company: searchCriteriaStore.company,
      query: searchCriteriaStore.query,
      page: searchCriteriaStore.page,
      size: searchCriteriaStore.size
    });
    if (validationError) {
      error.value = validationError;
      loading.value = false;
      return;
    }

    try {
      const response = await api.getArticleInfos(
        localStorage.getItem('userId') || undefined,
        searchCriteriaStore.hashtags,
        searchCriteriaStore.company,
        searchCriteriaStore.query,
        searchCriteriaStore.page,
        searchCriteriaStore.size
      )

      const xUserId = response.headers['x-user-id']
      if (xUserId) {
        localStorage.setItem('userId', xUserId)
      }

      const apiResult = response.data as ApiResult
      if (apiResult.status === 200) {
        const searchResponseBody = apiResult.content as SearchResponseBody
        articles.value = searchResponseBody.articleInfos
        paginationStore.setPageInfo(searchResponseBody.page)
      } else {
        error.value = apiResult.message
      }
    } catch (err) {
      console.error('Error fetching data:', err);
      error.value = err instanceof Error ? err.message : 'Error fetching data'
    } finally {
      loading.value = false
    }
  }

  return {
    articles,
    loading,
    error,
    fetchArticles
  }
}