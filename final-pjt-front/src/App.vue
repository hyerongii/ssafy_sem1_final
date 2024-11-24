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

<style scoped>

/* 전체 페이지 레이아웃 */
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh; /* 전체 화면 높이 */
}

/* 네비게이션 링크 스타일 */
.nav-link {
  text-decoration: none; /* 밑줄 없애기 */
  color: black; /* 글자 색상 검정으로 */
  font-weight: bold; /* 글자 굵게 (선택 사항) */
  margin-left: 1rem
  
}

.nav-link:hover {
  color: #555; /* 마우스를 올렸을 때 색상 변경 (선택 사항) */
}

/* HomeView가 들어가는 컨텐츠 영역 */
.content {
  /* overflow-y: auto; 세로 스크롤 활성화 */
  flex-grow: 1; /* 남은 공간을 모두 차지하도록 설정 */
}

</style>