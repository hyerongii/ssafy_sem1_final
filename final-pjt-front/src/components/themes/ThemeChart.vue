<template>
  <div class="chart-wrapper">
    <div class="chart-title">테마 주가 동향</div>
    <apexchart
      width="100%"
      height="100%"
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

const chartOptions = {
  chart: {
    type: 'line',
    toolbar: {
      show: false
    },
    zoom: {
      enabled: false
    },
    fontFamily: 'Godo, sans-serif',
    background: 'transparent'
  },
  grid: {
    show: true,
    borderColor: '#f1f1f1',
    strokeDashArray: 3,
    position: 'back'
  },
  stroke: {
    curve: 'smooth',
    width: 3,
    lineCap: 'round',
    colors: ['var(--primary-dark)']
  },
  colors: ['var(--primary-dark)'],
  xaxis: {
    labels: {
      show: false,
    },
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false
    }
  },
  yaxis: {
    labels: {
      show: false
    }
  },
  tooltip: {
    enabled: false,
  }
}

const series = computed(() => [{
  name: '평균 종가',
  data: stockStore.chartdata.map(item => ({
    x: item.date,
    y: item.average_close
  }))
}])
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 400px;
  padding: 1.5rem;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(237, 145, 156, 0.1);
  transition: all 0.3s ease;
  position: relative;
}

.chart-wrapper:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(237, 145, 156, 0.15);
}

.chart-title {
  position: absolute;
  top: 1rem;
  left: 1.5rem;
  font-family: 'Godo', sans-serif;
  font-size: 1.1rem;
  color: var(--primary-word);
  font-weight: 600;
}

@media (max-width: 768px) {
  .chart-wrapper {
    height: 300px;
    padding: 1rem;
  }
  
  .chart-title {
    font-size: 1rem;
  }
}
</style>