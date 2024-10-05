<template>
  <div class="tags-wrapper">
    <section class="tags">
      <button v-for="tag in tags" :key="tag.id" :class="{ active: tag.active }" @click="toggleTag(tag.id)">
        {{ tag.name }}
      </button>
    </section>
  </div>
</template>
  
<script setup>
import { ref } from 'vue'
import { tags as initialTags } from '@/data/tags'

const tags = ref(initialTags)

const toggleTag = (id) => {
  const tag = tags.value.find(t => t.id === id)
  if (tag) {
      tag.active = !tag.active
  }
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
  max-width: 52rem;  /* 수정 */
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
</style>