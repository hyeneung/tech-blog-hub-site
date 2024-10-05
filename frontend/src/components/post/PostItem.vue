<template>
  <a :href="post.link" class="post-link">
    <article class="post">
      <PostInfo :post="post" />
      <PostContent :summary="post.summary" />
    </article>
  </a>
</template>

<script setup>
import PostInfo from './PostInfo.vue'
import PostContent from './PostSummary.vue'

defineProps({
  post: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.post-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

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
</style>