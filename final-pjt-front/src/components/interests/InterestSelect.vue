<template>
  <div class="interest-container">
    <div class="interest-box">
      <div class="interest-header text-center mb-4">
        <h2>요즘 나의 관심사는?</h2>
        <!-- <p class="text-muted">투자 성향에 맞는 테마를 추천해드립니다</p> -->
        <div class="selection-counter" :class="{ 'text-danger': selectedCategories.length < 3 }">
          {{ selectedCategories.length }}/3 선택됨
        </div>
      </div>

      <div class="d-flex flex-wrap justify-content-center gap-3">
        <div v-for="category in categories" 
            :key="category.value" 
            class="category-wrapper"
        >
          <button
            class="category-btn"
            :class="{ 'active': selectedCategories.includes(category) }"
            @click="toggleCategory(category)"
          >
            <div class="circle-text">{{ category.label }}</div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useUserInterestStore } from '@/stores/userinterest'
import { useAuthStore } from '@/stores/auth';

// const getCategoryIcon = (value) => {
//   const iconMap = {
//     shopping: 'bi bi-shop',
//     fashion: 'bi bi-bag-heart',
//     food: 'bi bi-cup-hot',
//     pet: 'bi bi-heart',
//     construct: 'bi bi-building',
//     game: 'bi bi-controller',
//     media: 'bi bi-play-circle',
//     travel: 'bi bi-airplane',
//     it: 'bi bi-cpu',
//     ev: 'bi bi-ev-station',
//     semiconductor: 'bi bi-cpu-fill',
//     aerospace: 'bi bi-rocket',
//     metaverse: 'bi bi-badge-vr',
//     vr: 'bi bi-badge-3d',
//     bankingSecurities: 'bi bi-bank',
//     blockchain: 'bi bi-link-45deg',
//     realestateReits: 'bi bi-houses',
//     renewableEnergy: 'bi bi-sun',
//     battery: 'bi bi-battery-charging'
//   }
//   return iconMap[value] || 'bi bi-tag'
// }


// 카테고리 리스트 정의
const categories = ref([
  { label: '쇼핑/유통', value: 'shopping', mapping: ['리테일/유통', '언택트 경제', '플랫폼 대표주자'] },
  { label: '패션/뷰티', value: 'fashion', mapping: ['어디 옷이야?', '뷰티의 세계', '럭셔리'] },
  { label: '식음료', value: 'food', mapping: ['갈증 해소', '프랜차이즈'] },
  { label: '반려동물', value: 'pet', mapping: ['반려동물'] },
  { label: '건설', value: 'construct', mapping: ['건물주의 꿈'] },
  { label: '게임', value: 'game', mapping: ['게임월드', '메타버스구현'] },
  { label: '미디어/컨텐츠', value: 'media', mapping: ['컨텐츠 강자', '스트리밍의 시대'] },
  { label: '여행', value: 'travel', mapping: ['이번 휴가는 어디?'] },
  { label: 'IT', value: 'it', mapping: ['인공지능(AI)', '스트리밍의 시대', '플랫폼 대표주자'] },
  { label: '전기차', value: 'ev', mapping: ['리튬 & 배터리', '자율주행차'] },
  { label: '반도체', value: 'semiconductor', mapping: ['반도체', '소재/원자재'] },
  { label: '우주항공 & 방위산업', value: 'aerospace', mapping: ['항공우주 & 방위산업'] },
  { label: '메타버스', value: 'metaverse', mapping: ['메타버스구현'] },
  { label: '가상현실', value: 'vr', mapping: ['가상현실(VR)'] },
  { label: '증권', value: 'bankingSecurities', mapping: ['핀테크', '플랫폼 대표주자', '언택트 경제'] },
  { label: '블록체인', value: 'blockchain', mapping: ['블록체인'] },
  { label: '부동산', value: 'realestateReits', mapping:['건물주의 꿈']},
  { label: '신재생에너지' ,value:'renewableEnergy' ,mapping:['클린 에너지','자원/에너지' ]},
  { label: '2차전지' ,value:'battery' ,mapping:['리튬 & 배터리']}
])

// 사용자가 선택한 카테고리를 저장하는 배열
const selectedCategories = ref([])

// 백엔드로 보낼 최종 관심사 데이터 (중복 제거된 매핑 값)
const userInterestMappings = ref([])

// 카테고리 선택 및 해제 함수
const toggleCategory = (category) => {
  if (selectedCategories.value.includes(category)) {
    // 이미 선택된 경우 해제
    selectedCategories.value = selectedCategories.value.filter(c => c !== category)
    // 해당 카테고리의 매핑 값도 제거
    userInterestMappings.value = userInterestMappings.value.filter(mapping => !category.mapping.includes(mapping))
  } else {
    // 선택되지 않은 경우 추가
    selectedCategories.value.push(category)
    // 해당 카테고리의 매핑 값을 추가 (중복 제거)
    userInterestMappings.value = [...new Set([...userInterestMappings.value, ...category.mapping])]
  }
}

const store = useUserInterestStore()
const authstore = useAuthStore()



// watch를 통해 userInterestMappings가 변경될 때마다 store.userinterest 업데이트
watch(userInterestMappings, (newMappings) => {
  store.userinterest = newMappings // 스토어에 최종 관심사 매핑 값 저장
}, { immediate:true })

</script>

<style scoped>
.interest-container {
  padding: 0.5 rem;
  font-family: 'Godo', sans-serif;
}

.interest-box {
  background: white;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 8px 20px rgba(139, 193, 72, 0.1);
  max-width: 1200px;
  margin: 0 auto;
}

.interest-header h2 {
  color: var(--primary-color);
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 2rem;
}

/* text-danger 클래스 스타일 수정 */
.text-danger {
  color: #D372A4 !important;
  font-weight: 700; /* 더 굵게 */
}

.selection-counter {
  display: inline-block;
  padding: 8px 16px;
  background: #f8faf5;
  border-radius: 20px;
  font-weight: 600; /* 폰트 굵기 증가 */
  font-size: 1.1rem; /* 폰트 크기 증가 */
  margin-top: 15px;
  border: 1px solid rgba(139, 193, 72, 0.2);
}

.d-flex {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  padding: 1rem;
}
  
/* .category-wrapper {
  width: 100%;
} */

.category-btn {
  width: 100%;
  padding: 0;
  border: none;
  background: transparent;
  cursor: pointer;
  transition: all 0.3s ease;
}

.circle-text {
  width: 100%;
  aspect-ratio: 1;
  border-radius: 50%;
  background: #f8faf5;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 15px;
  font-size: 1rem;
  color: #333;
  transition: all 0.3s ease;
  text-align: center;
  word-break: keep-all;
  border: 2px solid transparent;
}

.category-btn:hover .circle-text {
  border-color: var(--primary-dark);
  transform: translateY(-2px);
}

.category-btn.active .circle-text {
  background: var(--primary-dark);
  color: white;
  border-color: var(--primary-dark);
}

@media (max-width: 768px) {
  .d-flex {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
  
  .interest-box {
    padding: 20px;
  }
}

@media (max-width: 480px) {
  .d-flex {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
</style>