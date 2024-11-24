<template>
  <div class="app-container">
    <nav class="navbar fixed-top navbar-expand-lg navbar-light bg-light w-100">
      <div class="container-fluid justify-content-end">
        <RouterLink :to="{ name: 'HomeView' }" class="nav-link">Home</RouterLink>
        <RouterLink v-if="!isLoggedIn" :to="{ name: 'LogInView' }" class="nav-link">로그인</RouterLink>
        <RouterLink v-if="!isLoggedIn" :to="{ name: 'SignUpView' }" class="nav-link">회원가입</RouterLink>
        <!-- 진문수정 / 테스트용은 이제 없어도 될 것 같습니다. -->
        <!-- <RouterLink v-if="isLoggedIn" :to="{ name: 'UserSelectView' }" class="nav-link">테마추천(테스트용)</RouterLink> -->
        <RouterLink v-if="isLoggedIn" :to="{ name: 'UserSelectView' }" class="nav-link">재추천 받기</RouterLink>
        <!-- 진문수정 / 인증된 사용자의 경우 추천받았던 테마들을 다시 볼 수 있도록 nav 탭 구성 -->
        <RouterLink v-if="isLoggedIn" :to="{ name: 'ThemeListView' }" class="nav-link">추천받은 테마</RouterLink>
        <button v-if="isLoggedIn" @click="logOut" class="nav-link btn btn-link">로그아웃</button>
      </div>
    </nav>
    <div class="content">
      <RouterView/>
    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'
import { computed } from 'vue'

const store = useAuthStore()
const isLoggedIn = computed(() => store.isAuthenticated)

const logOut = function () {
  store.logOut()
}
</script>

<style>
/* 전역 CSS 변수 설정 - scoped 밖에 작성 */
:root {
  --primary-color: #8bc148;
  --primary-light: #DCCAF0;
  /* --primary-dark: #A274D6; */ /* 보라색 */ 
  --primary-dark: #D372A4;
}
</style>

<style scoped>

/* .App {
  font-family:'Godo'; 
} */

@font-face {
  font-family: 'Godo';
  font-style: normal;
  font-weight: 400;
  src: url('//cdn.jsdelivr.net/korean-webfonts/1/corps/godo/Godo/GodoM.woff2') format('woff2'), url('//cdn.jsdelivr.net/korean-webfonts/1/corps/godo/Godo/GodoM.woff') format('woff');
}

/* 전체 페이지 레이아웃 */
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh; /* 전체 화면 높이 */
  background: linear-gradient(135deg, #fff5f3, #fff);
}

.container-fluid {
  padding-left: 2rem;  /* 왼쪽 여백 */
  padding-right: 2rem; /* 오른쪽 여백 */
  max-width: 1400px;   /* 최대 너비 설정 */
  margin: 0 auto;      /* 중앙 정렬 */
}

.navbar {
  background: var(--primary-color) !important;
  min-height: 64px;
  padding: 0.5rem 0;   /* 상하 패딩만 적용 */
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  font-family: 'Godo', sans-serif;
}

/* 네비게이션 링크 스타일 */
.nav-link {
  text-decoration: none; /* 밑줄 없애기 */
  color: white !important;
  font-weight: 500;
  font-size: 1rem;
  margin-left: 1.5rem;
  padding: 0.5rem 1rem;
  transition: all 0.3s ease;
}

.nav-link:hover {
  color: rgba(255,255,255,0.85) !important;
  transform: translateY(-1px);
}

/* HomeView가 들어가는 컨텐츠 영역 */
.content {
  /* overflow-y: auto; 세로 스크롤 활성화 */
  flex-grow: 1; /* 남은 공간을 모두 차지하도록 설정 */
}

</style>