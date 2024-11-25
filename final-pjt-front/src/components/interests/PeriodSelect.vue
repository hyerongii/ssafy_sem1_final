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
const durationLabel = ref('1개월')
const period = ref('단기') // 초기값 설정
const store = useUserInterestStore()

const updateDurationLabel = () => {
  if (investmentDuration.value >= 12) {
    period.value = '장기'
    durationLabel.value = '1년 이상'
  } else {
    durationLabel.value = `${investmentDuration.value}개월`
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
  min-height: calc(100vh - 64px);
  display: flex;
  /* align-items: center; */
  border-radius: 20px;
  justify-content: center;
  background: #fff;
  padding: 20px;
  font-family: 'Godo', sans-serif;
}

.period-box {
  background: white;
  border-radius: 20px;
  padding: 12px;
  box-shadow: 0 8px 20px rgba(139, 193, 72, 0.1);
  width: 100%;
  max-width: 600px;
}

.period-header {
  text-align: center;
  margin-bottom: 40px;
}

.period-header h2 {
  color: var(--primary-color);
  font-weight: 600;
  margin-bottom: 20px;
  font-size: 2rem;
}


.slider-wrapper {
  margin-top: 70px;
  padding: 20px;
}

.duration-display {
  text-align: center;
  margin-bottom: 40px;
}

.duration-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--primary-dark);
  margin-right: 10px;
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
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--primary-dark);
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 6px rgba(139, 193, 72, 0.2);
}

.custom-range::-moz-range-thumb {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--primary-color);
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 6px rgba(139, 193, 72, 0.2);
}


.range-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
  padding: 0 10px;
}

.range-labels span {
  color: #666;
  font-size: 1rem;
  font-weight: 500;
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