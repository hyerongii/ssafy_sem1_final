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
  const url = ref('')

  const getDayInfo = function (stockCode, currentTime) { 
    const endpoint = isNaN(stockCode) ? 'o_chart_and_data' : 'd_chart_and_data'
      
    axios({
        //국내
        method: 'post',
        url: `${authStore.API_URL}/api/v1/stock/${endpoint}/`,
        headers: {
          Authorization: `Bearer ${authStore.token}`,
        },
        data: {
          stock_code : stockCode,
          // 숫자형태(국내)면 current_time 추가
          ...(!isNaN(stockCode) && { current_time: currentTime })
        },
      })
        .then((res) => {
          console.log('당일 차트 데이터 받음')
          console.log(res.data)
          // dayChartData.value = res.data.chart_data
          // websocketStore.webSocketStart(stockCode)
        })
        .catch((err) => {
          console.log(err)
        })
    
  }

  return {getDayInfo, dayChartData}
}
// ,{persist: true}
)