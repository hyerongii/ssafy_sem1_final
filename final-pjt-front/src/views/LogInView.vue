<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h2>또 오셨군요!</h2>
        <p class="text-muted">주주랜드에 오신걸 환영해요</p>
      </div>
      <form @submit.prevent="logIn" class="login-form">
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
        <div class="form-floating mb-4">
          <input 
            type="password" 
            class="form-control" 
            id="input_password" 
            placeholder="비밀번호"
            v-model.trim="password"
          >
          <label for="input_password">비밀번호</label>
        </div>
        <div class="button-group">
          <button type="submit" class="btn btn-primary btn-lg">로그인</button>
          <button @click.prevent="goToSignupPage" class="btn btn-secondary btn-lg">회원가입</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { ref } from 'vue'
// 진문수정
import { useRouter } from 'vue-router';
const router = useRouter()
const store = useAuthStore()
const username = ref(null)
const password = ref(null)

const logIn = function() {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.logIn(payload)
}

// 진문 수정 / 회원가입 페이지로 이동
const goToSignupPage = function () {
  router.push({name:'SignUpView'})
}
</script>

<style scoped>
.login-container {
  min-height: calc(100vh - 64px);
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8faf5, #fff);
  padding: 20px;
  margin-top: 64px;
  font-family: 'Godo', sans-serif;
}

.login-box {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 8px 20px rgba(139, 193, 72, 0.1);
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-header h2 {
  color: var(--primary-color);
  margin-bottom: 10px;
  font-weight: 600;
  font-size: 2rem;
}

.form-floating input {
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  padding: 1rem;
  font-size: 1rem;
}

.form-floating input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 0.2rem rgba(139, 193, 72, 0.2);
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 2rem;
}

.btn-primary {
  background-color: var(--primary-color);
  border: none;
  padding: 12px 30px;
  border-radius: 12px;
  transition: all 0.3s ease;
  font-weight: 600;
}

.btn-secondary {
  background-color: var(--primary-dark);
  border: none;
  padding: 12px 30px;
  border-radius: 12px;
  transition: all 0.3s ease;
  font-weight: 600;
}

.btn-primary:hover, .btn-secondary:hover {
  transform: translateY(-2px);
  filter: brightness(1.1);
}

.btn-lg {
  width: calc(50% - 7.5px);
  font-size: 1.1rem;
}

.text-muted {
  color: #666 !important;
  font-size: 1.1rem;
  margin-top: 0.5rem;
}
</style>
