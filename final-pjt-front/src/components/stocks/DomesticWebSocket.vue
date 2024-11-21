<template>
  <div>
    <h1>실시간 주가 차트 - 국내주식</h1>
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
</style>