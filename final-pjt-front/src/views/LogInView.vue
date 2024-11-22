<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h2>Welcome Back!</h2>
        <p class="text-muted">당신의 투자 여정을 시작하세요</p>
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
        <div class="d-grid gap-2">
          <button type="submit" class="btn btn-primary btn-lg">로그인</button>
        </div>
        <!-- <div class="text-center mt-3">
          <a href="#" class="text-muted text-decoration-none">비밀번호를 잊으셨나요?</a>
        </div> -->
      </form>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { ref } from 'vue'

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
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-box {
  background: white;
  border-radius: 10px;
  padding: 40px;
  box-shadow: 0 15px 25px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-header h2 {
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

.btn-primary {
  background: linear-gradient(to right, #667eea, #764ba2);
  border: none;
  padding: 12px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102,126,234,0.4);
}
</style>
