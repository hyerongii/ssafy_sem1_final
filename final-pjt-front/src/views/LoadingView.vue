<template>
  <div class="loading-container">
    <div class="loading-box">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">로딩중...</span>
      </div>
      <p class="loading-text">{{ randomMessage }}</p>
      <div class="loading-bar">
        <div class="loading-progress"></div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from "vue-router"

// Vue Router 인스턴스를 가져옵니다.
const router = useRouter()
const randomMessage = ref('')

const messages = [
  "ZooZoo님만을 위한 특별한 투자 레시피를 준비하고 있어요 🌱",
  "ZooZoo님의 투자 테마을 분석하는 중이에요... 잠시만요! 🔍",
  "ZooZoo님을 위한 맞춤 테마를 찾아보는 중... 거의 다 왔어요! ✨"
]

onMounted(() => {
  // 랜덤 메시지 선택
  const randomIndex = Math.floor(Math.random() * messages.length);
  randomMessage.value = messages[randomIndex];
});


// 컴포넌트가 마운트되면 4초 후 ThemeListView로 이동합니다.
setTimeout(() => {
  router.push({ name: "ThemeListView" })
}, 4000)
</script>

<style scoped>
.loading-container {
  min-height: calc(100vh - 64px);
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8faf5, #fff);
  padding: 20px;
  margin-top: 64px;
  font-family: 'Godo', sans-serif;
}

.loading-box {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 8px 20px rgba(139, 193, 72, 0.1);
  width: 100%;
  max-width: 600px; /* 박스 너비를 좀 더 넓게 조정 */
  text-align: center;
}

.spinner-border {
  width: 4rem;
  height: 4rem;
  color: var(--primary-color);
  margin-bottom: 1.5rem;
}

.loading-text {
  color: #333;
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
  white-space: nowrap; /* 텍스트를 한 줄로 표시 */
  max-width: 100%; /* 부모 요소의 너비를 넘지 않도록 설정 */
}

.loading-bar {
  width: 100%;
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.loading-progress {
  width: 30%;
  height: 100%;
  background: var(--primary-dark);
  border-radius: 4px;
  animation: loading 4s linear infinite;
}

@keyframes loading {
  0% {
    width: 0%;
  }
  100% {
    width: 100%;
  }
}

</style>