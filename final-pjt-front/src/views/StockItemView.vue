<template>
  <div class="container-fluid px-4 mt-5">
    <h1 class="mb-4">{{ stockItemStore.stockInfo.articles_data?.stock_name }}</h1>
    
    <!-- 차트와 종목정보 섹션 -->
    <div class="row gx-4 mb-4">
      <!-- 차트 섹션 (왼쪽) -->
      <div class="col-lg-8">
        <!-- 네비게이션 Pills -->
        <ul class="nav nav-pills mb-4">
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
        
        <!-- 차트 영역 -->
        <div class="chart-container">
          <RouterView></RouterView>
        </div>
      </div>

      <!-- 종목 정보 섹션 (오른쪽) -->
      <div class="col-lg-4">
        <div class="stock-info-container">
          <div v-if="isNaN(stockcode)">
            <UsaStockInfo/>
          </div>
          <div v-else>
            <DomesticStockInfo/>
          </div>
        </div>
      </div>
    </div>
      <!-- 커뮤니티 섹션 -->
    <div class="row mt-4">
      <div class="col-12">
        <div class="community-container">
          <h3 class="community-title" @click="moveCommunity">커뮤니티</h3>
          <div class="articles-grid">
            <div v-for="article in stockItemStore.stockInfo.articles_data?.articles" 
                :key="article.id" 
                class="article-card">
              <div class="article-header">
                <span class="article-status" :class="article.status">{{ article.status }}</span>
              </div>
              <div class="article-content">
                <h4 class="article-title">{{ article.title }}</h4>
                <p class="article-text">{{ article.content }}</p>
              </div>
              <div class="article-footer">
                <span class="article-date">{{ article.created_at }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import DomesticStockInfo from '@/components/stocks/DomesticStockInfo.vue'
import UsaStockInfo from '@/components/stocks/UsaStockInfo.vue'
import { useStockItemStore } from '@/stores/stockitem'
import { computed, onMounted, ref, watch } from 'vue'
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

// 페이지 처음 들어왔을때
onMounted(() => {
  // 종목 정보 먼저 가져오기
stockItemStore.getStockInfo(stockcode, currentTime)
  // 일 차트 그리기
stockItemStore.getDayInfo(stockcode, currentTime)
})

const moveCommunity = function () {

}

</script>

<style scoped>
.container-fluid {
  max-width: 1600px;
  margin: 0 auto;
}

.chart-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  height: calc(100vh - 250px);
}

.stock-info-container {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  height: calc(100vh - 250px);
  overflow-y: auto;
}

.nav-pills .nav-link {
  margin-right: 0.5rem;
  border-radius: 20px;
  padding: 0.5rem 1.5rem;
}

.nav-pills .nav-link.active {
  background-color: #0d6efd;
}

h1 {
  font-size: 1.8rem;
  color: #333;
  margin-left: 0.5rem;
}
</style>