<template>
  <div class="select-wrapper">
    <div class="custom-select">
      <select v-model="selectedCompany" @change="updateSelectedCompany">
        <option value="">모든 회사</option>
        <option v-for="company in companies" :key="company.name" :value="company.name">
          {{ company.name }}
        </option>
      </select>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { companies } from '@/data/companies'
import { useArticleSearchCriteriaStore } from '@/stores/articleSearchCriteriaStore'

const selectedCompany = ref('')
const searchCriteriaStore = useArticleSearchCriteriaStore()

const updateSelectedCompany = () => {
  searchCriteriaStore.setCompany(selectedCompany.value)
}
</script>

<style scoped>
.select-wrapper {
  display: flex;
  justify-content: flex-start;
  font-family: 'Montserrat', 'Inter', sans-serif;
  width: 8rem;
  margin-bottom: 0.5rem;
}

.custom-select select {
  width: 100%;
  font-size: 1rem;
  padding: 0.2rem 0.2rem;
  border-radius: 0.3rem;
}
</style>