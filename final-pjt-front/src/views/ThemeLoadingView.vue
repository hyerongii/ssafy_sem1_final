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
  import { useRoute, useRouter } from "vue-router"
  
  // Vue Router 인스턴스를 가져옵니다.
  const router = useRouter()
  const randomMessage = ref('')
  const route = useRoute()
  const themeId = route.params.theme_id
  
  const messages = [
    "특별한 테마의 세계로 안내하고 있어요 🌟",
    "테마 정보를 한 데 모으는 중이에요... 잠시만 기다려주세요 📊",
    "투자 테마의 숨겨진 이야기를 찾아가는 중이에요 🔍",
    "테마의 모든 것을 담아내고 있어요, 곧 만나요! 💫",
    "시장의 흐름을 읽어내는 중... 거의 다 왔어요 🌊",
    "시장의 트렌드를 분석하는 중이에요... 조금만 더! 📈",
    "테마의 전체적인 그림을 그리고 있어요 🎨",
    "최신 테마 동향을 불러오는 중이에요 ⭐️"
  ]
  
  onMounted(() => {
    // 랜덤 메시지 선택
    const randomIndex = Math.floor(Math.random() * messages.length);
    randomMessage.value = messages[randomIndex];
  });
  
  
  // 컴포넌트가 마운트되면 1초 후 ThemeItemView로 이동합니다.
  setTimeout(() => {
    // 여기 수정해야 합니다.
    router.push({ name: "ThemeItemView", params: { theme_id : themeId } })
  }, 2000)
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
    animation: loading 2s linear infinite;
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