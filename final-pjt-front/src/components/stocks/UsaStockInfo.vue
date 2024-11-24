<template>
  <div class="stock-info-wrapper">
    <div class="info-card" v-if="stockItemStore.stockInfo">
      <!-- 재무비율 정보 섹션 -->
      <div class="info-section" v-if="stockItemStore.stockInfo.ratio_data?.length">
        <h3 class="section-title">재무비율 정보</h3>
        <div class="ratio-grid">
          <div class="ratio-card">
            <div class="ratio-icon">PER</div>
            <div class="ratio-value">{{ stockItemStore.stockInfo.ratio_data[0].PER }}</div>
            <div class="ratio-label">주가수익비율</div>
          </div>
          <div class="ratio-card">
            <div class="ratio-icon">PBR</div>
            <div class="ratio-value">{{ stockItemStore.stockInfo.ratio_data[0].PBR }}</div>
            <div class="ratio-label">주가순자산비율</div>
          </div>
          <div class="ratio-card">
            <div class="ratio-icon">EPS</div>
            <div class="ratio-value">{{ stockItemStore.stockInfo.ratio_data[0].EPS }}</div>
            <div class="ratio-label">주당순이익</div>
          </div>
          <div class="ratio-card">
            <div class="ratio-icon">BPS</div>
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

.info-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
}

.info-section {
  padding: 1.5rem;
  border-bottom: 1px solid #eef2f6;
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
  color: #3b82f6;
  margin-bottom: 0.5rem;
}

.ratio-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.3rem;
}

.ratio-label {
  font-size: 0.8rem;
  color: #64748b;
}

.consensus-card {
  background: #f8fafc;
  padding: 1.2rem;
  border-radius: 8px;
}

.consensus-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.consensus-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
  background: #e2e8f0;
  color: #64748b;
}

.consensus-badge.buy {
  background: #dcfce7;
  color: #166534;
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