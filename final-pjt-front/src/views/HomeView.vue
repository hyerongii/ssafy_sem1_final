<template>
  <swiper
    :modules="modules"
    :slides-per-view="1"
    :space-between="0"
    direction="vertical"
    :mousewheel="true"
    :pagination="{ clickable: true }"
    @swiper="onSwiper"
    @slideChange="onSlideChange"
    class="mySwiper"
  >
    <swiper-slide class="slide" >
      <section class="section">
        <!-- zoozoo랜드만 색 변환 -->
        <h2>Welcome to ZooZoo랜드</h2>
        <!-- 주린이만 색변환 -->
        <p>주린이의 주린이에 의한 주린이를 위한</p>
        <p>맞춤형 투자 추천 서비스!</p>
      </section>
    </swiper-slide>

    <!-- 2. MBTI 기반 개인화 추천 서비스 -->
    <swiper-slide class="slide">
      <section class="section">
        <h2>MBTI 기반 커뮤니티 서비스</h2>
        <p>나랑 같은 MBTI 사람들은 어떤 테마를 추천받았을까?</p>
      </section>
    </swiper-slide>

    <!-- 3. 국내주식부터 해외주식까지 한눈에! -->
    <swiper-slide class="slide">
      <section class="section">
        <h2>야! 너두 미국주식 할 수 있어!</h2>
        <p>(속닥속닥) 미국 주식은 하루라도 일찍 사는게 이득이래 🤭</p>
      </section>
    </swiper-slide>

    <!-- 4. 주린이여도 괜찮아! -->
    <swiper-slide class="slide zoo-background">
      <section class="section">
        <h2>주린이여도 괜찮아!</h2>
        <p>초보 투자자도 쉽게 접할 수 있는 가이드와 추천 종목 제공</p>
      </section>
    </swiper-slide>


  </swiper>
  <!-- 진문수정 / Fixed 버튼 추가 -->
  <button class="theme-recommend-btn" @click="goToThemeRecommendation">
    테마 추천받기
  </button>
</template>

<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue';
import { Pagination, Mousewheel } from 'swiper/modules';

import 'swiper/css';
import 'swiper/css/pagination';
// 진문수정
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
const modules = [Pagination, Mousewheel];

// 진문수정
const router = useRouter()
const authStore = useAuthStore()

const onSwiper = (swiper) => {
  console.log(swiper);
};

const onSlideChange = () => {
  console.log('slide change');
};

// 진문수정 / 버튼 클릭 시 라우팅 함수
const isLoggedIn = computed(() => authStore.isAuthenticated)
const goToThemeRecommendation = () => {
  // 로그인 된 유저라면 
  if (isLoggedIn.value) {
    router.push({name: 'UserSelectView'})
  // 로그인 되어 있지 않은 유저라면
  } else {
    // 1. <추천받기 위해 로그인을 진행해 주세요!> 라는 알림창 띄우기
    alert('추천받기 위해 로그인을 진행해 주세요!')
    // 2. 로그인 페이지로 이동(router.push 활용)
    router.push({name: 'LogInView'})
  }
  
};
</script>

<style>
.mySwiper {
  height: 100vh;
  width: 100%;
}

.swiper-slide {
  display: flex;
  justify-content: center;
  align-items: center;
  background: #fff;
}

.section {
  text-align: center;
  padding: 20px;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.8s ease forwards;
}

.section h2 {
  font-size: 4.0rem;
  margin-bottom: 1.5rem;
  color: var(--primary-color);
  font-weight: bold;
  line-height: 1.2;
  font-family: 'Godo', sans-serif;
}

.section p {
  font-size: 1.8rem;
  color: #666;
  line-height: 1.6;
  max-width: 800px;
  margin: 0 auto;
  font-family: 'Godo', sans-serif;
}

/* 페이지네이션 스타일 */
.swiper-pagination-bullet {
  width: 12px;
  height: 12px;
  background: var(--primary-color);
  opacity: 0.5;
}

.swiper-pagination-bullet-active {
  opacity: 1;
  background: var(--primary-color);
}
/* 진문수정 / Fixed 버튼 스타일 */
.theme-recommend-btn {
  position: fixed;
  bottom: 40px; /* 하단에서 더 멀리 떨어지게 조정 */
  left: 50%; /* 왼쪽 가장자리에서 50% 위치로 이동 */
  transform: translateX(-50%); /* 버튼의 중앙이 화면 중앙에 오도록 조정 */
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 50px;
  padding: 20px 40px;
  font-size: 1.3rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(255, 107, 98, 0.3);
  transition: all 0.3s ease;
  z-index: 1000; /* 다른 요소 위로 올리기 */
  font-family: 'Godo', sans-serif;
}

.theme-recommend-btn:hover {
  background-color: var(--primary-dark);
  transform: translateX(-50%) translateY(-5px);
  box-shadow: 0 6px 20px rgba(255, 107, 98, 0.4);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.zoo-background {
  background-image: url('@/assets/zoo-background.png'); /* 이미지 경로 */
  background-size: cover; /* 이미지 크기 조정 */
  background-position: center; /* 이미지 위치 */
}
</style>



