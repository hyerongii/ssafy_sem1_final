<template>
  <div class="container mt-5">
    <h2>{{ theme_name }}</h2>
    <p>{{ stockStore.themeinfo.description }}</p>
    <div>
      <!-- 테마 그래프 작성 -->
      <ThemeChart/>
    </div>
    <div>
      <!-- 각 테마의 주식 종목 나열 -->
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

</style>