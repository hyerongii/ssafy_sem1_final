<template>
  <div class="period-container">
    <div class="period-box">
      <div class="period-header">
        <h2>투자 기간 설정</h2>
        <p class="text-muted">원하시는 투자 기간을 선택해주세요</p>
      </div>

      <div class="slider-wrapper">
        <div class="duration-display">
          <span class="duration-value">{{ durationLabel }}</span>
          <!-- <span class="duration-type">{{ period }}</span> -->
        </div>

        <div class="slider-container">
          <input 
            type="range" 
            class="custom-range" 
            min="1" 
            max="12" 
            step="1" 
            v-model="investmentDuration" 
            @input="updateDurationLabel"
          />
          
          <div class="range-labels">
            <span>1개월</span>
            <span>6개월</span>
            <span>1년+</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, watch, onMounted } from 'vue'
import { useUserInterestStore } from '@/stores/userinterest'

const investmentDuration = ref(1)
const durationLabel = ref('1달')
const period = ref('단기') // 초기값 설정
const store = useUserInterestStore()

const updateDurationLabel = () => {
  if (investmentDuration.value >= 12) {
    period.value = '장기'
    durationLabel.value = '1년 이상'
  } else {
    durationLabel.value = `${investmentDuration.value}달`
    if (investmentDuration.value <= 3) {
      period.value = '단기'
    } else {
      period.value = '중기'
    }
  }
}

// 컴포넌트 마운트 시 초기값 설정
onMounted(() => {
  updateDurationLabel()
})

watch(period, (newPeriod) => {
  store.userperiod = newPeriod
}, { immediate: true })
</script>

<style scoped>
.period-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.period-box {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 15px 25px rgba(0,0,0,0.05);
  width: 100%;
  max-width: 600px;
}

.period-header {
  text-align: center;
  margin-bottom: 40px;
}

.period-header h2 {
  color: #2d3748;
  font-weight: 600;
  margin-bottom: 10px;
}

.slider-wrapper {
  padding: 20px;
}

.duration-display {
  text-align: center;
  margin-bottom: 30px;
}

.duration-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #667eea;
  margin-right: 10px;
}

.duration-type {
  font-size: 1.2rem;
  color: #718096;
  padding: 5px 15px;
  background: #f7fafc;
  border-radius: 20px;
}

.slider-container {
  position: relative;
  padding: 10px 0;
}

.custom-range {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  width: 100%;
  height: 8px;
  border-radius: 5px;
  background: #e2e8f0;
  outline: none;
}

.custom-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

.custom-range::-moz-range-thumb {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}


.range-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
  padding: 0 10px;
}

.range-labels span {
  color: #718096;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .period-box {
    padding: 20px;
  }
  
  .duration-value {
    font-size: 2rem;
  }
}
</style>