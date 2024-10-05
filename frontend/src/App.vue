<template>
  <Header />
  <main>
    <SearchBar />
    <Hashtags />
    <PostList />
  </main>
  <Footer />
</template>

<script setup>
import Header from './components/common/Header.vue'
import SearchBar from './components/search/SearchBar.vue'
import Hashtags from './components/search/Hashtags.vue'
import PostList from './components/post/PostList.vue'
import Footer from './components/common/Footer.vue'
</script>