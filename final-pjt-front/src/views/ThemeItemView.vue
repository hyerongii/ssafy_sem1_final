<template>
  <div class="theme-container mt-5">
    <div class="theme-header">
      <h2>{{ theme_name }}</h2>
      <p class="theme-description">{{ stockStore.themeinfo.description }}</p>
    </div>
    <!-- 테마차트 -->
    <div class="chart-section">
      <ThemeChart/>
    </div>
    <!-- 테마종목리스트 -->
    <div class="stock-list-section">
      <ThemeStockList/>
    </div>
  </div>
</template>

<script setup>
import { useStockStore } from '@/stores/stock'
import { useRoute } from 'vue-router'
import ThemeChart from '@/components/themes/ThemeChart.vue'
import ThemeStockList from '@/components/themes/ThemeStockList.vue'
import { onMounted } from 'vue'

// axios post 요청 변수

const route = useRoute()
const stockStore = useStockStore()
const theme_name = route.params.theme_id
const currentDate = new Date()

// 페이지 접속시 store 호출하면 theme 데이터 업데이트 됨
onMounted(() => {
  stockStore.todaydate = `${currentDate.getFullYear()}${currentDate.getMonth()+1}${currentDate.getDate()}`
  stockStore.getStockChart(theme_name)

  console.log(stockStore)
  
})


</script>

<style scoped>
.theme-container {
  font-family: 'Godo', sans-serif;
  padding: 3rem 2rem;
  background: white;
  border-left: 4px solid var(--primary-color);
  margin-top: 80px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.theme-header {
  text-align: left;
  margin-bottom: 1rem;
  padding-bottom: 1.5rem;
}

h2 {
  font-size: 2.2rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--primary-word);
  display: inline-block;
  position: relative;
}

.theme-description {
  color: var(--primary-word);
  font-size: 1.1rem;
  line-height: 1.8;
  max-width: 800px;
  opacity: 0.85;
}

.chart-section {
  margin-bottom: 3rem;
  position: relative;
}

.chart-section::before {
  content: '테마 동향';
  position: absolute;
  top: 0;
  left: 0;
  font-size: 1.1rem;
  color: var(--primary-word);
  font-weight: 500;
  opacity: 0.8;
}

.chart-section:hover {
  box-shadow: 0 5px 15px rgba(237, 145, 156, 0.2);
  transform: translateY(-2px);
}

.stock-list-section {
  position: relative;
  padding-top: 1rem;
}

@media (max-width: 768px) {
  .theme-container {
    padding: 2rem 1rem;
    border-left-width: 3px;
  }

  h2 {
    font-size: 1.8rem;
  }

  .theme-description {
    font-size: 1rem;
    line-height: 1.6;
  }
}
</style>