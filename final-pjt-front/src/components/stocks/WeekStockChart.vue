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
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const stockItemStore = useStockItemStore()
const route = useRoute()
const stockcode = route.params.stock_id

const chartOptions = ref({
  chart: {
    id: 'realtime-stock-chart',
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
    text: '1주 주가',
    align: 'left',
  },
  xaxis: {
    type: 'datetime',
    labels: {
      show: false
    },
    axisTicks: {
      show: false
    },
    tooltip: {
      enabled: false  // X축 툴팁 완전히 비활성화
    }
  },
  colors: ['#F78CA0'],
  yaxis: {
    labels: {
      formatter: (value) => Math.round(value).toLocaleString()
    },
    min: (min) => parseInt(min * 0.99),
    max: (max) => parseInt(max * 1.01),
  },
  tooltip: {
    x: {
      format: 'yyyy.MM.dd'
    },
    y: {
      title: {
        formatter: () => '종가: ' // 툴팁 타이틀 설정
      },
      formatter: (value) => `${Math.round(value).toLocaleString()}원` // 가격 포맷 설정
    }
  }
})

const series = computed(() => [{
  name: 'Stock Price',
  data: stockItemStore.periodChart?.map(item => ({
    // YYYYMMDD 형식의 문자열을 Date 객체로 변환
    x: new Date(
      item.date.substring(0, 4),
      parseInt(item.date.substring(4, 6)) - 1,
      item.date.substring(6, 8)
    ).getTime(),
    // 숫자를 안전하게 변환
    y: isNaN(Number(stockcode)) 
      ? parseFloat(item.clpr) * 1405 
      : parseFloat(item.clpr)
  })) || []
}])
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 100%;
  min-height: calc(100vh - 300px);
}
</style>