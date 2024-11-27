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
        // alert('회원가입 성공! 개인화된 테마를 추천받아보세요!')
        // 회원가입 성공 후 자동 로그인
        const password = password1
        logIn({username, password})
      })
      .catch((err) => {
        console.log(err)
      })
  }
  
  const logIn = function (payload) {
    const { username, password } = payload;
    
    if (!username || !password) {
      alert('적절한 아이디와 비밀번호를 입력해주세요!');
      return;
    }

    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: { username, password },
    })
      .then((res) => {
        // 로그인 성공 처리
        token.value = res.data.access
        user.value = res.data.user
        console.log('로그인 성공:', res.data)

        axios({
          method: 'get',
          url: `${API_URL}/api/v1/token/`,
          headers: {
            Authorization: `Bearer ${token.value}`,
          },
        })
          .then((res) => {
            // console.log(res.data)
            console.log('웹소켓 토큰 발급 완료')
            websocketToken.value = res.data
          })
          .catch((err) => {
            console.log(err.data)
          })

        // 홈 화면으로 이동
        router.push({ name: 'HomeView' })
      })
      .catch((err) => {
        console.log(err)
        if (err.response) {
          const errorMessage = err.response.data.detail
          if (err.response.status === 404) {
            alert('등록되지 않은 아이디입니다.')
          } else if (err.response.status === 401) {
            alert('비밀번호가 올바르지 않습니다.')
          } else {
            alert('로그인 중 문제가 발생했습니다. 다시 시도해주세요.')
          }
        } else {
          console.error('네트워크 오류:', err)
          alert('서버와의 연결이 원활하지 않습니다. 잠시 후 다시 시도해주세요.')
        }
      })
  }

  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
      .then(() => {
        // 로그아웃 성공 처리
        token.value = null
        websocketToken.value = null
        alert('로그아웃 성공!')
        // 로컬 스토리지나 쿠키에 저장된 토큰 제거
        localStorage.removeItem('auth')
        localStorage.removeItem('interest')
        localStorage.removeItem('article')
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
