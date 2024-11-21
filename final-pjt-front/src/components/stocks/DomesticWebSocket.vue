<template>
  <div>
    <h1>실시간 주가 차트 - 국내주식</h1>
    <apexchart
      width="800"
      height="400"
      type="line"
      :options="chartOptions"
      :series="series"
    ></apexchart>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { ref, onMounted, onUnmounted } from 'vue'
import VueApexCharts from 'vue3-apexcharts'

// url에서 주식코드 가져옴
const stockcodeProps = defineProps({ stockcode:String })
const authStore = useAuthStore()

const chartOptions = ref({
  chart: {
    id: 'realtime-stock-chart',
    animations: {
      enabled: true,
      easing: 'linear',
    },
    toolbar: {
      show: false
    },
    zoom: {
      enabled: false
    }
  },
  stroke: {
    curve: 'smooth',
    width: 2,
    lineCap: 'round',
  },
  title: {
    text: '실시간 주가',
    align: 'left',
  },
  xaxis: {
    type: 'datetime',
    labels: {
      datetimeFormatter: {
        hour: 'HH:mm:ss'
      }
    }
  },
  yaxis: {
    labels: {
      formatter: (value) => Math.round(value).toLocaleString()
    },
    min: (min) => parseInt(min * 0.95), // 최소값보다 5% 낮게
    max: (max) => parseInt(max * 1.05), // 최대값보다 5% 높게
    // floating: false,
    // decimalsInFloat: false
  },
  tooltip: {
    x: {
      format: 'HH:mm:ss'
    }
  }
})

const series = ref([{
  name: '주가',
  data: []
}])


//////////////// 실시간 웹소켓 통신 데이터 받는 코드


const socket = ref(null)
let isRunning = true

const stockspurchaseDomestic = (data) => {
  const pValue = data.split('^')
  const price = parseInt(pValue[2])
  // 시간 문자열을 타임스탬프로 변환
  const timestamp = new Date().getTime() + (9 * 60 * 60 * 1000)
  
  // NaN 체크 및 처리
  if (isNaN(price)) {
    console.warn('Invalid price value received:', pValue[2])
    return null // 유효하지 않은 데이터는 null 반환
  }
  
  return {
    timestamp: timestamp,
    price: price
  }
}

const updateChartData = (newData) => {
  // null 체크 추가
  if (!newData || newData.price === null) {
    return // 유효하지 않은 데이터는 무시
  }

  // 데이터 포인트를 추가하기 전에 유효성 검사
  if (isFinite(newData.price)) {
    // 데이터 포인트를 [timestamp, price] 형태로 추가
    series.value[0].data.push([newData.timestamp, newData.price])

    // // 최대 데이터 포인트 수 유지
    // if (series.value[0].data.length > MAX_DATA_POINTS) {
    //   series.value[0].data.shift()
    // }

    // 시리즈 강제 업데이트
    series.value = [{
      name: '주가',
      data: [...series.value[0].data]
    }]
  }
}

const sendMessage = () => {
  if (socket.value && socket.value.readyState === WebSocket.OPEN) {
    socket.value.send(JSON.stringify({
      header: {
        approval_key: authStore.websocketToken,
        custtype: "P",
        tr_type: "1",
        content_type: "utf-8"
      },
      body: {
        input: {
          tr_id: "H0STCNT0",
          tr_key: stockcodeProps.stockcode
        }
      }
    }))
  }
}

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms))


const receiveMessage = () => {
  return new Promise((resolve) => {
    socket.value.onmessage = (event) => {
      try {
        const processedData = stockspurchaseDomestic(event.data)
        if (processedData) { // null이 아닐 때만 처리
          updateChartData(processedData)
          console.log('Processed Data:', processedData)
        }
        resolve(processedData)
      } catch (error) {
        console.error('Data processing error:', error)
        resolve(null)
      }
    }
  })
}

const dataFetchLoop = async () => {
  sendMessage()
  while (isRunning) {
    await receiveMessage()
    await sleep(3000) // 3초 대기
  }
}


onMounted(() => {
  // console.log(authStore.websocketToken)
  socket.value = new WebSocket('ws://ops.koreainvestment.com:21000')

  socket.value.onopen = () => {
    console.log('WebSocket 연결이 열렸습니다.')
    dataFetchLoop()
  }

  socket.value.onerror = (error) => {
    console.error('WebSocket 오류:', error)
  }

  socket.value.onclose = () => {
    console.log('WebSocket 연결이 닫혔습니다.')
    isRunning = false
  }
})

onUnmounted(() => {
  isRunning = false
  if (socket.value) {
    socket.value.close()
  }
})
</script>

<style scoped>
</style>