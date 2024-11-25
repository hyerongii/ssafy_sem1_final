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
        speed: 350  // 애니메이션 속도를 더 빠르게
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
      datetimeUTC: false,
      format: 'HH:mm:ss',
      formatter: function(value) {
        const date = new Date(value);
        return date.toLocaleTimeString('ko-KR', {
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: false
        });
      },
    },
    tooltip : false,
    axisTicks: {
      show: false
    }
  },
  yaxis: {
    labels: {
      formatter: (value) => Math.round(value).toLocaleString()
    },
    min: (min) => parseInt(min * 0.999),
    max: (max) => parseInt(max * 1.001),
  },
  tooltip: {
    x: {
      show: true
    },
    y: {
      title: {
        formatter: () => '체결가: ' // 툴팁 타이틀 설정
      },
      formatter: (value) => `${Math.round(value).toLocaleString()}원` // 가격 포맷 설정
    }
  }
})

// 초기 차트 데이터 설정
watch(
  () => stockItemStore.dayChartData,
  (newData) => {
    if (newData && Array.isArray(newData)) {
      const formattedData = newData.map(item => {
        // 시간 문자열을 파싱
        const timeStr = item.time;
        const hours = timeStr.substring(0, 2);
        const minutes = timeStr.substring(2, 4);
        const seconds = timeStr.substring(4, 6);
        
        // 오늘 날짜 기준으로 timestamp 생성
        const today = new Date();
        const timestamp = new Date(
          today.getFullYear(),
          today.getMonth(),
          today.getDate(),
          parseInt(hours),
          parseInt(minutes),
          parseInt(seconds)
        ).getTime();

        return {
          x: timestamp,
          y: isNaN(Number(stockcode)) 
            ? parseFloat(item.price) * 1405 
            : parseFloat(item.price)
        }
      })

      currentSeries.value[0].data = formattedData
      
      // 웹소켓 연결 시작
      websocketStore.webSocketStart(stockcode)
    }
  },
  { immediate: true }
)

// series computed 속성 수정
const series = computed(() => [{
  name: '주가',
  data: currentSeries.value[0].data
}])


// 실시간 데이터 업데이트
watch(
  () => websocketStore.processedData,
  (newData) => {
    if (newData && newData.price && isFinite(newData.price)) {
      // 시간 문자열을 올바른 Date 객체로 변환
      const timeStr = newData.time;
      const hours = timeStr.substring(0, 2);
      const minutes = timeStr.substring(2, 4);
      const seconds = timeStr.substring(4, 6);
      
      const today = new Date();
      const timestamp = new Date(
        today.getFullYear(),
        today.getMonth(),
        today.getDate(),
        parseInt(hours),
        parseInt(minutes),
        parseInt(seconds)
      ).getTime();
      
      const price = isNaN(Number(stockcode))
        ? parseFloat(newData.price) * 1405
        : parseFloat(newData.price)
      
      currentSeries.value[0].data.push({
        x: timestamp,
        y: price
      })

      // ApexCharts 업데이트
      if (chart.value) {
        chart.value.updateSeries([{
          data: currentSeries.value[0].data
        }])
      }
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
.chart-wrapper {
  width: 100%;
  height: 100%;
  min-height: calc(100vh - 300px);
}
</style>