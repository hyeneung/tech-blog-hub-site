<template>
  <div class="tags-wrapper">
    <section class="tags">
      <button 
        v-for="tag in tags" 
        :key="tag.name" 
        :class="{ active: isTagActive(tag.name) }" 
        @click="toggleTag(tag.name)"
      >
        {{ '#' + tag.name }}
      </button>
    </section>
  </div>
</template>
  
<script setup lang="ts">
import { ref } from 'vue'
import { tags as initialTags, Tag } from '@/data/tags'
import { useArticleSearchCriteriaStore } from '@/stores/articleSearchCriteriaStore'

const tags = ref<Tag[]>(initialTags)
const searchStore = useArticleSearchCriteriaStore()

const isTagActive = (tagName: string) => {
  return searchStore.hashtags.includes(tagName)
}

const toggleTag = (tagName: string) => {
  const currentTags = [...searchStore.hashtags]
  const tagIndex = currentTags.indexOf(tagName)
  
  if (tagIndex > -1) {
    currentTags.splice(tagIndex, 1)
  } else {
    currentTags.push(tagName)
  }
  
  searchStore.setHashtags(currentTags)
}
</script>
  
<style scoped>
.tags-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  align-content: flex-start;
  gap: 0.5rem;
  max-width: 52rem; 
}

.tags button {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0.5rem;
  background-color: #F5F5F5;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  font-style: normal;
  font-weight: 400;
  font-size: 1rem;
  line-height: 100%;
  color: #757575;
  transition: background-color 0.3s, color 0.3s;
}

.tags button.active {
  background-color: #2C2C2C;
  color: #F5F5F5;
}

.tags button:hover {
  background-color: #E0E0E0;
}

.tags button.active:hover {
  background-color: #1A1A1A;
}
@media (max-width: 768px) {
  .tags-wrapper {
    margin-bottom: 0.75rem; /* 여백 조정 */
  }

  .tags button {
    padding: 0.4rem;
    font-size: 1rem;
    line-height: normal; 
    border-radius: 0.4rem; 
    max-width: none; 
    width: auto; 
  }
}

@media (max-width: 480px) {
   .tags button {
    padding: 0.3rem; /* 패딩 더 감소 */
    font-size: 0.8rem; /* 글꼴 크기 더 감소 */
    border-radius: 0.3rem; /* 모서리 둥글기 더 조정 */
   }
}
</style>