<template>
  <div class="chart-wrapper">
    <div class="chart-header">
      <!-- <div class="chart-title">테마 주가 동향</div> -->
      <div class="trend-badge" :class="getTrendClass">
        {{ getTrendMessage }}
      </div>
    </div>
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

// 최근 추세 분석을 위한 computed 속성 추가
const analyzeTrend = computed(() => {
  const data = stockStore.chartdata
  if (!data || data.length < 2) return 0
  
  // 최근 10개의 데이터 사용하여 추세 분석
  const recentData = data.slice(-10)
  const firstPrice = recentData[0].average_close
  const lastPrice = recentData[recentData.length - 1].average_close
  const changeRate = ((lastPrice - firstPrice) / firstPrice) * 100
  
  return changeRate
})

const getTrendMessage = computed(() => {
  const change = analyzeTrend.value
  console.log(change)
  if (Math.abs(change) < 1) return '보합세'
  if (change >= 3) return '강한 상승세'
  if (change >= 1) return '상승세'
  if (change <= -3) return '강한 하락세'
  return '하락세'
})

const getTrendClass = computed(() => {
  const change = analyzeTrend.value
  if (0 < Math.abs(change) < 1) return 'neutral'
  else if (change > 0) return 'up'
  return 'down'
})

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
.chart-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: absolute;
  top: 1rem;
  left: 1.5rem;
}

.trend-badge {
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  font-family: 'Godo', sans-serif;
}

.trend-badge.up {
  background-color: var(--primary-color);
  color: white;
}

.trend-badge.down {
  background-color: var(--primary-dark);
  color: white;
}

.trend-badge.neutral {
  background-color: #e2e8f0;
  color: var(--primary-word);
}

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