<template>
  <div>
    <h1>실시간 주가 차트</h1>
    <apexchart
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

const chartOptions = ref({
  chart: {
    id: 'realtime-stock-chart',
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
    // min: (min) => parseInt(min * 0.99),
    // max: (max) => parseInt(max * 1.01),
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

// 초기 데이터 로드를 위한 watcher
watch(
  () => stockItemStore.dayChartData,
  (newData) => {
    if (newData && Array.isArray(newData)) {
      series.value[0].data = newData.map(item => ({
        x: item.time,
        y: item.price
      }))

    }
  },
  { immediate: true }
)

// 실시간 데이터 업데이트를 위한 watcher
watch(
  () => websocketStore.processedData,
  (newData) => {
    if (newData && newData.price && isFinite(newData.price)) {
      series.value[0].data.push([newData.timestamp, newData.price])
      series.value = [{
        name: '주가',
        data: [...series.value[0].data]
      }]
    }
  }
)

// onMounted(async () => {
//   // 초기 데이터 로드
//   await stockItemStore.getDayInfo(stockcodeProps.stockcode)
  
//   // 웹소켓 연결 시작
//   websocketStore.webSocketStart(stockcodeProps.stockcode)
// })

onUnmounted(() => {
  if (websocketStore.socket) {
    websocketStore.socket.close()
  }
})
</script>

<!-- <template>
  <div>
    <h1>실시간 주가 차트</h1>
    <apexchart
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
import { ref, computed, onMounted, watch } from 'vue'

// url에서 주식코드 가져옴
const stockcodeProps = defineProps({ stockcode:String })

const stockItemStore = useStockItemStore()
// const dayChartData = stockItemStore.dayChartData


const chartOptions = ref({
  chart: {
    id: 'realtime-stock-chart',
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
    // min: (min) => parseInt(min * 0.95), // 최소값보다 5% 낮게
    // max: (max) => parseInt(max * 1.05), // 최대값보다 5% 높게
  },
  tooltip: {
    x: {
      format: 'HH:mm:ss'
    }
  }
})


const series = computed(() => {
  if (!stockItemStore.dayChartData || !Array.isArray(stockItemStore.dayChartData)) {
    return [{
      name: '시가',
      data: []
    }]
  }

  return [{
    name: '시가',
    data: stockItemStore.dayChartData.map(item => ({
      x: item.time,
      y: item.price
    }))
  }]
})

</script>

<style scoped>
</style> -->