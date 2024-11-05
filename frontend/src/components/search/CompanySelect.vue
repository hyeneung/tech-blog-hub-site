<template>
  <div class="select-wrapper">
    <div class="custom-select">
      <select v-model="selectedCompany">
        <option value="">모든 회사</option>
        <option v-for="company in companies" :key="company.name" :value="company.name">
          {{ company.name }}
        </option>
      </select>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { companies } from '@/data/companies'
import { useArticleSearchCriteriaStore } from '@/stores/articleSearchCriteriaStore'
import { storeToRefs } from 'pinia'

const searchCriteriaStore = useArticleSearchCriteriaStore()

const { company } = storeToRefs(searchCriteriaStore)
// 양방향 바인딩
// 사용자가 회사 선택 -> setter 호출. 검색조건 변경 -> api 호출
// 사용자가 검색조건 초기화 선택 -> company 변경 -> 변경감지. getter 호출. selectedCompany 변경
const selectedCompany = computed({
  get: () => company.value,
  set: (value) => searchCriteriaStore.setCompany(value)
})
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