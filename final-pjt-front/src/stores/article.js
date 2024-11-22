import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from './auth'

export const useStockItemStore = defineStore('article', () => {
  const store = useAuthStore()

  axios({
    //백에서 받아오기
    method: 'post',
    url: `${store.API_URL}/api/v1/stock/indus_chart/`,
    headers: {
      Authorization: `Bearer ${store.token}`,
    },
    data: {

    },
  })
    .then((res) => {
      console.log(res.data)
    })
    .catch((err) => {
      console.log(err)
    })

  
  return {}
})