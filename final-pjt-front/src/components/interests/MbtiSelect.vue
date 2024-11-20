<template>
  <div class="mbti-container">
    <div class="mbti-header">
      <h2>나의 MBTI는?</h2>
      <p class="text-muted">당신의 성향에 맞는 투자 스타일을 찾아드립니다</p>
    </div>

    <div class="mbti-grid">
      <!-- E/I 선택 -->
      <div class="mbti-group">
        <span class="type-label">에너지 방향</span>
        <div class="btn-group">
          <input type="radio" class="btn-check" id="E" v-model="selectedEI" value="E">
          <label class="mbti-btn" :class="{ active: selectedEI === 'E' }" for="E">
            <span class="type">E</span>
            <span class="description">외향형</span>
          </label>
          
          <input type="radio" class="btn-check" id="I" v-model="selectedEI" value="I">
          <label class="mbti-btn" :class="{ active: selectedEI === 'I' }" for="I">
            <span class="type">I</span>
            <span class="description">내향형</span>
          </label>
        </div>
      </div>

      <!-- S/N 선택 -->
      <div class="mbti-group">
        <span class="type-label">인식 방식</span>
        <div class="btn-group">
          <input type="radio" class="btn-check" id="S" v-model="selectedSN" value="S">
          <label class="mbti-btn" :class="{ active: selectedSN === 'S' }" for="S">
            <span class="type">S</span>
            <span class="description">감각형</span>
          </label>
          
          <input type="radio" class="btn-check" id="N" v-model="selectedSN" value="N">
          <label class="mbti-btn" :class="{ active: selectedSN === 'N' }" for="N">
            <span class="type">N</span>
            <span class="description">직관형</span>
          </label>
        </div>
      </div>

      <!-- T/F 선택 -->
      <div class="mbti-group">
        <span class="type-label">판단 기준</span>
        <div class="btn-group">
          <input type="radio" class="btn-check" id="T" v-model="selectedTF" value="T">
          <label class="mbti-btn" :class="{ active: selectedTF === 'T' }" for="T">
            <span class="type">T</span>
            <span class="description">사고형</span>
          </label>
          
          <input type="radio" class="btn-check" id="F" v-model="selectedTF" value="F">
          <label class="mbti-btn" :class="{ active: selectedTF === 'F' }" for="F">
            <span class="type">F</span>
            <span class="description">감정형</span>
          </label>
        </div>
      </div>

      <!-- J/P 선택 -->
      <div class="mbti-group">
        <span class="type-label">생활 양식</span>
        <div class="btn-group">
          <input type="radio" class="btn-check" id="J" v-model="selectedJP" value="J">
          <label class="mbti-btn" :class="{ active: selectedJP === 'J' }" for="J">
            <span class="type">J</span>
            <span class="description">판단형</span>
          </label>
          
          <input type="radio" class="btn-check" id="P" v-model="selectedJP" value="P">
          <label class="mbti-btn" :class="{ active: selectedJP === 'P' }" for="P">
            <span class="type">P</span>
            <span class="description">인식형</span>
          </label>
        </div>
      </div>
    </div>

    <div class="mbti-result" v-if="store.usermbti">
      <span class="result-label">선택한 MBTI:</span>
      <span class="result-value">{{ store.usermbti }}</span>
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
  box-shadow: 0 8px 20px rgba(0,0,0,0.05);
}

.mbti-header {
  text-align: center;
  margin-bottom: 2rem;
}

.mbti-header h2 {
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.mbti-grid {
  display: grid;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.mbti-group {
  background: #f8fafc;
  padding: 1.5rem;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.mbti-group:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}

.type-label {
  display: block;
  font-weight: 600;
  color: #4a5568;
  margin-bottom: 1rem;
}

.btn-group {
  display: flex;
  gap: 1rem;
  width: 100%;
}

.mbti-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.mbti-btn:hover {
  border-color: #667eea;
  background: #f7fafc;
}

.mbti-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  color: white;
}

.type {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.description {
  font-size: 0.9rem;
}

.mbti-result {
  text-align: center;
  margin-top: 2rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 10px;
}

.result-label {
  color: #4a5568;
  margin-right: 0.5rem;
}

.result-value {
  font-weight: 600;
  color: #667eea;
  font-size: 1.2rem;
}

@media (max-width: 768px) {
  .mbti-container {
    padding: 1rem;
  }
  
  .btn-group {
    flex-direction: column;
  }
}
</style>
