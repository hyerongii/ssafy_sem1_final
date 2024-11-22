<template>
  <div>
    <h1>실시간 주가 차트</h1>
    <apexchart
      ref="chart"
      width="1000"
      height="400"
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

const stockcodeProps = defineProps({ stockcode: String })
const stockItemStore = useStockItemStore()
const websocketStore = useWebsocketStore()
const chart = ref(null)

const chartOptions = ref({
  chart: {
    id: 'realtime-stock-chart',
    events: {},
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
  markers: { // 이 부분 추가
    size: 0
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
      datetimeFormatter: {
        hour: 'HH:mm:ss'
      }
    }
  },
  yaxis: {
    labels: {
      formatter: (value) => Math.round(value).toLocaleString()
    },
    min: (min) => parseInt(min * 0.99),
    max: (max) => parseInt(max * 1.01),
  },
  tooltip: {
    x: {
      format: 'HH:mm:ss'
    }
  }
})

// const series = ref([{
//   name: '주가',
//   data: []
// }])


// 초기 데이터 로드를 위한 watcher
// watch(
//   () => stockItemStore.dayChartData,
//   (newData) => {
//     if (newData && Array.isArray(newData)) {
//       const formattedData = newData.map(item => ({
//         x: new Date(item.time).getTime(), // timestamp로 변환
//         y: parseFloat(item.price)
//       }))
//       series.value = [{
//         name: '주가',
//         data: formattedData
//       }]
//     }
//   },
//   { immediate: true }
// )

const series = computed(() => [{
  name: '주가',
  data: stockItemStore.dayChartData.map(item => ({
    x: new Date(item.time).getTime(), // timestamp로 변환
    y: parseFloat(item.price)
  }))
}])


// 실시간 데이터 업데이트를 위한 watcher
watch(
  () => websocketStore.processedData,
  (newData) => {
    if (newData && newData.price && isFinite(newData.price)) {
      const timestamp = new Date(newData.time).getTime()
      series.value[0].data.push({
        x: timestamp,
        y: parseFloat(newData.price)
      })

      // 전체 series 업데이트
      // series.value = [...series.value]
    }
  }
)

onUnmounted(() => {
  if (websocketStore.socket) {
    websocketStore.socket.close()
  }
})
</script>


<style scoped>
</style>