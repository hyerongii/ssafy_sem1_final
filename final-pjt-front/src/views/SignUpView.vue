<template>
  <div class="signup-container">
    <div class="signup-box">
      <div class="signup-header">
        <h2>Welcome!</h2>
        <p class="text-muted">새로운 투자 여정을 시작하세요</p>
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
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.signup-box {
  background: white;
  border-radius: 15px;
  padding: 40px;
  box-shadow: 0 15px 25px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 500px;
}

.signup-header {
  text-align: center;
  margin-bottom: 40px;
}

.signup-header h2 {
  color: #2d3748;
  margin-bottom: 10px;
  font-weight: 600;
}

.form-floating input {
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.form-floating input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102,126,234,0.25);
}

.signup-btn {
  background: linear-gradient(to right, #667eea, #764ba2);
  border: none;
  padding: 15px;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.signup-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102,126,234,0.4);
}

a {
  color: #667eea;
}

a:hover {
  color: #764ba2;
}
</style>