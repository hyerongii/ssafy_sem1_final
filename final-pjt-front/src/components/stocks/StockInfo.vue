<template>
  <div>
    <h1>주식종목정보</h1>
    <!-- <p>{{ consensusData.consensus }}</p>
    <p>{{ consensusData.ratio }}</p> -->
    <div>

    </div>
  </div>
</template>

<script setup>
// const consensusData = defineProps({
//   consensus:Object,
//   ratio:Object
// })
import { useStockItemStore } from '@/stores/stockitem'
import { onMounted } from 'vue'

const stockItemStore = useStockItemStore()
const stockcodeProps = defineProps({ stockcode: String })

const getCurrentTime = () => {
  const now = new Date()
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')
  return `${hours}${minutes}${seconds}`
}
const currentTime = getCurrentTime()

// 페이지 처음 들어왔을때는 일 데이터 받아오기
onMounted(()=>{
  stockItemStore.getStockInfo(stockcodeProps.stockcode, currentTime)
})

</script>

<style scoped>

</style>