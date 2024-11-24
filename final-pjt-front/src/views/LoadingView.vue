<template>
  <div class="loading-container">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
    <p>Zoozoo님께 커스텀된 테마를 추천하고 있어요...</p>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

// Vue Router 인스턴스를 가져옵니다.
const router = useRouter();

// 컴포넌트가 마운트되면 4초 후 ThemeListView로 이동합니다.
setTimeout(() => {
  router.push({ name: "ThemeListView" }); 
}, 4000);
</script>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh; /* 화면 전체 높이 */
  background-color: #f8f9fa; /* 부드러운 배경색 */
}

.spinner-border {
  width: 3rem;
  height: 3rem;
  margin-bottom: 1rem; /* 텍스트와 간격 */
}
</style>