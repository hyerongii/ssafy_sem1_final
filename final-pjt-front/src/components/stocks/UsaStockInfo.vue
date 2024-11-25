<template>
  <div class="stock-info-wrapper">
    <div class="info-card" v-if="stockItemStore.stockInfo">
      <!-- 재무비율 정보 섹션 -->
      <div class="info-section" v-if="stockItemStore.stockInfo.ratio_data?.length">
        <h3 class="section-title">재무비율 정보</h3>
        <div class="ratio-grid">
          <div class="ratio-card">
            <div class="ratio-header">
              <div class="ratio-icon">PER</div>
              <div class="info-icon" data-tooltip="주가가 1주당 순이익의 몇 배인지 나타내는 수치로, 숫자가 낮을수록 주가가 저평가되어 있어요!">
                <i class="bi bi-info-circle-fill"></i>
              </div>
            </div>
            <div class="ratio-value">{{ stockItemStore.stockInfo.ratio_data[0].PER }}</div>
            <div class="ratio-label">주가수익비율</div>
          </div>
          <div class="ratio-card">
            <div class="ratio-header">
              <div class="ratio-icon">PBR</div>
              <div class="info-icon" data-tooltip="회사의 장부 가치 대비 현재 주가가 몇 배인지 보여주는 지표에요!">
                <i class="bi bi-info-circle-fill"></i>
              </div>
            </div>
            <div class="ratio-value">{{ stockItemStore.stockInfo.ratio_data[0].PBR }}</div>
            <div class="ratio-label">주가순자산비율</div>
          </div>
          <div class="ratio-card">
            <div class="ratio-header">
              <div class="ratio-icon">EPS</div>
              <div class="info-icon" data-tooltip="회사가 1년 동안 번 돈을 총 주식 수로 나눈 값으로, &#10;1주당 얼마를 벌었는지 보여줘요!">
                <i class="bi bi-info-circle-fill"></i>
              </div>
            </div>
            <div class="ratio-value">{{ stockItemStore.stockInfo.ratio_data[0].EPS }}</div>
            <div class="ratio-label">주당순이익</div>
          </div>
          <div class="ratio-card">
            <div class="ratio-header">
              <div class="ratio-icon">BPS</div>
              <div class="info-icon" data-tooltip="주식 한 주당 회사의 순자산(자산-부채)이 얼마인지 나타내는 지표에요!">
                <i class="bi bi-info-circle-fill"></i>
              </div>
            </div>
            <div class="ratio-value">{{ stockItemStore.stockInfo.ratio_data[0].BPS }}</div>
            <div class="ratio-label">주당순자산</div>
          </div>
        </div>
      </div>
      <!-- 재무비율 정보 섹션 아래에 추가 -->
      <div class="info-section">
        <h3 class="section-title">컨센서스 정보</h3>
        <div class="consensus-card">
          <div class="no-data-message">
            <i class="bi bi-info-circle"></i>
            <p>미국 주식 종목의 경우 컨센서스 정보를 제공하지 않습니다.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useStockItemStore } from '@/stores/stockitem'
import { computed, onMounted, ref } from 'vue'

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

</script>

<style scoped>
.stock-info-wrapper {
  padding: 1rem;
}

.ratio-header {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  margin-bottom: 0.5rem;
}

.info-icon {
  position: absolute;
  left: 0;
  color: #64748b;
  cursor: help;
  justify-content: center;
}


.info-icon i {
  font-size: 0.7rem;
  font-weight: bold; /* 아이콘 두께 증가 */
}

.info-icon:hover::before {
  content: attr(data-tooltip);
  position: fixed;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  width: max-content;
  max-width: 350px;
  padding: 0.8rem;
  background:  #f8fafc;
  /* border: 2px solid #64748b; */
  border-radius: 8px;
  font-size: 0.85rem;
  color: #1e293b;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 9999;
  opacity: 0;
  animation: fadeIn 0.2s ease-in-out forwards;
  white-space: pre-line; /* 줄바꿈 허용 */
}

.info-icon:hover::after {
  content: '';
  position: absolute;
  top: -5px;
  left: 50%;
  transform: translateX(-50%);
  border-width: 5px;
  border-style: solid;
  border-color: transparent transparent transparent transparent;
  z-index: 1000;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translate(-50%, 10px);
  }
  to {
    opacity: 1;
    transform: translate(-50%, -5px);
  }
}


.info-card {
  background: white;
  border-radius: 12px;
  overflow: visible !important; /* overflow 제한 해제 */
}

.info-section {
  padding: 1rem;
  padding-bottom: 2rem;
  margin-top: 2rem;
  border-bottom: 1px solid #eef2f6;
  overflow: visible !important; /* overflow 제한 해제 */
}

.info-section:last-child {
  border-bottom: none;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.ratio-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.ratio-card {
  background: #f8fafc;
  padding: 1.0rem;
  border-radius: 8px;
  text-align: center;
  transition: transform 0.2s;
}

.ratio-card:hover {
  transform: translateY(-2px);
}

.ratio-icon {
  font-size: 1.2rem;
  font-weight: 600;
  color: #488bc1;
}

.ratio-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.3rem;
}

.ratio-label {
  font-size: 0.7rem;
  color: #64748b;
}

.consensus-card {
  background: #f8fafc;
  padding: 1.2rem;
  border-radius: 8px;
}

.consensus-source {
  font-size: 0.9rem;
  color: #64748b;
}

@media (max-width: 768px) {
  .ratio-grid {
    grid-template-columns: 1fr;
    gap: 0.8rem;
  }
  
  .ratio-card {
    padding: 1rem;
  }

  .info-icon:hover::before {
    width: 250px;
    font-size: 0.8rem;
  }
}

.no-data-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1.5rem;
  color: #64748b;
  text-align: center;
}

.no-data-message i {
  font-size: 1.2rem;
  color: #94a3b8;
}

.no-data-message p {
  margin: 0;
  font-size: 0.95rem;
}
</style>