<template>
  <div class="pagination-wrapper">
    <nav v-if="paginationStore.pageInfo" class="pagination">
      <button 
        class="pagination__btn pagination__btn--prev" 
        :disabled="currentPage === 0"
        @click="changePage(currentPage - 1)"
      >
        <span class="pagination__icon">←</span>
        <span>Prev</span>
      </button>
      <ul class="pagination__list">
        <li v-for="page in displayedPages" :key="page">
          <button 
            v-if="page !== '...'"
            class="pagination__page" 
            :class="{ 'pagination__page--active': page === currentPage }"
            @click="changePage(page)"
          >
            {{ typeof page === 'number' ? page + 1 : page }}
          </button>
          <span v-else class="pagination__gap">...</span>
        </li>
      </ul>
      <button 
        class="pagination__btn pagination__btn--next"
        :disabled="currentPage === totalPages - 1"
        @click="changePage(currentPage + 1)"
      >
        <span>Next</span>
        <span class="pagination__icon">→</span>
      </button>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useArticleSearchCriteriaStore } from '@/stores/articleSearchCriteriaStore'
import { usePaginationStore } from '@/stores/paginationStore'

const searchStore = useArticleSearchCriteriaStore()
const paginationStore = usePaginationStore()

const currentPage = computed(() => paginationStore.pageInfo?.pageNumber || 0)
const totalPages = computed(() => paginationStore.pageInfo?.totalPages || 1)

const displayedPages = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  const pages = []

  pages.push(0);

  if (total <= 7) {
    for (let i = 1; i < total; i++) {
      pages.push(i)
    }
  } else {
    if (current <= 3) {
      for (let i = 1; i <= 4; i++) {
        pages.push(i);
      }
      pages.push('...');
      pages.push(total-1);
    } else if (current >= total - 4) {
      pages.push('...');
      for (let i = total - 5; i < total - 1; i++) {
        pages.push(i);
      }
      pages.push(total-1);
    } else {
      pages.push('...');
      pages.push(current - 1);
      pages.push(current);
      pages.push(current + 1);
      pages.push('...');
      pages.push(total-1);
    }
  }

  return pages
})

const changePage = (page: number | string) => {
  const newPage = typeof page === 'string' ? parseInt(page, 10) : page;
  if (newPage < 0 || newPage >= totalPages.value) return;
  searchStore.setPage(newPage);
}
</script>

<style scoped>
.pagination-wrapper {
  width: 100%;
  display: flex;
  justify-content: center; /* 중앙 정렬 */
}

.pagination {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 0;
  gap: 0rem;
  margin: 1rem auto;
  width: 100%;
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
  height: auto;
  border: none;
  background: none;
  border-radius: 0.5rem; 
  font-size: inherit; /* Use inherited font size */ 
  color: #1E1E1E;
  cursor: pointer;
}

.pagination__icon {
  font-size: inherit; /* Use inherited font size */
}

.pagination__btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination__btn--prev {
  width: auto; 
}

.pagination__btn--next {
  width: auto;
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
  width: auto; 
  height: auto;
  padding: 0.5rem; 
  border: none;
  background: none;
  border-radius: 0.5rem;
  font-size: inherit; 
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
  width: auto; 
  height: auto; 
  font-weight: 700;
  color: #000000;
}
</style>