<template>
  <section class="post-container">
    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="error-message" role="alert">{{ error }}</div>
    <div v-else-if="noResults" class="no-results-message">
      검색 결과를 찾을 수 없습니다. 다른 검색어나 필터를 시도해보세요.
    </div>
    <template v-else>
      <Post v-for="post in posts" :key="post.title" :post="post" />
    </template>
  </section>
</template>
  
<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import Post from './Post.vue'
import { useArticleSearch } from '@/composables/useArticleSearch'
import { useArticleSearchCriteriaStore } from '@/stores/articleSearchCriteriaStore'
import type { ArticleInfo } from '@/frontend-ts-axios-package'

const { articles, loading, error, noResults, fetchArticles } = useArticleSearch()
const searchCriteriaStore = useArticleSearchCriteriaStore()

const posts = ref<ArticleInfo[]>([])

onMounted(() => {
  searchCriteriaStore.loadFromLocalStorage()
})

// Fetch articles whenever search criteria changes
watch(() => searchCriteriaStore.currentCriteria, fetchArticles, { deep: true })

// Update posts when search results change
watch(articles, (newArticles) => {
  posts.value = newArticles
})
</script>
  
<style scoped>
.post-container {
  max-width: 60rem;
  margin: 0 auto;
  padding: 0 1rem;
}
.error-message {
  color: #721c24;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}
</style>