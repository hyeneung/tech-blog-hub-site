<template>
  <article class="post">
    <div @click="handlePostClick" class="post-content">
      <PostInfo :post="post" />
      <PostContent :summary="post.summarizedText" />
    </div>
  </article>
</template>

<script setup lang="ts">
import PostInfo from './PostInfo.vue'
import PostContent from './PostSummary.vue'
import { getApiConfig } from '@/config/api'
import { RedirectApi } from '@/frontend-ts-axios-package'
import type { ArticleInfo } from '@/frontend-ts-axios-package'
import { useArticleSearchCriteriaStore } from '@/stores/articleSearchCriteriaStore'

const props = defineProps<{
  post: ArticleInfo
}>()

const redirectApi = new RedirectApi(getApiConfig())

const searchCriteriaStore = useArticleSearchCriteriaStore()

const handlePostClick = async (event: MouseEvent) => {

  // If the clicked element is a child of an element with the 'summary-toggle' class, do not process the event
  if ((event.target as HTMLElement).closest('.summary-toggle')) {
    event.preventDefault()
    return
  }

  searchCriteriaStore.saveToLocalStorage()
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
  
  event.preventDefault();
  try {
    const userId = localStorage.getItem('userId') || undefined;
    await redirectApi.redirectToUrl(props.post.url, userId);    
  } catch (error) {    
    console.error('Error logging click:', error instanceof Error ? error.message : String(error));
  } finally{
    // Even if a request fails due to CORS issues, we still redirect the user to maintain a smooth experience
    // Open in a new tab if Ctrl key (or Cmd key on Mac) is pressed during click
    if (event.ctrlKey || event.metaKey) {
      window.open(props.post.url, '_blank');
    } else {
      window.location.href = props.post.url;
    }
    /*
      * CONTEXT AND REASONING:
      *
      * 1. Cross-Origin Challenges:
      *    Our application needs to redirect users to external blog posts, which are on different domains.
      *    These external domains may not have CORS (Cross-Origin Resource Sharing) properly configured,
      *    especially for OPTIONS requests (preflight requests).
      *
      * 2. Logging Requirement:
      *    We want to log user clicks for analytics purposes before redirecting them.
      *    This requires an API call to our backend.
      *
      * 3. CORS and OPTIONS Method:
      *    Modern browsers send an OPTIONS request before the actual GET request for cross-origin requests,
      *    especially when custom headers (like our user ID) are included.
      *    Many external domains don't handle OPTIONS requests, leading to CORS errors.
      *
      * 4. Solution Approach:
      *    To overcome these limitations, we've implemented a "fire-and-forget" logging mechanism:
      *    a. We initiate the logging API call to our backend.
      *    b. Without waiting for the response, we immediately redirect the user.
      *    
      *    This approach ensures:
      *    - The user experience is not delayed by waiting for our logging to complete.
      *    - We avoid CORS issues with external domains that don't support OPTIONS requests.
      * 
      * This implementation balances the needs for analytics data collection with providing a seamless user experience,
      * while working around the limitations imposed by external domains that we cannot control.
    */
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