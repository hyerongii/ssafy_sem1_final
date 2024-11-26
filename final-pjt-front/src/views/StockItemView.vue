<template>
  <div class="container-fluid px-4 mt-5">
    <!-- 종목 헤더 섹션 -->
    <div class="stock-header mb-4">
      <h1 class="stock-title">{{ stockItemStore.stockInfo.articles_data?.stock_name }}</h1>
    </div>

    <div class="row gx-4 mb-4">
      <!-- 차트 섹션 -->
      <div class="col-lg-8">
        <!-- 네비게이션 Pills -->
        <div class="chart-nav-container">
          <ul class="nav nav-pills chart-nav">
            <li class="nav-item">
              <RouterLink 
                :to="{ name: 'day', params: { stock_id: stockcode }}" 
                class="nav-link"
                replace 
                :class="{ active: $route.name === 'day' || !$route.name }"
              >일</RouterLink>
            </li>
            <li>
            <RouterLink 
                :to="{ name: 'week', params: { stock_id: stockcode }}" 
                class="nav-link" 
                replace
                :class="{ active: $route.name === 'week' }"
                @click="movePeriodChart('W')"
              >주</RouterLink>
            </li>
            <li>
            <RouterLink 
                :to="{ name: 'month', params: { stock_id: stockcode }}" 
                class="nav-link" 
                replace
                :class="{ active: $route.name === 'month' }"
                @click="movePeriodChart('1M')"
              >월</RouterLink>
            </li>
            <li>
            <RouterLink 
                :to="{ name: 'sixmonth', params: { stock_id: stockcode }}" 
                class="nav-link" 
                replace
                :class="{ active: $route.name === 'sixmonth' }"
                @click="movePeriodChart('6M')"
              >6개월</RouterLink>
            </li>
            <li>
            <RouterLink 
                :to="{ name: 'year', params: { stock_id: stockcode }}" 
                class="nav-link" 
                replace
                :class="{ active: $route.name === 'year' }"
                @click="movePeriodChart('1Y')"
              >년</RouterLink>
            </li>
          </ul>
        </div>
        
        <!-- 차트 영역 -->
        <div class="chart-card">
          <RouterView></RouterView>
        </div>
      </div>

      <!-- 종목 정보 섹션 -->
      <div class="col-lg-4">
        <div class="info-card">
          <component :is="isNaN(stockcode) ? UsaStockInfo : DomesticStockInfo"/>
        </div>
      </div>
    </div>

    <!-- 커뮤니티 섹션 -->
    <div class="community-section mt-5">
      <div class="community-header">
        <h3 @click="moveCommunity" class="community-btn">실시간 커뮤니티</h3>
        <button class="write-btn" @click="writeArticle">
          <i class="bi bi-pencil-fill"></i>
          새 글 작성
        </button>
      </div>

      <!-- 게시글 목록 -->
      <div class="posts-container">
        <div v-for="article in latestArticles" 
            :key="article.id" 
            class="post-card">
          <div @click="moveArticleDetail(article.id)">
            <!-- 작성자 프로필 -->
            <div class="post-header" >
              <div class="profile">
                <img :src="profileImage" 
                    alt="프로필" 
                    class="profile-img">
                <div class="profile-info">
                  <span class="author">{{ article.author_nickname || '익명' }}</span>
                  <span class="mbti-tag">{{ article.author_mbti }}</span>
                  <span class="time">{{ formatTime(article.created_at) }}</span>
                </div>
              </div>
              <div class="post-menu">
                <i class="bi bi-three-dots"></i>
              </div>
            </div>
  
            <!-- 게시글 내용 -->
            <div class="post-content">
              <h4>{{ article.title }}</h4>
              <p>{{ article.content }}</p>
              <!-- <div class="theme-badge">
                # {{ article.theme__name }}
              </div> -->
            </div>
  
            <!-- 게시글 액션 -->
            <div class="post-actions">
              <button class="action-btn">
                <i class="bi bi-heart"></i>
                <span>좋아요</span>
              </button>
              <button class="action-btn">
                <i class="bi bi-chat"></i>
                <span>댓글</span>
              </button>
            </div>
          </div>
        </div>  
      </div>
    </div>
  </div>
</template>


<script setup>
import DomesticStockInfo from '@/components/stocks/DomesticStockInfo.vue'
import UsaStockInfo from '@/components/stocks/UsaStockInfo.vue'
import { useStockItemStore } from '@/stores/stockitem'
import { useUserInterestStore } from '@/stores/userinterest'
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'

const stockItemStore = useStockItemStore()
const interestStore = useUserInterestStore()
const route = useRoute()
const router = useRouter()
const stockcode = route.params.stock_id

// 입력 코드 국내/해외 인지 구분하기!
const checkDomestic = (stockcode) => isNaN(stockcode)

const getCurrentTime = () => {
  const now = new Date()
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')
  return `${hours}${minutes}${seconds}`
}

// 라우트링크 클릭할때는 주, 월, 년 각각 데이터 받아오기
const movePeriodChart = function (period) {
  // 주, 월, 년 함수
  stockItemStore.getPeriodInfo(stockcode, period)
  console.log(stockItemStore.periodChart)
}

const currentTime = getCurrentTime()

// const moveDayChart = function (stockcode){
//   stockItemStore.getDayInfo(stockcode, currentTime)
// }

// 페이지 처음 들어왔을때
onMounted(() => { 
  // 종목 정보 먼저 가져오기
  stockItemStore.getStockInfo(stockcode, currentTime)
  // 일 차트 그리기
  stockItemStore.getDayInfo(stockcode, currentTime)
  getProfileImage()
})

const moveCommunity = function () {
  router.push({ name: 'CommunityView', params: {stock_id : stockcode}})
}

const writeArticle = () => {
  // 글 작성 페이지로 이동하는 로직 구현
  router.push({
    name: 'CreateArticleView',
    params: { stock_id: stockcode }
  })
}

////커뮤니티 관련
// 최신 5개 게시글만 표시
// 진문수정 / 백엔드 데이터 전달 형식을 vue 형식으로 변환
const latestArticles = computed(() => {
  return stockItemStore.stockInfo.articles_data?.articles.map(article => ({
    ...article,
  })).slice(0,5) || [];
});

const formatTime = (timestamp) => {
  // 한국 시간으로 변환
  const date = new Date(timestamp)
  const now = new Date()

  // 한국 시간으로 조정 (UTC+9)
  const kstDate = new Date(date.getTime() + (9 * 60 * 60 * 1000))
  const diff = now - kstDate

  // 1시간 이내
  if (diff < 3600000) {
    const minutes = Math.floor(diff / 60000)
    return `${minutes}분 전`
  }
  // 24시간 이내
  if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000)
    return `${hours}시간 전`
  }
  // 그 외
  return `${kstDate.getMonth() + 1}월 ${kstDate.getDate()}일`
}

const moveArticleDetail = function (articleId) {
  router.push({name: 'ArticleDetailView', params:{ article_id : articleId }})
}

const profileImage = ref(null)
const getProfileImage = function () {
  const profileImages = [
    'penguin.png',
    'elephant.png',
    'lion.png',
    'dog.png',
    'cat.png',
    'pig.png',
    'sheep.png',
    'monkey.png',
    'rabbit.png',
    'tiger.png'
  ]
  const randomIndex = Math.floor(Math.random() * profileImages.length)
  const imageName = profileImages[randomIndex]
  profileImage.value = new URL(`../assets/profile/${imageName}`, import.meta.url).href
}

</script>

<style scoped>

.container-fluid {
  font-family: 'Godo', sans-serif;
  padding: 2rem;
}

.stock-header {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  border-left: 4px solid var(--primary-color);
  margin-bottom: 2rem;
}

.stock-title {
  color: var(--primary-word);
  font-size: 2rem;
  font-weight: 600;
  margin: 0;
}

/* 차트 네비게이션 */
.chart-nav-container {
  background: white;
  padding: 0.5rem;
  border-radius: 12px;
}

.chart-nav {
  display: flex;
  gap: 0.3rem;
}

.nav-pills .nav-link {
  color: var(--primary-word);
  background: white;
  border: 1px solid var(--primary-light); /* 테두리 두께 감소 */
  padding: 0.3rem 1rem; /* 패딩 감소 */
  border-radius: 15px; /* 둥글기 조정 */
  font-weight: 500;
  font-size: 0.9rem; /* 폰트 크기 감소 */
  transition: all 0.3s ease;
}

.nav-pills .nav-link:hover {
  background: var(--primary-light);
  color: white;
}

.nav-pills .nav-link.active {
  background: var(--primary-dark);
  color: white;
  box-shadow: 0 2px 4px rgba(139, 193, 72, 0.1); /* 그림자 효과 감소 */
}

.chart-card, .info-card {
  background: white;
  border-radius: 15px;
  padding: 0.5rem;
  height: calc(100vh - 250px);
  transition: all 0.3s ease;
}

.chart-card:hover, .info-card:hover {
  box-shadow: 0 5px 15px rgba(139, 193, 72, 0.1);
}

.period-tabs .nav-link {
  border-radius: 20px;
  padding: 0.6rem 1.5rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

/* 커뮤니티 섹션 */
.community-section {
  max-width: 1000px;
  margin: 2rem auto;
}


.community-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.write-btn {
  background: var(--primary-color);
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 25px;
  font-weight: 500;
  transition: all 0.3s ease;
}
.write-btn:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
}

.post-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  border: 2px solid rgba(139, 193, 72, 0.05); /* 더 은은한 보더 색상 */
  transition: all 0.3s ease;
}

.post-card:hover {
  border-color: var(--primary-color);
  transform: translateY(-2px);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.profile {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.profile-img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid var(--primary-light);
}

.profile-info {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.mbti-tag {
  font-size: 0.8rem;
  color: var(--primary-dark);
  background: var(--primary-light);
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
}

.author {
  font-weight: 600;
  font-size: 1rem;
  color: var(--primary-word);
}

.time {
  font-size: 0.8rem;
  color: #666;
  margin-left: auto;
}

.post-content {
  margin: 1rem 0;
}

.theme-badge {
  display: inline-block;
  padding: 0.4rem 1rem;
  background: #f0f2f5;
  border-radius: 20px;
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.5rem;
}

.post-actions {
  display: flex;
  gap: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(139, 193, 72, 0.05); /* 더 은은한 보더 색상 */
}

.action-btn {
  background: none;
  border: none;
  color: var(--primary-word);
  opacity: 0.8;
  transition: all 0.3s ease;
  padding: 0;
}

.action-btn:hover {
  color: var(--primary-dark);
  opacity: 1;
}

.community-btn {
  background: #F78CA0; 
  color: white;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 25px; /* 둥근 모서리 */
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
}

.community-btn:hover {
  background: var(--primary-color);
  transform: translateY(-2px);
}

.community-btn:active {
  transform: translateY(2px); /* 클릭 시 눌리는 효과 */
}
</style>