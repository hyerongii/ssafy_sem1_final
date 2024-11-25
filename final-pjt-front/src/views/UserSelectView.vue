<template>
  <div class="survey-container">
    <div class="survey-box">
      <div class="survey-header">
        <h2>나만의 투자 여정을 시작해볼까요?</h2>
        <p class="text-muted">당신에게 딱 맞는 투자 테마를 찾아드립니다</p>
      </div>

      <div class="survey-content">

        <div class="survey-grid">
          <!-- MBTI 선택 -->
          <div class="survey-card">
            <MbtiSelect />
          </div>

          <!-- 관심 분야 선택 -->
          <div class="survey-card">
            <InterestSelect />
          </div>

          <!-- 투자 기간 선택 -->
          <div class="survey-card">
            <PeriodSelect />
          </div>
        </div>

        <div class="text-center mt-2 ">
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

const sendUserData = function () {
  store.analyze()
}
</script>

<style scoped>
.survey-container {
  min-height: calc(100vh - 64px);
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8faf5, #fff);
  padding: 20px;
  margin-top: 64px;
}

.survey-box {
  background: white;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 15px 25px rgba(139, 193, 72, 0.1);
  width: 100%;
  max-width: 1400px;
}

.survey-header {
  text-align: center;
  margin-bottom: 40px;
}

.survey-header h2 {
  color: var(--primary-color);
  font-weight: 600;
  margin-top: 30px;
  margin-bottom: 10px;
  font-family: 'Godo', sans-serif;
}

.survey-header p {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 40px;
}

.survey-grid {
  display: grid;
  grid-template-columns: 1fr 1.3fr 1fr;  /* InterestSelect를 더 넓게 설정 */
  gap: 30px;
  margin-top: 30px;
}

.survey-card {
  background: #f8faf5;
  border-radius: 15px;
  padding: 30px;  /* 패딩 증가 */
  text-align: center;
  transition: all 0.3s ease;
  border: 1px solid rgba(139, 193, 72, 0.1);
  min-height: 400px;  /* 최소 높이 설정 */
}

.survey-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(139, 193, 72, 0.2);
  border-color: var(--primary-color);
}

.card-icon {
  font-size: 2rem;
  color: var(--primary-dark);
  margin-bottom: 20px;
}

.submit-btn {
  background: var(--primary-color);
  color: white;
  border: none;
  padding: 15px 40px;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 500;
  transition: all 0.3s ease;
  font-family: 'Godo', sans-serif;
  
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(139, 193, 72, 0.3);
  background: var(--primary-dark);

}

.text-muted {
  color: #666 !important;
}

@media (max-width: 768px) {
  .survey-grid {
    grid-template-columns: 1fr;  /* 화면이 작아지면 세로로 배열 */
  }

  .survey-card {
    min-height: auto;  /* 모바일에서는 자동 높이 */
  }
}

</style>