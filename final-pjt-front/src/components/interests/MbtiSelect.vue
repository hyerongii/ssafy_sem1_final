<template>
  <div class="mbti-container">
    <div class="mbti-header">
      <h2>나의 MBTI는?</h2>
      <!-- <p class="text-muted">당신의 성향에 맞는 투자 스타일을 찾아드립니다</p> -->
    </div>

    <div class="mbti-grid">
      <div class="mbti-result" v-if="store.usermbti">
        <span class="result-label"></span>
        <span class="result-value">{{ store.usermbti }}</span>
      </div>

      <!-- E/I 선택 -->
      <div class="mbti-group">
        <span class="type-label">에너지 방향</span>
        <div class="btn-group">
          <input type="radio" class="btn-check" id="E" v-model="selectedEI" value="E">
          <label class="mbti-btn" :class="{ active: selectedEI === 'E' }" for="E">
            <div class="btn-content">
              <div class="type-info">
                <span class="type">E</span>
                <span class="description">외향형</span>
              </div>
              <span class="message">주식방에서 떠들면서 투자하는게 내 스타일!</span>
            </div>
          </label>
          
          <input type="radio" class="btn-check" id="I" v-model="selectedEI" value="I">
          <label class="mbti-btn" :class="{ active: selectedEI === 'I' }" for="I">
            <div class="btn-content">
              <div class="type-info">
                <span class="type">I</span>
                <span class="description">내향형</span>
              </div>
              <span class="message">혼자 차트 보면서 분석하는게 편해요</span>
            </div>
          </label>
        </div>
      </div>

      <!-- S/N 선택 -->
      <div class="mbti-group">
        <span class="type-label">인식 방식</span>
        <div class="btn-group">
          <input type="radio" class="btn-check" id="S" v-model="selectedSN" value="S">
          <label class="mbti-btn" :class="{ active: selectedSN === 'S' }" for="S">
            <div class="btn-content">
              <div class="type-info">
                <span class="type">S</span>
                <span class="description">감각형</span>
              </div>
              <span class="message">실제 데이터로 승부하는 현실주의자</span>
            </div>
          </label>
          
          <input type="radio" class="btn-check" id="N" v-model="selectedSN" value="N">
          <label class="mbti-btn" :class="{ active: selectedSN === 'N' }" for="N">
            <div class="btn-content">
              <div class="type-info">
                <span class="type">N</span>
                <span class="description">직관형</span>
              </div>
              <span class="message">다음 테마주가 뭐가 될지 감이 와!</span>
            </div>
          </label>
        </div>
      </div>

      <!-- T/F 선택 -->
      <div class="mbti-group">
        <span class="type-label">판단 기준</span>
        <div class="btn-group">
          <input type="radio" class="btn-check" id="T" v-model="selectedTF" value="T">
          <label class="mbti-btn" :class="{ active: selectedTF === 'T' }" for="T">
            <div class="btn-content">
              <div class="type-info">
                <span class="type">T</span>
                <span class="description">사고형</span>
              </div>
              <span class="message">차트와 데이터로만 얘기해주세요</span>
            </div>
          </label>
          
          <input type="radio" class="btn-check" id="F" v-model="selectedTF" value="F">
          <label class="mbti-btn" :class="{ active: selectedTF === 'F' }" for="F">
            <div class="btn-content">
              <div class="type-info">
                <span class="type">F</span>
                <span class="description">감정형</span>
              </div>
              <span class="message">이 기업 성장 스토리가 너무 감동적이야</span>
            </div>
          </label>
        </div>
      </div>

      <!-- J/P 선택 -->
      <div class="mbti-group">
        <span class="type-label">생활 양식</span>
        <div class="btn-group">
          <input type="radio" class="btn-check" id="J" v-model="selectedJP" value="J">
          <label class="mbti-btn" :class="{ active: selectedJP === 'J' }" for="J">
            <div class="btn-content">
              <div class="type-info">
                <span class="type">J</span>
                <span class="description">판단형</span>
              </div>
              <span class="message">투자는 계획한 대로만 가야죠</span>
            </div>
          </label>
          
          <input type="radio" class="btn-check" id="P" v-model="selectedJP" value="P">
          <label class="mbti-btn" :class="{ active: selectedJP === 'P' }" for="P">
            <div class="btn-content">
              <div class="type-info">
                <span class="type">P</span>
                <span class="description">인식형</span>
              </div>
              <span class="message">시장 흐름 따라 유연하게 갈래요</span>
            </div>
          </label>
        </div>
      </div>
    </div>


  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useUserInterestStore } from '@/stores/userinterest'

const selectedEI = ref(null)
const selectedSN = ref(null)
const selectedTF = ref(null)
const selectedJP = ref(null)

const store = useUserInterestStore()

// watch로 mbti 선택할 때 마다 값 바뀌게 설정
watch([selectedEI, selectedSN, selectedTF, selectedJP], ([newEI, newSN, newTF, newJP]) => 
  {if (newEI && newSN && newTF && newJP) {store.usermbti = `${newEI}${newSN}${newTF}${newJP}`;}}, 
  { immediate: true })

</script>

<style scoped>
.mbti-container {
  padding: 2rem;
  background: white;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(139, 193, 72, 0.1);
  font-family: 'Godo', sans-serif;
}

.mbti-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.mbti-header h2 {
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 0.5rem;
  font-size: 2rem;
}

.mbti-grid {
  display: grid;
  gap: 2rem;
  margin-bottom: 2rem;
}

.mbti-group {
  background: #f8faf5;
  padding: 1.3rem;
  border-radius: 12px;
  transition: all 0.3s ease;
  border: 1px solid rgba(139, 193, 72, 0.1);
}

.mbti-group:hover {
  transform: translateY(-2px);
  border-color: var(--primary-color);
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.type-label {
  display: block;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
  text-align: center;
}


.btn-group {
  display: flex;
  gap: 1rem;
  width: 100%;
  flex-direction: column;
  /* justify-content: center; 중앙 정렬 */
}

.mbti-btn {
  width: 100%;
  padding: 1rem;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mbti-btn:hover {
  /* border-color: var(--primary-dark); */
  background: var(--primary-light);
}

.mbti-btn.active {
  background: var(--primary-light);
  border-color: var(--primary-light);
  color: var(--primary-word);
}

.mbti-btn.active .message{
  color: var(--primary-word);
}

.type-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.type {
  font-size: 2rem;
  font-weight: 700;
}

.description {
  font-size: 1.1rem;
  font-weight: 600;
}

.message {
  font-size: 0.9rem;
  color: #666;
}

.mbti-result {
  text-align: center;
  margin-top: 0.5rem;
  padding: 1.2rem;
  background: #f8faf5;
  border-radius: 10px;
  border: 1px solid var(--primary-dark);
  border: 1px solid rgba(139, 193, 72, 0.1);
}

.result-label {
  color: #333;
  margin-right: 0.8rem;
  font-size: 1.1rem;
}

.result-value {
  font-weight: 600;
  color: var(--primary-verydark);
  font-size: 2rem;
}

/* 모바일 반응형 수정 */
@media (max-width: 768px) {
  .btn-group {
    flex-direction: row; /* 모바일에서도 가로 배치 유지 */
    gap: 0.5rem; /* 간격 줄임 */
  }
  
  .mbti-btn {
    padding: 0.8rem;
  }
  
  .type {
    font-size: 1.2rem;
  }
  
  .description {
    font-size: 0.8rem;
  }
  
  .message {
    font-size: 0.7rem;
  }
}
</style>
