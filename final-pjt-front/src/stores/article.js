import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from './auth'

export const useArticleStore = defineStore('article', () => {
  const authstore = useAuthStore()
  const userMbti = ref(null)

  const getUserInfo = function () {
    console.log(authstore.user.pk)
    axios({
      //사용자 정보 요청
      method: 'get',
      url: `${authstore.API_URL}/api/v1/user_info/${authstore.user.pk}/`,
      headers: {
        Authorization: `Bearer ${authstore.token}`,
      },
    })
      .then((res) => {
        console.log(res.data)
      })
      .catch((err) => {
        console.log(err)
      })
  }
  
  return { getUserInfo, userMbti }
},{persist: true})