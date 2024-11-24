<template>
  <div class="signup-container">
    <div class="signup-box">
      <div class="signup-header">
        <h2>환영해요!</h2>
        <p class="text-muted">새로운 투자 여정을 주주랜드에서 시작하세요</p>
      </div>
      
      <form @submit.prevent="signUp" class="signup-form">
        <div class="form-floating mb-3">
          <input 
            type="text" 
            class="form-control" 
            id="input_id" 
            placeholder="아이디"
            v-model.trim="username"
          >
          <label for="input_id">아이디</label>
        </div>

        <div class="form-floating mb-3">
          <input 
            type="password" 
            class="form-control" 
            id="input_password1" 
            placeholder="비밀번호"
            v-model.trim="password1"
          >
          <label for="input_password1">비밀번호</label>
        </div>

        <div class="form-floating mb-3">
          <input 
            type="password" 
            class="form-control" 
            id="input_password2" 
            placeholder="비밀번호 확인"
            v-model.trim="password2"
          >
          <label for="input_password2">비밀번호 확인</label>
        </div>

        <div class="form-floating mb-3">
          <input 
            type="email" 
            class="form-control" 
            id="input_email" 
            placeholder="이메일"
            v-model.trim="email"
          >
          <label for="input_email">이메일</label>
        </div>

        <div class="form-floating mb-4">
          <input 
            type="text" 
            class="form-control" 
            id="input_nickname" 
            placeholder="닉네임"
            v-model.trim="nickname"
          >
          <label for="input_nickname">닉네임</label>
        </div>

        <div class="d-grid gap-2">
          <button type="submit" class="btn btn-primary btn-lg signup-btn">시작하기</button>
        </div>

        <div class="text-center mt-3">
          <span class="text-muted">이미 계정이 있으신가요?</span>
          <a @click="moveLogIn" class="text-decoration-none ms-2">로그인</a>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const store = useAuthStore()
const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const email = ref(null)
const nickname = ref(null)

const signUp = function () {
  const payload =  {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    email: email.value,
    nickname: nickname.value
  }
  store.signUp(payload)
}

const moveLogIn = function () {
  router.push({name:'LogInView'})
}
</script>

<style scoped>
.signup-container {
  min-height: calc(100vh - 64px);
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8faf5, #fff);
  padding: 20px;
  margin-top: 64px;
  font-family: 'Godo', sans-serif;
}

.signup-box {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 8px 20px rgba(139, 193, 72, 0.1);
  width: 100%;
  max-width: 500px;
}

.signup-header {
  text-align: center;
  margin-bottom: 40px;
}

.signup-header h2 {
  color: var(--primary-color);
  margin-bottom: 10px;
  font-weight: 600;
  font-size: 2rem;
}

.text-muted {
  color: #666 !important;
  font-size: 1.1rem;
}

.form-floating input {
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  padding: 1rem;
  font-size: 1rem;
  margin-bottom: 1rem;
}

.form-floating input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 0.2rem rgba(139, 193, 72, 0.2);
}

.signup-btn {
  background-color: var(--primary-color);
  border: none;
  padding: 15px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  margin-top: 1rem;
}

.signup-btn:hover {
  transform: translateY(-2px);
  filter: brightness(1.1);
  box-shadow: 0 5px 15px rgba(139, 193, 72, 0.3);
}

a {
  color: var(--primary-dark);
  cursor: pointer;
  font-weight: 500;
}

a:hover {
  color: var(--primary-color);
}

.mt-3 {
  margin-top: 2rem !important;
}
</style>