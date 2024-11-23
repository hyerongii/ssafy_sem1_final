import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const router = useRouter()
  const websocketToken = ref(null)
  const user = ref(null)
  
  const signUp = function (payload) {
    const {username, password1, password2, email, nickname } = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2, email, nickname
      }
    })
      .then((res) => {
        console.log(res)
        console.log('회원가입 성공')

        // 회원가입 성공 후 자동 로그인
        const password = password1
        logIn({username, password})
      })
      .catch((err) => {
        console.log(err)
      })
  }
  
  const logIn = function (payload) {
    const {username, password} = payload

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then((res) => {
        token.value = res.data.access
        console.log(res.data)
        // 로그인 성공하면 다음 페이지로 이동 가능하게,,!
        router.push({ name: 'HomeView'})
      })
      .catch((err) => {
        console.log(err)
      })

    axios({
      method:'get',
      url: `${API_URL}/api/v1/token/`,
    })
      .then((res) => {
        // 받아온 토큰 데이터 출력
        websocketToken.value = res.data.websocket_token

      })
      .catch((err) => {
        console.log(err)
      })
  }

  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(() => {
        // 로그아웃 성공 처리
        token.value = null
        // 로컬 스토리지나 쿠키에 저장된 토큰 제거
        localStorage.removeItem('token')
        user.value = null  // 로그아웃 시 사용자 정보도 초기화
        // 홈 페이지나 로그인 페이지로 리다이렉트
        router.push({ name: 'HomeView' })
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const isAuthenticated = computed(() => !!token.value)

  return { signUp, logIn, logOut, API_URL, token, isAuthenticated, websocketToken, user }
},{persist: true}
)
