<template>
  <div>
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
import { useStockStore } from '@/stores/stock'
import { computed, ref } from 'vue'

const stockStore = useStockStore()

// 차트 기본 옵션 설정
const chartOptions = {
  chart: {
    type: 'line',
    toolbar: {
      show: false // 상단 툴바 숨김
    },
    zoom: {
      enabled: false // 줌 기능 비활성화
    }
  },
  grid: {
    show: false // 그리드 숨김
  },
  stroke: {
    curve: 'smooth', // 부드러운 곡선
    width: 3,
    lineCap: 'round',
    smoothing: 0.2 
  },
  colors: ['#F78CA0'],
  xaxis: {
    labels: {
      show: false // x축 라벨 숨김
    },
    axisBorder: {
      show: false // x축 선 숨김
    },
    axisTicks: {
      show: false // x축 틱 숨김
    }
  },
  yaxis: {
    labels: {
      show: false // y축 라벨 숨김
    },
    axisBorder: {
      show: false // y축 선 숨김
    }
  },
  tooltip: {
    enabled: false // 툴팁 비활성화
  }
}

// 차트 데이터 설정
const series = computed(() => [{
  name: 'Stock Price',
  data: stockStore.chartdata.map(item => ({
    x: item.date,
    y: item.average_close
  }))
}])
</script>

<style scoped>
</style>