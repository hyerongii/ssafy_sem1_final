<template>
  <div class="container mt-5">
    <h1>개별 주식 종목 페이지</h1>
    <p>주식 종목 코드: {{ stockcode }}</p>
  </div>
    <!-- 입력 코드가 국내면 -->
    <div v-if="checkDomestic">
      <DomesticWebSocket
        :stockcode="stockcode"
      />
    </div>
    <!-- 입력 코드가 해외면 -->
    <div v-else>
      <UsaWebSocket
        :stockcode="stockcode"
      />
    </div>
</template>

<script setup>
import DomesticWebSocket from '@/components/stocks/DomesticWebSocket.vue'
import UsaWebSocket from '@/components/stocks/UsaWebSocket.vue'
import { useStockItemStore } from '@/stores/stockitem'
import { onMounted } from 'vue';
import { useRoute } from 'vue-router'

// const stockItemStore = useStockItemStore()
const route = useRoute()
const stockcode = route.params.stock_id

// 입력 코드 국내/해외 인지 구분하기!
const checkDomestic = (stockcode) => isNaN(stockcode)

// onMounted(()=>{
//   const d = new Date()
//   const currentTime = `${d.getHours()}${d.getMinutes()}${d.getSeconds()}`
//   stockItemStore.getDayInfo(stockcode, currentTime)
//   // console.log(currentTime)
// })

</script>

<style scoped>

</style>