<template>
  <div class="chart-wrapper">
    <apexchart
      ref="chart"
      width="100%"
      height="100%"
      type="line"
      :options="chartOptions"
      :series="series"
    ></apexchart>
  </div>
</template>

<script setup>
import { useStockItemStore } from '@/stores/stockitem'
import { useWebsocketStore } from '@/stores/websocket'
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const stockcode = route.params.stock_id
const stockItemStore = useStockItemStore()
const websocketStore = useWebsocketStore()
const chart = ref(null)

const currentSeries = ref([{
  name: '주가',
  data: []
}])


const chartOptions = ref({
  chart: {
    id: 'realtime-stock-chart',
    events: {},
    height: '100%',
    animations: {
      enabled: true,
      easing: 'linear',
      dynamicAnimation: {
        speed: 1000
      }
    },
    toolbar: {
      show: false
    },
    zoom: {
      enabled: false
    }
  },
  dataLabels: { // 이 부분 추가
    enabled: false
  },
  stroke: {
    curve: 'smooth',
    width: 3,
    lineCap: 'round',
  },
  title: {
    text: '실시간 주가',
    align: 'left',
  },
  xaxis: {
    type: 'datetime',
    labels: {
      show: false,
    },
    axisTicks: {
      show: false
    },
    tooltip: {
      enabled: false  // X축 툴팁 완전히 비활성화
    }
  },
  yaxis: {
    labels: {
      formatter: (value) => Math.round(value).toLocaleString()
    },
    // min: (min) => parseInt(min * 0.99),
    // max: (max) => parseInt(max * 1.01),
  },
  tooltip: {
    x: {
      show: false // 툴팁의 X값 숨기기
    },
    y: {
      title: {
        formatter: () => '체결가: ' // 툴팁 타이틀 설정
      },
      formatter: (value) => `${Math.round(value).toLocaleString()}원` // 가격 포맷 설정
    }
  }
})


// 초기 차트 데이터 설정을 위한 computed 속성
const series = computed(() => [{
  name: '주가',
  data: currentSeries.value[0].data
}])

// 초기 데이터 로드를 위한 watcher
watch(
  () => stockItemStore.dayChartData,
  (newData) => {
    if (newData && Array.isArray(newData)) {
      const formattedData = newData.map(item => ({
        x: new Date(item.time).getTime(),
        y: isNaN(Number(stockcode)) 
          ? parseFloat(item.price) * 1405 
          : parseFloat(item.price)
      }))
      
      // 초기 데이터 설정
      currentSeries.value[0].data = formattedData
    }
  },
  { immediate: true }
)

// 실시간 데이터 업데이트를 위한 watcher
watch(
  () => websocketStore.processedData,
  (newData) => {
    if (newData && newData.price && isFinite(newData.price)) {
      const timestamp = new Date(newData.time).getTime()
      const price = isNaN(Number(stockcode))
        ? parseFloat(newData.price) * 1405
        : parseFloat(newData.price)
      
      // 새로운 데이터 추가
      currentSeries.value[0].data.push({
        x: timestamp,
        y: price
      })

      // // 데이터가 너무 많아지면 오래된 데이터 제거
      // if (currentSeries.value[0].data.length > 100) {
      //   currentSeries.value[0].data.shift()
      // }

      // ApexCharts 업데이트
      if (chart.value) {
        chart.value.updateSeries([{
          data: currentSeries.value[0].data
        }])
      }
    }
  }
)

onMounted(() => {
  // 컴포넌트 마운트 시 초기 데이터 로드
  if (stockItemStore.dayChartData.length === 0) {
    const currentTime = new Date().toLocaleTimeString('en-US', { 
      hour12: false, 
      hour: '2-digit', 
      minute: '2-digit', 
      second: '2-digit' 
    }).replace(/:/g, '')
    stockItemStore.getDayInfo(stockcode, currentTime)
  }
})


onUnmounted(() => {
  if (websocketStore.socket) {
    websocketStore.socket.close()
  }
})
</script>


<style scoped>
.chart-wrapper {
  width: 100%;
  height: 100%;
  min-height: calc(100vh - 300px);
}
</style>