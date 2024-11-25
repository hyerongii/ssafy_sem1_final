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
  const periodChart = ref([])
  const stockInfo = ref({})
  const articles = ref([])


  const getDayInfo = function (stockCode, currentTime) { 
    const endpoint = isNaN(stockCode) ? 'o_chart' : 'd_chart'
      
    axios({
        //통합
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
          console.log('당일 차트 데이터')
          console.log(res.data)
          dayChartData.value = res.data.chart_data
        })
        // .then((res) => {
        //   websocketStore.webSocketStart(stockCode)
        // })
        .catch((err) => {
          console.log(err)
        })
    
  }

  const getPeriodInfo = function (stockCode, period) { 
    const endpoint = isNaN(stockCode) ? 'o_chart_period' : 'd_chart_period'

    axios({
      method : 'post',
      url : `${authStore.API_URL}/api/v1/stock/${endpoint}/`,
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
      data: {
        stock_code : stockCode,
        // period 넣어주기
        period : period,
      },
    })
      .then((res) => {
        // console.log(res.data)
        periodChart.value = res.data.chart_data
        console.log(periodChart.value)
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const getArticleInfo = function (stockCode, currentTime){
    const endpoint = isNaN(stockCode) ? 'o_main_data' : 'd_main_data'

    axios({
        //통합
        method: 'post',
        url: `${authStore.API_URL}/api/v1/stock/${endpoint}/`,
        headers: {
          Authorization: `Bearer ${authStore.token}`,
        },
        data: {
          stock_code : stockCode,
          // 숫자형태(국내)면 current_time 추가
          // stock_id :
          ...(!isNaN(stockCode) && { current_time: currentTime })
        },
      })
        .then((res) => {
          console.log('게시글 정보')
          console.log(res.data)
          articles.value = res.data
        })
        .catch((err) => {
          console.log(err)
        })
  }

  const getStockInfo = function (stockCode, currentTime) {
    // 한 번만 결정되도록 먼저 체크
    const isNumeric = !isNaN(stockCode)
    const endpoint = isNumeric ? 'd_main_data' : 'o_main_data'
    
    const data = {
      stock_code: stockCode,
      ...(isNumeric && { current_time: currentTime })
    }
  
    axios({
      method: 'post',
      url: `${authStore.API_URL}/api/v1/stock/${endpoint}/`,
      headers: {
        Authorization: `Bearer ${authStore.token}`,
      },
      data
    })
    .then((res) => {
      console.log('주식종목정보')
      console.log(res.data)
      stockInfo.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
  }

  return {getDayInfo, dayChartData, getPeriodInfo, getStockInfo, getArticleInfo, periodChart, stockInfo, articles}
}
// ,{persist: true}
)