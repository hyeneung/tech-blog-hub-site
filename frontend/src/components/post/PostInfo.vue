<template>
  <div class="post-info-wrapper">
    <div class="post-info">
      <div class="post-title-and-date">
        <h2 class="post-title">{{ post.title }}</h2>
        <span class="date">{{ formattedDate  }}</span>
      </div>                
      <div class="author-and-tags">                    
        <div class="author-section">
          <img v-if="companyLogo" :src="companyLogo" :alt="post.companyName + ' Logo'" class="company-logo">
          <div v-else class="company-logo placeholder">No Logo</div>
          <span class="author">{{ post.companyName }}</span>
        </div>
        <div class="tags">
            <span v-for="tag in post.hashtags" :key="tag" class="tag">#{{ tag }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script setup lang="ts">
import { computed } from 'vue';
import { useCompanyLogo } from '@/utils/useCompanyLogo'
import type { ArticleInfo } from '@/frontend-ts-axios-package'

const props = defineProps<{
  post: ArticleInfo
}>()

const formattedDate = computed(() => {
  const date = new Date(props.post.pubDate);

  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');

  return `${year}-${month}-${day}`;
});

const companyLogo = useCompanyLogo(props.post.companyName)
</script>

<style scoped>
.post-info {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.post-title-and-date {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  gap: 1.2rem;
}

.post-title {
  font-weight: 600;
  font-size: 1.5rem;
  line-height: 1.2;
  letter-spacing: -0.02em;
  color: #1E1E1E;
  margin: 0;
}

.date {
  font-weight: 400;
  font-size: 1.05rem;
  line-height: 1.2;
  color: #757575;
}

.author-and-tags {
  display: flex;
  align-items: center;
  width: 100%;
  margin-left: 1rem;
}

.author-section {
  display: flex;
  align-items: center;
  width: 25%;
  margin-right: 1rem;
}

.company-logo {
  height: 1.7rem;
  width: auto; 
}

.company-logo.placeholder {
  width: 1.7rem;
  height: 1.7rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  color: #666;
  font-size: 0.8rem;
}

.author {
  font-weight: 550;
  font-size: 1.2rem;
  line-height: 1.2;
  color: #1E1E1E;
  margin-left: 0.5rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  align-items: center;
  gap: 0.5rem;
  flex-grow: 1;
}

.tag {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0.25rem 0.5rem;
  background: #F5F5F5;
  border-radius: 0.25rem;
  font-family: 'Inter', sans-serif;
  font-style: normal;
  font-weight: 400;
  font-size: 1rem;
  line-height: 1;
  color: #757575;
}
</style>