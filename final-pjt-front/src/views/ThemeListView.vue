<template>
  <div class="container mt-5">
    <div class="theme-container">
      <!-- 같은 MBTI 추천 테마 섹션 -->
      <div class="recommendation-section mb-5">
        <h1 class="title-bubble">{{store.nickname}}님의 mbti와 같은 주주들은 이런 테마도 추천 받았어요! 🎈</h1>
        <div class="tags-container">
          <div v-for="sametheme in sameThemes.interests" 
              class="theme-tag"
              @click="goToThemeDetail(sametheme)">
            {{ sametheme }}
          </div>
        </div>
      </div>

      <!-- 메인 추천 테마 섹션 -->
      <div class="recommendation-section">
        <h1 class="title-bubble">{{store.nickname}}의 추천 테마는 아래와 같습니다! 🎯</h1>
        <div class="theme-grid">
          <div v-for="theme in themes" 
              :key="theme.theme_name" 
              class="theme-card"
              @click="goToThemeDetail(theme.theme_name)">
            <div class="theme-header">
              <h3 class="theme-title">{{ theme.theme_name }}</h3>
              <p class="theme-description">{{ theme.description }}</p>
            </div>

            <div class="stocks-container">
              <!-- 미국 주식 섹션 -->
              <div class="market-box" v-if="hasUsaStocks(theme.stocks)">
                <div class="market-header">
                  <span class="market-label">🇺🇸 미국</span>
                  <!-- <span class="market-badge positive">+25.59%</span> -->
                </div>
                <div class="stocks-grid">
                  <div v-for="stock in filterUsaStocks(theme.stocks)" 
                      :key="stock.code"
                      class="stock-item">
                    <img :src="getStockLogo(stock.code)" 
                        class="stock-logo"
                        :alt="stock.name">
                    <span class="stock-name">{{ stock.name }}</span>
                  </div>
                </div>
              </div>

              <!-- 한국 주식 섹션 -->
              <div class="market-box" v-if="hasKoreanStocks(theme.stocks)">
                <div class="market-header">
                  <span class="market-label">🇰🇷 한국</span>
                  <!-- <span class="market-badge negative">-0.04%</span> -->
                </div>
                <div class="stocks-grid">
                  <div v-for="stock in filterKoreanStocks(theme.stocks)" 
                      :key="stock.code"
                      class="stock-item">
                    <img :src="getStockLogo(stock.code)" 
                        class="stock-logo"
                        :alt="stock.name">
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
</template>

<script setup>
import { useUserInterestStore } from "@/stores/userinterest"
import { ref } from "vue"
import { useRouter } from 'vue-router'

const router = useRouter()
const store = useUserInterestStore()
const themes = store.recommendthemes
const sameThemes = store.samethemes

const checkUsa = (stock_code) => isNaN(stock_code)

const hasUsaStocks = (stocks) => stocks.some(stock => checkUsa(stock.code))
const hasKoreanStocks = (stocks) => stocks.some(stock => !checkUsa(stock.code))

const filterUsaStocks = (stocks) => stocks.filter(stock => checkUsa(stock.code))
const filterKoreanStocks = (stocks) => stocks.filter(stock => !checkUsa(stock.code))

const getStockLogo = (code) => {
  if (isNaN(Number(code))) {
    return `https://assets.parqet.com/logos/symbol/${code}?format=png`
  }
}

const goToThemeDetail = (theme_name) => {
  router.push({
    name: 'ThemeItemView',
    params: { theme_id: theme_name }
  })
}
</script>

<style scoped>
.theme-container {
  padding: 2rem;
}

.title-bubble {
  font-size: 2rem;
  background-color: #f0f7ff;
  padding: 1rem 2rem;
  border-radius: 30px;
  display: inline-block;
  margin-bottom: 2rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 1rem;
}

.theme-tag {
  background-color: #e9ecef;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.theme-tag:hover {
  background-color: #007bff;
  color: white;
  transform: scale(1.05);
}

.theme-grid {
  display: grid;
  gap: 2rem;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

.theme-card {
  background: white;
  border-radius: 25px;
  padding: 1.5rem;
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.theme-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 12px 25px rgba(0,0,0,0.15);
}

.theme-header {
  margin-bottom: 1.5rem;
}

.theme-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.theme-description {
  color: #6c757d;
  font-size: 0.9rem;
}

.market-box {
  background: #f8f9fa;
  border-radius: 20px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.market-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.market-label {
  font-weight: bold;
  font-size: 1.1rem;
}

.market-badge {
  padding: 0.3rem 1rem;
  border-radius: 15px;
  font-size: 0.9rem;
  font-weight: bold;
}

.market-badge.positive {
  background-color: #d4edda;
  color: #155724;
}

.market-badge.negative {
  background-color: #f8d7da;
  color: #721c24;
}

.stocks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.8rem;
}

.stock-item {
  background: white;
  border-radius: 15px;
  padding: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.stock-item:hover {
  transform: scale(1.05);
}

.stock-logo {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  object-fit: cover;
}

.stock-name {
  font-size: 0.85rem;
  color: #495057;
}
</style>
