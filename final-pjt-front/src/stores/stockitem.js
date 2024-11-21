import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from './auth'

export const useStockItemStore = defineStore('stock', () => {
  const authStore = useAuthStore()

  const getDayInfo = function (stockCode, currentTime) {
    axios({
      //백에서 받아오기
      method: 'post',
      url: `${authStore.API_URL}/api/v1/stock/chart_and_data/`,
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
      data: {
        stock_code : stockCode,
        current_time : currentTime
      },
    })
      .then((res) => {
        console.log(res.data)
      })
      .catch((err) => {
        console.log(err)
      })
  }
  return {getDayInfo}
}
// ,{persist: true}
)