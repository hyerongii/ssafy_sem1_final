<template>
  <div class="container mt-5">
    <div class="theme-container">
      <!-- 같은 MBTI 추천 테마 섹션 -->
      <div class="recommendation-section mb-5">
        <h1 class="title-bubble">{{store.nickname}} 주주님의 mbti와 같은 주주들은 이런 테마도 추천 받았어요! 🎈</h1>
        <div class="tags-container">
          <div v-for="sametheme in sameThemes.interests" 
              :key="sametheme"
              class="theme-tag"
              @click="goToThemeDetail(sametheme)">
            {{ sametheme }}
          </div>
        </div>
      </div>

      <!-- 메인 추천 테마 섹션 -->
      <div class="recommendation-section">
        <h1 class="title-bubble">{{store.nickname}} 주주님의 추천 테마는 아래와 같습니다! 🎯</h1>
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
                </div>
                <div class="stocks-grid">
                  <div v-for="stock in filterUsaStocks(theme.stocks)" 
                      :key="stock.code"
                      class="stock-item">
                    <!-- stockLogos에서 동적으로 이미지 경로 가져오기 -->
                    <img :src="stockLogos[stock.code]" 
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
                </div>
                <div class="stocks-grid">
                  <div v-for="stock in filterKoreanStocks(theme.stocks)" 
                      :key="stock.code"
                      class="stock-item">
                    <!-- stockLogos에서 동적으로 이미지 경로 가져오기 -->
                    <img :src="stockLogos[stock.code]" 
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
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"

const router = useRouter();
const store = useUserInterestStore();
const themes = store.recommendthemes;
const sameThemes = store.samethemes;

// 컴포넌트가 마운트될 때 데이터 확인 및 초기화
onMounted(async () => {
  // store에 데이터가 없는 경우에만 analyze 실행
  if (!store.recommendthemes || store.recommendthemes.length === 0) {
    await store.analyze();
    // analyze 완료 후 데이터 업데이트
    themes.value = store.recommendthemes;
    sameThemes.value = store.samethemes;
  }
  
  // 로고 초기화는 데이터 유무와 관계없이 실행
  await initializeStockLogos();
})

// 로고 URL을 저장하는 반응형 객체
const stockLogos = ref({});

// 미국/한국 주식 필터링 함수
const checkUsa = (stock_code) => isNaN(stock_code);
const hasUsaStocks = (stocks) => stocks.some(stock => checkUsa(stock.code));
const hasKoreanStocks = (stocks) => stocks.some(stock => !checkUsa(stock.code));
const filterUsaStocks = (stocks) => stocks.filter(stock => checkUsa(stock.code));
const filterKoreanStocks = (stocks) => stocks.filter(stock => !checkUsa(stock.code));

// 이미지 존재 여부 확인 함수
const checkImageExists = (url) => {
  return new Promise((resolve) => {
    const img = new Image()
    img.onload = () => resolve(true)
    img.onerror = () => resolve(false)
    img.src = url
  })
}

// 비동기 로고 URL 가져오기
const getStockLogo = async (code) => {
  if (isNaN(Number(code))) {
    const parqetLogoUrl = `https://assets.parqet.com/logos/symbol/${code}?format=png`;
    const isParqetLogoValid = await checkImageExists(parqetLogoUrl)
    if (isParqetLogoValid) {
      return parqetLogoUrl
    }
  }

  try {
    return new URL(`../assets/logos/${code}.png`, import.meta.url).href
  } catch {
    console.error(`로컬 이미지가 존재하지 않습니다: @/assets/logos/${code}.png`)
    return null;
  }
};

// 모든 주식의 로고 URL을 초기화
const initializeStockLogos = async () => {
  for (const theme of themes) {
    for (const stock of theme.stocks) {
      if (!stockLogos.value[stock.code]) {
        stockLogos.value[stock.code] = await getStockLogo(stock.code)
      }
    }
  }
};

// 컴포넌트가 마운트될 때 로고 초기화
onMounted(() => {
  initializeStockLogos()
})

// 테마 상세 페이지 이동
const goToThemeDetail = (theme_name) => {
  router.push({
    name: "ThemeItemView",
    params: { theme_id: theme_name },
  })
}
</script>

<style scoped>
.theme-container {
  padding: 2rem;
  font-family: 'Godo', sans-serif;
}

.title-bubble {
  font-size: 1.8rem;
  background-color: #f8faf5;
  padding: 1.2rem 2rem;
  border-radius: 30px;
  display: inline-block;
  margin-bottom: 2rem;
  box-shadow: 0 4px 15px rgba(139, 193, 72, 0.1);
  color: var(--primary-color);
  font-weight: 600;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 1rem;
}

.theme-tag {
  background-color: #f8faf5;
  padding: 0.8rem 1.5rem;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(139, 193, 72, 0.2);
  color: #333;
}

.theme-tag:hover {
  background-color: var(--primary-color);
  color: white;
  transform: translateY(-2px);
}

.theme-grid {
  display: grid;
  gap: 2rem;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

.theme-card {
  background: white;
  border-radius: 20px;
  padding: 1.8rem;
  box-shadow: 0 8px 20px rgba(139, 193, 72, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid rgba(139, 193, 72, 0.1);
}

.theme-card:hover {
  transform: translateY(-5px);
  border-color: var(--primary-color);
}

.theme-header {
  margin-bottom: 1.5rem;
}

.theme-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 0.8rem;
}

.theme-description {
  color: #666;
  font-size: 1rem;
  line-height: 1.5;
}

.market-box {
  background: #f8faf5;
  border-radius: 15px;
  padding: 1.2rem;
  margin-bottom: 1rem;
  border: 1px solid rgba(139, 193, 72, 0.1);
}

.market-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.market-label {
  font-weight: 600;
  font-size: 1.1rem;
  color: #333;
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
  border-radius: 12px;
  padding: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  transition: all 0.2s ease;
  border: 1px solid rgba(139, 193, 72, 0.1);
}

.stock-item:hover {
  transform: translateY(-2px);
  border-color: var(--primary-color);
}

.stock-logo {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  object-fit: cover;
}

.stock-name {
  font-size: 0.9rem;
  color: #333;
}
</style>
