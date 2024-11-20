<template>
  <div class="survey-container">
    <div class="survey-box">
      <div class="survey-header">
        <h2>나만의 투자 여정을 시작해볼까요?</h2>
        <p class="text-muted">당신에게 딱 맞는 투자 테마를 찾아드립니다</p>
      </div>

      <div class="survey-content">
        <!-- Progress Bar -->
        <div class="progress mb-4" style="height: 8px;">
          <div class="progress-bar progress-gradient" role="progressbar" 
              :style="{ width: progressWidth + '%' }" 
              aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">
          </div>
        </div>

        <div class="survey-grid">
          <!-- MBTI 선택 -->
          <div class="survey-card">
            <div class="card-icon">
              <i class="bi bi-person-circle"></i>
            </div>
            <MbtiSelect />
          </div>

          <!-- 관심 분야 선택 -->
          <div class="survey-card">
            <div class="card-icon">
              <i class="bi bi-graph-up"></i>
            </div>
            <InterestSelect />
          </div>

          <!-- 투자 기간 선택 -->
          <div class="survey-card">
            <div class="card-icon">
              <i class="bi bi-calendar-check"></i>
            </div>
            <PeriodSelect />
          </div>
        </div>

        <div class="text-center mt-5">
          <button @click="sendUserData" class="submit-btn">
            나만의 투자 테마 확인하기
            <i class="bi bi-arrow-right ms-2"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import MbtiSelect from '@/components/interests/MbtiSelect.vue'
import InterestSelect from '@/components/interests/InterestSelect.vue'
import PeriodSelect from '@/components/interests/PeriodSelect.vue'
import { useUserInterestStore } from '@/stores/userinterest'
import { ref, computed } from 'vue'

const store = useUserInterestStore()

const progressWidth = computed(() => {
  // 각 선택 항목이 완료되었는지 확인하고 진행률 계산
  let progress = 0
  // 진행률 계산 로직 구현
  return progress
})

const sendUserData = function () {
  store.analyze()
}
</script>

<style scoped>
.survey-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.survey-box {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 15px 25px rgba(0,0,0,0.05);
  width: 100%;
  max-width: 1200px;
}

.survey-header {
  text-align: center;
  margin-bottom: 40px;
}

.survey-header h2 {
  color: #2d3748;
  font-weight: 600;
  margin-bottom: 10px;
}

.survey-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-top: 30px;
}

.survey-card {
  background: #f8fafc;
  border-radius: 15px;
  padding: 15px;
  text-align: center;
  transition: transform 0.3s ease;
}

.survey-card:hover {
  transform: translateY(-5px);
}

.card-icon {
  font-size: 2.5rem;
  color: #667eea;
  margin-bottom: 20px;
}

.progress-gradient {
  background: linear-gradient(to right, #667eea, #764ba2);
}

.submit-btn {
  background: linear-gradient(to right, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102,126,234,0.4);
}

@media (max-width: 768px) {
  .survey-box {
    padding: 20px;
  }
  
  .survey-grid {
    grid-template-columns: 1fr;
  }
}
</style>
