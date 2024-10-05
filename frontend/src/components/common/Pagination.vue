<template>
  <nav class="pagination">
    <button class="pagination__btn pagination__btn--prev" disabled>
      <span class="pagination__icon">←</span>
      <span>Previous</span>
    </button>
    <ul class="pagination__list">
      <li><button class="pagination__page pagination__page--active">1</button></li>
      <li><button class="pagination__page">2</button></li>
      <li><button class="pagination__page">3</button></li>
      <li><span class="pagination__gap">...</span></li>
      <li><button class="pagination__page">98</button></li>
      <li><button class="pagination__page">99</button></li>
    </ul>
    <button class="pagination__btn pagination__btn--next">
      <span>Next</span>
      <span class="pagination__icon">→</span>
    </button>
  </nav>
</template>
  
<script setup>
import { ref } from 'vue'

const currentPage = ref(1)
const totalPages = ref(99)

const changePage = (page) => {
  currentPage.value = page
  // 페이지 변경 로직
}
</script>

<style scoped>
.pagination {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 0;
  gap: 0.5rem;
  width: 100%;
  max-width: 32rem;
  height: 2.5rem; 
  font-family: 'Inter', sans-serif;
}

.pagination__btn {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 0.5rem 0.8rem; 
  gap: 0.5rem;
  height: 2rem;
  border: none;
  background: none;
  border-radius: 0.5rem; 
  font-size: 1rem; 
  color: #1E1E1E;
  cursor: pointer;
}

.pagination__btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination__btn--prev {
  width: 7.5rem; 
}

.pagination__btn--next {
  width: 5.5rem;
}

.pagination__icon {
  font-size: 1rem;
}

.pagination__list {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 0;
  gap: 0.5rem;
  list-style-type: none;
}

.pagination__page {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 2rem; 
  height: 2rem; 
  border: none;
  background: none;
  border-radius: 0.5rem;
  font-size: 1rem; 
  color: #1E1E1E;
  cursor: pointer;
}

.pagination__page--active {
  background: #2C2C2C;
  color: #F5F5F5;
}

.pagination__gap {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 3rem; 
  height: 2.5rem; 
  font-weight: 700;
  font-size: 1rem;
  color: #000000;
}
</style>