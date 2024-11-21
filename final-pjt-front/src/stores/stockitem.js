import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from './auth'
import { useWebsocketStore } from './websocket'

export const useStockItemStore = defineStore('stockitem', () => {
  const authStore = useAuthStore()
  const dayChartData = ref([])
  const websocketStore = useWebsocketStore()

  const getDayInfo = function (stockCode, currentTime) {

    

    axios({
      //백에서 받아오기
      method: 'post',
      // url: `${authStore.API_URL}/api/v1/stock/d_chart_and_data/`,
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
        console.log('당일 차트 데이터 받음')
        console.log(res.data)
        dayChartData.value = res.data.chart_data
        websocketStore.webSocketStart(stockCode)
      })
      // .then(()=>{
      // })
      .catch((err) => {
        console.log(err)
      })
  }

  return {getDayInfo, dayChartData}
}
// ,{persist: true}
)