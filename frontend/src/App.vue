<template>
  <Header />
  <main class="app-container">
    <SearchBar />
    <Hashtags />
    <PostList />
  </main>
  <Footer class="app-container"/>
</template>

<script setup lang="ts">
import Header from './components/common/Header.vue'
import SearchBar from './components/search/SearchBar.vue'
import Hashtags from './components/search/Hashtags.vue'
import PostList from './components/post/PostList.vue'
import Footer from './components/common/Footer.vue'
</script>

<style>
.app-container {
  max-width: 1200px;
  margin: 0 auto; /* 중앙 정렬을 위해 자동 마진 */
  display: flex; /* 플렉스 박스 사용 */
  flex-direction: column; /* 세로 방향으로 정렬 */
  align-items: center; /* 자식 요소들을 중앙 정렬 */
}

.post-info-wrapper,
.post-summary-wrapper {
  width: 100% !important;
}
</style>