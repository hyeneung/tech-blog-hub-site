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
    <div class="empty-space"></div> <!-- Empty space to push content -->
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
  display: flex; /* Use flexbox for layout */
  justify-content: center; /* Center items initially */
  align-items: center; /* Center items vertically */
  width: 100%; /* Full width */
  max-width: 58rem; /* Limit max width */
  margin: 0 auto; /* Center align initially */
  margin-bottom: 0.5rem;
}

.custom-select {
  display: inline-block; /* Keep it inline-block to size according to content */
  text-align: left; /* Align text inside select to the left */
}

.custom-select select {
  width: 100%; /* Make select take full width of .custom-select */
  font-size: 1rem;
  padding: 0.2rem;
  border-radius: 0.3rem;
}

.empty-space {
  flex-grow: 1; /* Allow this div to take up remaining space */
}

@media (max-width: 740px) {
  .select-wrapper {
    justify-content: flex-start; /* Align items to the left when below breakpoint */
    margin-left: 0; /* Remove auto margins on left for alignment */
    margin-right: auto; /* Keep right margin auto for centering when above breakpoint */
    padding-left: 1rem; /* Optional padding for better spacing */
    padding-right: 1rem; /* Optional padding for better spacing */
    max-width: none; /* Allow full width on small screens */
  }
}

@media (max-width: 480px) {
  .select-wrapper {
    padding: 0.25rem; /* Adjust padding for smaller screens */
    width: auto; /* Allow it to resize naturally */
    max-width: none; /* Remove max-width restriction for smaller screens */
    margin-left: 0; /* Align left when below breakpoint */
    margin-right: 0; /* Align left when below breakpoint */
    justify-content: flex-start; /* Ensure items are aligned to the start on small screens */
  }
  
  .custom-select select {
    font-size: 0.8rem;
    padding: 0.1rem;
  }
}
</style>