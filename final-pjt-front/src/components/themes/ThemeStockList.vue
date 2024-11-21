<template>
  <div class="container mt-4">
    <div class="row">
      <!-- 국내 주식 칼럼 -->
      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-header bg-light">
            <h2 class="h4 mb-0 fw-bold">국내</h2>
          </div>
          <div class="card-body">
            <div class="stock-list">
              <div v-for="stock in koreanStocks" 
                  :key="stock.code" 
                  class="stock-item">
                <div class="d-flex align-items-center p-2 border-bottom" @click="moveStockItem(stock.code)">
                  <div class="stock-logo me-3">
                    <img :src="getStockLogo(stock.code)" 
                        :alt="stock.name"
                        class="rounded-circle"
                        width="40"
                        height="40">
                  </div>
                  <span class="stock-name">{{ stock.name }}</span>
                  <span class="ms-auto">{{ formatPrice(stock.price) }}원</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 미국 주식 칼럼 -->
      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-header bg-light">
            <h2 class="h4 mb-0 fw-bold">미국</h2>
          </div>
          <div class="card-body">
            <div class="stock-list">
              <div v-for="stock in usaStocks" 
                  :key="stock.code" 
                  class="stock-item">
                <div class="d-flex align-items-center p-2 border-bottom">
                  <div class="stock-logo me-3">
                    <img :src="getStockLogo(stock.code)" 
                        :alt="stock.name"
                        class="rounded-circle"
                        width="40"
                        height="40">
                  </div>
                  <span class="stock-name">{{ stock.name }}</span>
                  <span class="ms-auto">{{ formatPrice(stock.price) }}원</span>
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
import { useStockItemStore } from '@/stores/stockitem';
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const stockStore = useStockStore()
const stockItemStore = useStockItemStore()
const router = useRouter()

const checkUsa = (stock_code) => isNaN(stock_code)

// 국내/미국 주식 분리
const koreanStocks = computed(() => 
  stockStore.stocklist.filter(stock => !checkUsa(stock.code))
)

const usaStocks = computed(() => 
  stockStore.stocklist.filter(stock => checkUsa(stock.code))
  
)

const getStockLogo = (code) => {
  return `/logos/${code}.png`
}

const formatPrice = (price) => {
  return price.toLocaleString('ko-KR')
}

// const currentTime = new Date(new Date().toLocaleString('en-US', { timeZone: 'Asia/Seoul' }))
// const timeString = currentTime.getHours().toString().padStart(2, '0') + 
//                   currentTime.getMinutes().toString().padStart(2, '0') + 
//                   currentTime.getSeconds().toString().padStart(2, '0')

const moveStockItem = function (stockcode) {
  router.push({
    name: 'StockItemView',
    params: { stock_id: stockcode }
  })

  // stockItemStore.getDayInfo(stockcode, timeString)

}

</script>

<style scoped>
.stock-list {
  max-height: 70vh;
  overflow-y: auto;
}

.stock-item:hover {
  background-color: #f8f9fa;
}

.stock-name {
  font-size: 0.95rem;
}

/* 스크롤바 스타일링 */
.stock-list::-webkit-scrollbar {
  width: 6px;
}

.stock-list::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.stock-list::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.stock-list::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>