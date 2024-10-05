<template>
  <div class="select-wrapper">
    <div class="custom-select">
      <select v-model="selectedCompany">
        <option value="">모든 회사</option>
        <option v-for="company in companies" :key="company" :value="company">
          {{ company }}
        </option>
      </select>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const companies = ['여기어때', '라인', '토스']
const selectedCompany = ref('')
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