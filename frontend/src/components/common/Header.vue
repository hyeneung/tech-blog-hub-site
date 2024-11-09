<template>
  <header class="container">
    <a href="/" class="logo" @click.prevent="resetAndNavigate">
      <img :src="logoSrc" alt="Logo">
      <h1>기술 블로그 허브 사이트</h1>
    </a>
  </header>
</template>

<script setup lang="ts">
import { useArticleSearchCriteriaStore } from '@/stores/articleSearchCriteriaStore'
import logoSrc from '@/assets/logo.png'

const searchCriteriaStore = useArticleSearchCriteriaStore()

const resetAndNavigate = () => {
  searchCriteriaStore.resetCriteriaAndLoad()
}
</script>

<style scoped>
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: inherit;
}

.logo img {
  width: 3rem;
  height: 3rem;
  margin-right: 0.625rem;
}

h1 {
  font-size: 1.5rem;
  margin: 0;
}
</style>