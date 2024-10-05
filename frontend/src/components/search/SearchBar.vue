<template>
  <div class="search-bar-wrapper">
    <div class="search-bar">
      <div class="search-group">
        <div class="search-icon">
          <img src="@/assets/search-icon.svg" alt="Search Icon" />
        </div>
        <input v-model="searchQuery" type="text" placeholder="Search the keyword">
      </div>
      <button @click="search"><span>Search</span></button>
    </div>
  </div>
</template>
  
<script setup>
import { ref } from 'vue'

const searchQuery = ref('')

const search = () => {
  console.log('Searching for:', searchQuery.value)
}
</script>
  
<style scoped>
.search-bar-wrapper {
  display: flex;
  justify-content: center;
  margin: 1.25rem auto;
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

/* 검색 버튼 호버 효과 */
.search-bar button:hover {
  background-color: #444;
}
</style>