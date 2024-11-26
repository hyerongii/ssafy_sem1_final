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
    fontFamily: 'Godo, sans-serif',
    background: 'transparent',
    animations: {
      enabled: true,
      easing: 'linear',
      dynamicAnimation: {
        speed: 500
      }
    },
    toolbar: {
      show: false
    },
    zoom: {
      enabled: false
    }
  },
  markers: {
    // size: 0,  // 기본 마커 크기는 0으로 설정
    discrete: [{
      seriesIndex: 0,
      dataPointIndex: -1,  // 마지막 포인트
      fillColor: '#FFF',
      strokeColor: 'var(--primary-dark)',
      size: 3,
      shape: "circle",  // circle, square, rect 등 선택 가능
      pulsing: true,  // 펄싱 효과 활성화
    }]
  },
  colors: ['var(--primary-dark)'],
  dataLabels: {
    enabled: false
  },
  stroke: {
    curve: 'smooth',
    width: 3,
    lineCap: 'round',
    colors: ['var(--primary-dark)']
  },
  title: {
    text: '실시간 주가',
    align: 'left',
    style: {
      fontSize: '1.2rem',
      fontWeight: 600,
      fontFamily: 'Godo, sans-serif',
      color: 'var(--primary-word)'
    },
    margin: 40 // 제목 여백 추가
  },
  grid: {
    borderColor: 'rgba(139, 193, 72, 0.1)',
    strokeDashArray: 3
  },
  xaxis: {
    type: 'datetime',
    min: new Date().setHours(9, 0, 0, 0), // 오전 9시
    max: new Date().setHours(15, 30, 0, 0), // 오후 3시 30분
    labels: {
      style: {
        colors: 'var(--primary-word)',
        fontFamily: 'Godo, sans-serif'
      },
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
      }
    },
    tickAmount: 6, // x축 눈금 개수 조정
    tooltip: {
      enabled: false  // X축 툴팁 완전히 비활성화
    },
    axisBorder: {
      color: 'rgba(139, 193, 72, 0.2)'
    },
    axisTicks: {
      color: 'rgba(139, 193, 72, 0.2)'
    }
  },
  yaxis: {
    labels: {
      formatter: (value) => Math.round(value).toLocaleString(),
      style: {
        colors: 'var(--primary-word)',
        fontFamily: 'Godo, sans-serif'
      }
    },
    min: (min) => parseInt(min * 0.995),
    max: (max) => parseInt(max * 1.005)
  },
  tooltip: {
    theme: 'light',
    style: {
      fontSize: '12px',
      fontFamily: 'Godo, sans-serif'
    },
    x: {
      show: true,
      format: 'HH:mm:ss'
    },
    y: {
      title: {
        formatter: () => '체결가: '
      },
      formatter: (value) => `${Math.round(value).toLocaleString()}원`
    }
  },
})

// 초기 차트 데이터 설정
// watch(
//   () => stockItemStore.dayChartData,
//   (newData) => {
//     if (newData && Array.isArray(newData)) {
//       const formattedData = newData.map(item => {
//         const timeStr = item.time;
//         const hours = timeStr.substring(0, 2);
//         const minutes = timeStr.substring(2, 4);
//         const seconds = timeStr.substring(4, 6);
        
//         const today = new Date();
//         const timestamp = new Date(
//           today.getFullYear(),
//           today.getMonth(),
//           today.getDate(),
//           parseInt(hours),
//           parseInt(minutes),
//           parseInt(seconds)
//         ).getTime();

//         return {
//           x: timestamp,
//           y: isNaN(Number(stockcode)) 
//             ? parseFloat(item.price) * 1405 
//             : parseFloat(item.price)
//         }
//       }).sort((a, b) => a.x - b.x) // 시간순으로 정렬

//       currentSeries.value[0].data = formattedData
      
//       if (!isNaN(stockcode)) {
//         websocketStore.webSocketStart(stockcode)
//       }
//     }
//   },
//   { immediate: true }
// )

// 차트 옵션 설정을 동적으로 변경하는 함수
const getChartOptions = (isUSStock) => {
  const today = new Date()
  
  const xaxisConfig = {
    min: new Date().setHours(9, 30, 0, 0), // 오전 9시
    max: new Date().setHours(16, 0, 0, 0) // 오후 3시 30분
  }

  return {
    ...chartOptions.value,
    xaxis: {
      ...chartOptions.value.xaxis,
      ...xaxisConfig,
      labels: {
        ...chartOptions.value.xaxis.labels,
        formatter: function(value) {
          const date = new Date(value)
          return date.toLocaleTimeString('ko-KR', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
          })
        }
      }
    }
  }
}

// 초기 차트 데이터 설정 시 차트 옵션 업데이트
watch(
  () => stockItemStore.dayChartData,
  (newData) => {
    if (newData && Array.isArray(newData)) {
      const isUSStock = isNaN(Number(stockcode))
      chartOptions.value = getChartOptions(isUSStock)
      
      const formattedData = newData.map(item => {
        const timeStr = item.time
        const hours = timeStr.substring(0, 2)
        const minutes = timeStr.substring(2, 4)
        const seconds = timeStr.substring(4, 6)
        
        const today = new Date()
        const timestamp = new Date(
          today.getFullYear(),
          today.getMonth(),
          today.getDate(),
          parseInt(hours),
          parseInt(minutes),
          parseInt(seconds)
        ).getTime()

        return {
          x: timestamp,
          y: isUSStock 
            ? parseFloat(item.price) * 1405 
            : parseFloat(item.price)
        }
      }).sort((a, b) => a.x - b.x)

      currentSeries.value[0].data = formattedData
      
      if (!isUSStock) {
        websocketStore.webSocketStart(stockcode)
      }
    }
  },
  { immediate: true }
)



// series computed 속성 수정
const series = computed(() => [{
  name: '주가',
  data: currentSeries.value[0].data
}])


// 실시간 데이터 업데이트 최적화
watch(
  () => websocketStore.processedData,
  (newData) => {
    if (newData?.price && isFinite(newData.price)) {
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
      
      // 중복 데이터 체크 및 제거
      const existingDataIndex = currentSeries.value[0].data.findIndex(
        item => item.x === timestamp
      )
      
      if (existingDataIndex !== -1) {
        // 같은 시간의 데이터가 있으면 업데이트
        currentSeries.value[0].data[existingDataIndex].y = price
      } else {
        // 새로운 데이터 추가
        currentSeries.value[0].data.push({
          x: timestamp,
          y: price
        })
      }

      // 차트 업데이트
      if (chart.value) {
        chart.value.updateSeries([{
          data: currentSeries.value[0].data
        }], true, false) // animate=true, updateAllSeries=false

        // // 마지막 데이터 포인트의 마커 업데이트
        // chart.value.updateOptions({
        //   markers: {
        //     size: 0,
        //     discrete: [{
        //       seriesIndex: 0,
        //       dataPointIndex: currentSeries.value[0].data.length - 1,
        //       fillColor: '#FFF',
        //       strokeColor: 'var(--primary-dark)',
        //       size: 6,
        //       shape: "circle"
        //     }]
        //   }
        // })
      }


    }
  }
)

onUnmounted(() => {
  stopWebSocket()
})

// DayStockChart.vue
const stopWebSocket = () => {
  if (websocketStore.socket) {
    websocketStore.webSocketClose()
  }
}

// 라우트가 변경될 때도 웹소켓 종료
watch(() => route.params.stock_id, (newId, oldId) => {
  if (newId !== oldId) {
    stopWebSocket()
  }
})

</script>


<style scoped>
.chart-wrapper {
  width: 100%;
  height: 100%;
  min-height: calc(100vh - 300px);
  font-family: 'Godo', sans-serif;
  padding: 1rem;
  background: white;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.chart-wrapper:hover {
  box-shadow: 0 4px 12px rgba(237, 145, 156, 0.1);
}
</style>