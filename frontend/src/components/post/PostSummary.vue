<template>
  <div class="post-summary">
    <div class="summary-container">
      <div class="summary-toggle" :class="{ active: isActive }" @click="toggleSummary">
        <span class="summary-toggle-text">요약된 내용 보기</span>
      </div>
      <div v-if="isActive" class="summary">
        <p>{{ summary }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  summary: {
    type: String,
    required: true
  }
})

const isActive = ref(false)

const toggleSummary = () => {
  isActive.value = !isActive.value
}
</script>

<style scoped>
.post-summary {
  --font-family: 'Inter', sans-serif;
  --primary-color: #1E1E1E;
  --border-color: #D9D9D9;
  --background-color: #FFFFFF;

  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
  gap: 1rem;
}

.summary-container {
  width: 100%;
  border: 1px solid var(--border-color);
  border-radius: 0.5rem;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
}

.summary-container:hover {
  border-color: var(--primary-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.summary-toggle {
  box-sizing: border-box;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  width: 100%;
  background: var(--background-color);
  cursor: pointer;
}

.summary-toggle-text {
  font-family: var(--font-family);
  font-style: normal;
  font-weight: 600;
  font-size: 1rem;
  line-height: 140%;
  color: var(--primary-color);
}

.summary-toggle::after {
  content: '';
  display: block;
  width: 0.5rem; 
  height: 0.5rem; 
  border: solid var(--primary-color);
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
  transition: transform 0.3s ease;
}

.summary-toggle.active::after {
  transform: rotate(-135deg);
}

.summary {
  display: none;
  flex-direction: column;
  padding: 0 1rem 1rem;
  gap: 0.5rem;
  width: 100%;
  background: var(--background-color);
}

.summary p {
  margin: 0;
  font-family: var(--font-family);
  font-style: normal;
  font-weight: 500;
  font-size: 1rem;
  line-height: 150%;
  color: var(--primary-color);
}

.summary-toggle.active + .summary {
  display: flex;
}

@media (max-width: 70rem) {
  .summary-toggle {
    padding: 0.75rem;
  }

  .summary-toggle-text,
  .summary p {
    font-size: 0.875rem;
  }

  .summary-toggle::after {
    width: 0.4rem;
    height: 0.4rem;
  }

  .summary {
    padding: 0 0.75rem 0.75rem;
  }
}
</style>