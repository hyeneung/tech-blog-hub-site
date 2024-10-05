<template>
  <section class="post-container">
      <CompanySelect />
      <PostItem v-for="post in posts" :key="post.id" :post="post" />
  </section>
</template>
  
<script setup>
import { ref } from 'vue'
import PostItem from './PostItem.vue'
import CompanySelect from '../search/CompanySelect.vue';
function getImageUrl(name) {
  return new URL(`../../assets/${name}`, import.meta.url).href
}
const posts = ref([
  {
    id: 1,
    title: "CodeDeploy를 이용한 배포 실패 Troubleshooting",
    date: "2024-09-13",
    company: "여기어때",
    companyLogo: getImageUrl('yogiottae.png'),
    tags: ["Backend", "DevOps"],
    summary: "이 게시글은 CI/CD 과정에서 발생한 문제와 이를 해결하는 과정에 대해 담은 글입니다."
  },
])
</script>
  
<style scoped>
.post-container {
  max-width: 70rem;
  margin: 0 auto;
  padding: 0 1rem;
}
</style>