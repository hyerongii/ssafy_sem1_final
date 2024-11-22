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
    <swiper-slide class="slide">
      <section class="section">
        <h2>야 너두 미국주식 할 수 있어!</h2>
        <p>당신만의 투자 동반자, 맞춤형 투자 추천 서비스!</p>
      </section>
    </swiper-slide>

    <!-- 2. MBTI 기반 개인화 추천 서비스 -->
    <swiper-slide class="slide">
      <section class="section">
        <h2>MBTI 기반 개인화 추천 서비스</h2>
        <p>당신의 성향에 맞는 맞춤형 투자 전략을 제안합니다.</p>
      </section>
    </swiper-slide>

    <!-- 3. 국내주식부터 해외주식까지 한눈에! -->
    <swiper-slide class="slide">
      <section class="section">
        <h2>국내주식부터 해외주식까지 한눈에!</h2>
        <p>국내외 다양한 주식 정보를 한 곳에서 확인하세요.</p>
      </section>
    </swiper-slide>

    <!-- 4. 주린이여도 괜찮아! -->
    <swiper-slide class="slide">
      <section class="section">
        <h2>주린이여도 괜찮아!</h2>
        <p>초보 투자자도 쉽게 따라할 수 있는 가이드와 추천 종목 제공.</p>
      </section>
    </swiper-slide>

    <!-- 5. 커뮤니티 (다양한 사람들과 종목에 대해 토의해봐요!) -->
    <swiper-slide class="slide">
      <section class="section">
        <h2>커뮤니티</h2>
        <p>다양한 사람들과 종목에 대해 토론하고 의견을 나누세요!</p>
      </section>
    </swiper-slide>

  </swiper>
</template>

<script setup>
import { Swiper, SwiperSlide } from 'swiper/vue';
import { Pagination, Mousewheel } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/pagination';

const modules = [Pagination, Mousewheel];

const onSwiper = (swiper) => {
  console.log(swiper);
};

const onSlideChange = () => {
  console.log('slide change');
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
}

.section h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.section p {
  font-size: 1.25rem;
}

/* 페이지네이션 스타일 */
.swiper-pagination-bullet {
  width: 10px;
  height: 10px;
  background: #000;
  opacity: 0.5;
}

.swiper-pagination-bullet-active {
  opacity: 1;
}
</style>



