<template>
  <div class="stock-container mt-4">
    <div class="row g-4">
      <!-- 국내 주식 칼럼 -->
      <div class="col-md-6">
        <div class="stock-card">
          <div class="card-header d-flex">
            <h2>국내 종목</h2>
            <img class="flag mx-2" src="../../../public/img/flag-south-korea.png" alt="flag_korea">
          </div>
          <div class="card-body">
            <div class="stock-list">
              <div v-for="stock in koreanStocks" 
                  :key="stock.code" 
                  class="stock-item"
                  @click="moveStockItem(stock.code)">
                <div class="stock-content">
                  <div class="stock-info">
                    <div class="stock-logo">
                      <img :src="getStockLogo(stock.code)" 
                          :alt="stock.name"
                          class="logo-image">
                    </div>
                    <span class="stock-name">{{ stock.name }}</span>
                  </div>
                  <span class="stock-price">{{ formatPrice(stock.price) }}원</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 미국 주식 칼럼 -->
      <div class="col-md-6">
        <div class="stock-card">
          <div class="card-header d-flex">
            <h2>미국 종목</h2>
            <img class="flag mx-2" src="../../../public/img/flag-united-states.png" alt="flag_us">
          </div>
          <div class="card-body">
            <div class="stock-list">
              <div v-for="stock in usaStocks" 
                  :key="stock.code" 
                  class="stock-item"
                  @click="moveStockItem(stock.code)">
                <div class="stock-content">
                  <div class="stock-info">
                    <div class="stock-logo">
                      <img :src="getStockLogo(stock.code)" 
                          :alt="stock.name"
                          class="logo-image">
                    </div>
                    <span class="stock-name">{{ stock.name }}</span>
                  </div>
                  <span class="stock-price">{{ formatPrice(stock.price) }}원</span>
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
import { useStockStore } from '@/stores/stock'
import { useStockItemStore } from '@/stores/stockitem'
import { computed, onMounted , ref} from 'vue'
import { useRouter } from 'vue-router'

const stockStore = useStockStore()
const router = useRouter()

const checkUsa = (stock_code) => isNaN(stock_code)

// 국내/미국 주식 분리
const koreanStocks = computed(() => 
  stockStore.stocklist.filter(stock => !checkUsa(stock.code))
)

const usaStocks = computed(() => 
  stockStore.stocklist.filter(stock => checkUsa(stock.code))
  
)

const checkImageExists = (url) => {
  const img = new Image();
  img.src = url;

  // 이미지가 즉시 로드 가능한 경우를 확인
  if (img.complete) {
    return img.width > 0; // 이미지가 유효한 경우 true 반환
  }

  // 이미지가 아직 로드되지 않은 경우 false 반환
  return false;
};
const getStockLogo = (code) => {
  if (isNaN(Number(code))) {
    const parqetLogoUrl = `https://assets.parqet.com/logos/symbol/${code}?format=png`;
    const isParqetLogoValid = checkImageExists(parqetLogoUrl);
    if (isParqetLogoValid) {
      console.log(code)
      return parqetLogoUrl;
    } else {
      return new URL(`../../assets/logos/${code}.png`, import.meta.url).href;
    }
  }
  try {
    return new URL(`../../assets/logos/${code}.png`, import.meta.url).href;
  } catch {
    console.error(`로컬 이미지가 존재하지 않습니다: @/assets/logos/${code}.png`);
    return null;
  }
};


const formatPrice = (price) => {
  return price.toLocaleString('ko-KR')
}

const getCurrentTime = () => {
  const now = new Date()
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')
  return `${hours}${minutes}${seconds}`
}

const currentTime = getCurrentTime()

const moveStockItem = function (stockcode) {
  router.push({
    name: 'day',
    params: { stock_id: stockcode }
  })

}

</script>

<style scoped>
.stock-container {
  font-family: 'Godo', sans-serif;
}

.stock-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(237, 145, 156, 0.1);
  transition: all 0.3s ease;
  overflow: hidden;
}

.stock-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(237, 145, 156, 0.15);
}

.card-header {
  background: var(--primary-green);
  padding: 1rem 1.5rem;
  border-bottom: none;
}

.card-header h2 {
  color: white;
  font-size: 1.2rem;
  margin: 0;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.flag {
  width: 30px;
  display: inline-block;
  vertical-align: middle;
}

.card-body {
  padding: 0;
}

.stock-list {
  max-height: 60vh;
  overflow-y: auto;
}

.stock-item {
  cursor: pointer;
  transition: all 0.2s ease;
  border-bottom: 1px solid rgba(139, 193, 72, 0.1);
}

.stock-item:hover {
  background-color: #dcecc8;
}

.stock-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.8rem 1.2rem;
}

.stock-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stock-logo {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  /* border: 2px solid var(--primary-light); */
}

.logo-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.stock-name {
  font-size: 1rem;
  color: var(--primary-word);
  font-weight: 500;
}

.stock-price {
  font-weight: 600;
  color: var(--primary-verydark);
}

/* 스크롤바 스타일링 */
.stock-list::-webkit-scrollbar {
  width: 6px;
}

.stock-list::-webkit-scrollbar-track {
  background: #f8f9fa;
  border-radius: 3px;
}

.stock-list::-webkit-scrollbar-thumb {
  background: var(--primary-light);
  border-radius: 3px;
}

.stock-list::-webkit-scrollbar-thumb:hover {
  background: var(--primary-dark);
}

@media (max-width: 768px) {
  .stock-content {
    padding: 0.6rem 1rem;
  }
  
  .stock-name {
    font-size: 0.9rem;
  }
  
  .stock-logo {
    width: 32px;
    height: 32px;
  }

  .card-header h2,
  .flag {
    font-size: 1rem;
  }
}
</style>