<template>
  <article class="post">
    <div @click="handlePostClick" class="post-content">
      <PostInfo :post="post" />
      <PostSummary :post="post" />
    </div>
  </article>
</template>

<script setup lang="ts">
import PostInfo from './PostInfo.vue'
import PostSummary from './PostSummary.vue'
import type { ArticleInfo } from '@/frontend-ts-axios-package'
import { useArticleSearchCriteriaStore } from '@/stores/articleSearchCriteriaStore'

const props = defineProps<{
  post: ArticleInfo
}>()

const searchCriteriaStore = useArticleSearchCriteriaStore()

const handlePostClick = async (event: MouseEvent) => {

  // If the clicked element is a child of an element with the 'summary-toggle' class, do not process the event
  if ((event.target as HTMLElement).closest('.summary-toggle')) {
    event.preventDefault()
    return
  }

  // send to Google Analytics
  window.dataLayer.push({
    'event': 'post_click',
    'post_title': props.post.title,
    'post_hashtags': props.post.hashtags,
    'post_url': props.post.url,
  });

  /*
    * CONTEXT AND REASONING:
    * 
    * 1. Preserves previous search criteria and results when users return from external links.
    * 2. Maintains state even after page refresh.
    * 3. Provides a better user experience by not interrupting the user's workflow.
    *
    * This implementation ensures a seamless browsing experience,
    * allowing users to navigate away and return without losing their search context.
  */ 
  searchCriteriaStore.saveToLocalStorage()
     
  // Open in a new tab if Ctrl key (or Cmd key on Mac) is pressed during click
  event.preventDefault();
  if (event.ctrlKey || event.metaKey) {
    window.open(props.post.url, '_blank');
  } else {
    window.location.href = props.post.url;
  }
}
</script>

<style scoped>
.post {
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 1.25rem;
  gap: 1rem;
  width: 100%;
  background: #FFFFFF;
  border: 0.0625rem solid #D9D9D9;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.post:hover {
  border-color: #1E1E1E;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
.post-link {
  display: block;
  width: 100%;
  text-decoration: none;
}

.post-content {
  width: 100%;
  display: flex;
  flex-direction: column;
}
</style>