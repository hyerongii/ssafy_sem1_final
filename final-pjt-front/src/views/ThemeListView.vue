<template>
  <div class="container mt-5">
    <h1 class="display-4 mb-5 text-center">당신의 추천 테마는 아래와 같습니다!</h1>
    
    <div class="row">
      <div class="col-12 mb-4" v-for="theme in themes" :key="theme.theme_name">
        <div class="card shadow-sm hover-card" @click="goToThemeDetail(theme.theme_name)">
          <!-- 테마 헤더 -->
          <div class="card-header bg-white border-bottom-0 pt-4 px-4">
            <h3 class="card-title h4 fw-bold mb-2">{{ theme.theme_name }}</h3>
            <p class="text-muted mb-3">{{ theme.description }}</p>
          </div>

          <div class="card-body px-4">
            <div class="row">
              <!-- 미국 주식 섹션 -->
              <div class="col-md-6" v-if="hasUsaStocks(theme.stocks)">
                <div class="market-section">
                  <div class="d-flex justify-content-between align-items-center mb-3">
                    <span class="fw-bold">미국</span>
                    <span class="badge bg-danger">+25.59%</span>
                  </div>
                  <div class="d-flex flex-wrap gap-2">
                    <div v-for="stock in filterUsaStocks(theme.stocks)" 
                        :key="stock.code"
                        class="stock-item d-flex align-items-center">
                      <div class="stock-logo-wrapper me-2">
                        <img :src="getStockLogo(stock.code)" 
                            class="stock-logo rounded-circle"
                            :alt="stock.name">
                      </div>
                      <span class="stock-name">{{ stock.name }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 한국 주식 섹션 -->
              <div class="col-md-6" v-if="hasKoreanStocks(theme.stocks)">
                <div class="market-section">
                  <div class="d-flex justify-content-between align-items-center mb-3">
                    <span class="fw-bold">한국</span>
                    <span class="badge bg-primary">-0.04%</span>
                  </div>
                  <div class="d-flex flex-wrap gap-2">
                    <div v-for="stock in filterKoreanStocks(theme.stocks)" 
                        :key="stock.code"
                        class="stock-item d-flex align-items-center">
                      <div class="stock-logo-wrapper me-2">
                        <img :src="getStockLogo(stock.code)" 
                            class="stock-logo rounded-circle"
                            :alt="stock.name">
                      </div>
                      <span class="stock-name">{{ stock.name }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUserInterestStore } from "@/stores/userinterest"
import { ref } from "vue"
import { useRouter } from 'vue-router'

const router = useRouter()
const store = useUserInterestStore()
const themes = store.recommendthemes

const checkUsa = (stock_code) => isNaN(stock_code)

const hasUsaStocks = (stocks) => stocks.some(stock => checkUsa(stock.code))
const hasKoreanStocks = (stocks) => stocks.some(stock => !checkUsa(stock.code))

const filterUsaStocks = (stocks) => stocks.filter(stock => checkUsa(stock.code))
const filterKoreanStocks = (stocks) => stocks.filter(stock => !checkUsa(stock.code))

const getStockLogo = (code) => {
  return `/logos/${code}.png`
}

const goToThemeDetail = (theme_name) => {
  router.push({
    name: 'ThemeItemView',
    params: { theme_id: theme_name }
  })
}
</script>

<style scoped>
.hover-card {
  transition: transform 0.2s ease-in-out;
  cursor: pointer;
}

.hover-card:hover {
  transform: translateY(-5px);
}

.stock-logo-wrapper {
  width: 40px;
  height: 40px;
  overflow: hidden;
}

.stock-logo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.stock-name {
  font-size: 0.9rem;
}

.market-section {
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  height: 100%;
}

.gap-2 {
  gap: 0.5rem !important;
}

.stock-item {
  background-color: white;
  padding: 0.5rem;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
</style>