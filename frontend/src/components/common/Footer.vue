<template>
  <footer>
    <div class="footer-content">
      <Pagination />
      <div class="additional-info">
        <p>Summaries and hashtags are generated using LLM</p>
      </div>
      <div class="link-section">
        <p>For a recommendation system,  
          <a href="https://chromewebstore.google.com/detail/tech-blog-hub-site-extens/jkccccofndhnikmhcfmgcelhbmbpncmh" target="_blank" class="link">try our Chrome extension!</a>
        </p>
        <a href="https://forms.gle/DnngrecMjMytAkCL9" target="_blank" class="link">Send Feedback</a>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import Pagination from './Pagination.vue'
</script>

<style scoped>
footer {
  display: flex;
  justify-content: center;
  align-items: center; 
  margin-bottom: 2rem; 
}

.footer-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  gap: 0.5rem;
}

.link-section {
  text-align: center;
}

.additional-info{
  font-size: 1rem;
  opacity: 0.8;
  color: #666;
  text-align: center;
  margin: 0;
  white-space: nowrap; /* Prevents text from wrapping */
  overflow: hidden; /* Hides any overflow text */
  text-overflow: ellipsis; /* Adds ellipsis (...) for overflowed text */
}

.link {
  font-size: 1rem;
  text-align: center;
  color: #555; /* 링크 색상 */
  text-decoration: none; /* 밑줄 제거 */
  font-weight: 100; /* 글자 두께 */
}

.link:hover {
  text-decoration: underline; /* 호버 시 밑줄 표시 */
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 0 1rem;
  }

  .llm-info{
    margin: 0 1rem;
  }
}
@media (max-width: 480px) {
  .llm-info{
    font-size: 0.85rem;
    margin: 0 1rem;
  }
  .feedback-link {
    font-size: 0.85rem;
  }
}
</style>