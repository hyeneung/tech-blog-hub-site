<template>
  <div class="search-bar-wrapper">
    <div class="search-bar">
      <div class="search-group">
        <div class="search-icon">
          <img src="@/assets/search-icon.svg" alt="Search Icon" />
        </div>
        <input v-model="localSearchQuery" type="text" placeholder="Search the keyword" @keyup.enter="search">
      </div>
      <button @click="search"><span>Search</span></button>
    </div>
  </div>
</template>
  
<script setup lang="ts">
import { ref, watch } from 'vue'
import { useArticleSearchCriteriaStore } from '@/stores/articleSearchCriteriaStore'

const searchCriteriaStore = useArticleSearchCriteriaStore()
const localSearchQuery = ref('')

// Update local state when the store's query changes
// This is crucial for synchronizing the input field with store changes,
// especially when the header component resets the search criteria
watch(() => searchCriteriaStore.query, (newQuery) => {
  localSearchQuery.value = newQuery
})

const search = () => {
  if (localSearchQuery.value.trim()) {
    searchCriteriaStore.resetCriteriaExceptQuery(localSearchQuery.value.trim())
  }
}
</script>
  
<style scoped>
.search-bar-wrapper {
  display: flex;
  justify-content: center;
  margin: 1rem auto;
  padding: 0.5rem 1.25rem;
  position: relative;
  width: 100%;
  max-width: 50rem;
  height: 4rem;
  background: #FFFFFF;
  box-shadow: 0px 0.28rem 1rem #E5E5E5;
  border-radius: 0.5rem;
  transition: border 0.3s ease, box-shadow 0.3s ease;
  margin-bottom: 2rem;
}

.search-bar-wrapper:focus-within {
  border: 2px solid #2C2C2C;
  box-shadow: 0px 0px 5px rgba(90, 90, 90, 0.5);
}

/* 검색바 */
.search-bar {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  gap: 1rem;
}

/* 검색바 내부(아이콘 및 입력 필드) */
.search-group {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 0px 0.75rem;
  gap: 0.75rem;
  flex-grow: 1; 
}

/* 검색 입력 필드 */
.search-bar input {
  width: 100%; 
  height: 1.5rem;
  font-family: 'Roboto', sans-serif;
  font-style: normal;
  font-weight: 700;
  font-size: 1rem;
  line-height: 1.5rem;
  color: #2C2C2C;
  border: none;
  outline: none;
}

/* 검색 버튼 */
.search-bar button {
  flex-shrink: 0; /* 버튼 크기 유지 */
  padding: 0.5rem 1.5rem; 
  width: auto;
  height: 2.5rem;
  background: #2C2C2C;
  border-radius: 0.25rem;
  border: none;
  cursor: pointer;
  color: #FFFFFF; 
  font-family: 'Roboto', sans-serif;
  font-style: normal;
  font-weight: 900;
  font-size: 1rem;
  line-height: 1.5rem;
}

.search-icon img {
  display: flex;
  align-items: center;
}

/* 검색 버튼 호버 효과 */
.search-bar button:hover {
  background-color: #444;
}
@media (max-width: 768px) {
  .search-bar-wrapper {
    height: auto;
    padding: 0.5rem;
    margin: 1rem auto;
  }

  .search-bar {
    gap: 0.5rem;
  }

  .search-group {
    flex-grow: 1;
    padding: 0.5rem;
  }

  .search-bar input {
    font-size: 1rem;
  }

  .search-bar button {
    flex-shrink: 0;
    font-size: 1rem;
    padding: 0.4rem 0.8rem;
  }

}

@media (max-width: 480px) {
  .search-bar-wrapper {
    padding: 0.35rem;
    margin: 0.75rem auto;
  }

  .search-group {
    padding: 0.25rem;
  }

  .search-bar input {
    font-size: 0.9rem;
  }

  .search-bar button {
    flex-shrink: 0;
    font-size: 0.8rem;
    padding: 0.4rem 0.8rem;
  }

}
</style>