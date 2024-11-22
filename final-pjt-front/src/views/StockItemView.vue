<template>
  <div class="container mt-5">
    <h1>개별 주식 종목 페이지</h1>
    <p>주식 종목 코드: {{ stockcode }}</p>
  </div>
  <div>
    <!-- 부트스트랩 네비게이션 Pills -->
    <ul class="nav nav-pills m-4">
      <li class="nav-item">
        <RouterLink 
          :to="{ name: 'day', params: { stock_id: stockcode }}" 
          class="nav-link" 
          :class="{ active: $route.name === 'day' || !$route.name }"
          @click="moveDayChart(stockcode)"
        >일</RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink 
          :to="{ name: 'week', params: { stock_id: stockcode }}" 
          class="nav-link"
          :class="{ active: route.name === 'week' }"
          @click="movePeriodChart('W')"
        >주</RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink 
          :to="{ name: 'month', params: { stock_id: stockcode }}" 
          class="nav-link"
          :class="{ active: route.name === 'month' }"
          @click="movePeriodChart('1M')"
        >월</RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink 
          :to="{ name: 'sixmonth', params: { stock_id: stockcode }}" 
          class="nav-link"
          :class="{ active: route.name === 'sixmonth' }"
          @click="movePeriodChart('6M')"
        >6개월</RouterLink>
      </li>
      <li class="nav-item">
        <RouterLink 
          :to="{ name: 'year', params: { stock_id: stockcode }}" 
          class="nav-link"
          :class="{ active: route.name === 'year' }"
          @click="movePeriodChart('1Y')"
        >년</RouterLink>
      </li>
    </ul>
  </div>

    <!-- 차트 컴포넌트를 표시할 router-view -->
    <RouterView></RouterView>
</template>

<script setup>
import DayStockChart from '@/components/stocks/DayStockChart.vue'
import { useStockItemStore } from '@/stores/stockitem'
import { onMounted } from 'vue';
import { RouterLink, RouterView, useRoute } from 'vue-router'

const stockItemStore = useStockItemStore()
const route = useRoute()
const stockcode = route.params.stock_id

// 입력 코드 국내/해외 인지 구분하기!
const checkDomestic = (stockcode) => isNaN(stockcode)

const getCurrentTime = () => {
  const now = new Date()
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')
  return `${hours}${minutes}${seconds}`
}

// 라우트링크 클릭할때는 주, 월, 년 각각 데이터 받아오기
const movePeriodChart = function (period) {
  // 주, 월, 년 함수
  stockItemStore.getPeriodInfo(stockcode, period)
  console.log(stockItemStore.periodChart)
}

const currentTime = getCurrentTime()

const moveDayChart = function (stockcode){
  stockItemStore.getDayInfo(stockcode, currentTime)
}

// 페이지 처음 들어왔을때는 일 데이터 받아오기
onMounted(()=>{
  // 일 차트 그리는 함수
  stockItemStore.getDayInfo(stockcode, currentTime)

})

</script>

<style scoped>

</style>