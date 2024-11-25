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
        <div class="chart-nav-container mb-4">
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
                <img :src="article.author_nickname ? `/profiles/${article.author_nickname}.jpg` : '/default-avatar.png'" 
                    alt="프로필" 
                    class="profile-img">
                <div class="profile-info">
                  <span class="author">{{ article.author_nickname || '익명' }}</span>
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
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'

const stockItemStore = useStockItemStore()
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
    author_nickname: article.author__nickname, // 키 변환
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

</script>

<style scoped>
.stock-header {
  background: white;
  padding: 1.5rem;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.chart-card, .info-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  height: calc(100vh - 250px);
}

.period-tabs .nav-link {
  border-radius: 20px;
  padding: 0.6rem 1.5rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.community-section {
  max-width: 800px;
  margin: 0 auto;
}

.community-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.write-btn {
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 25px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: transform 0.3s ease;
}

.post-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
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
  width: 45px;
  height: 45px;
  border-radius: 50%;
  object-fit: cover;
}

.profile-info {
  display: flex;
  flex-direction: column;
}

.author {
  font-weight: 600;
  font-size: 1rem;
}

.time {
  font-size: 0.8rem;
  color: #666;
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
  border-top: 1px solid #eee;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  color: #666;
  font-size: 0.9rem;
  padding: 0.5rem;
  border-radius: 20px;
  transition: background-color 0.3s ease;
}

.action-btn:hover {
  background-color: #f0f2f5;
}

.chart-nav-container {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 15px;
}

.chart-nav {
  display: flex;
  gap: 0.5rem;
}

.nav-pills .nav-link {
  color: #495057;
  background-color: white;
  border: 1px solid #dee2e6;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.nav-pills .nav-link:hover {
  background-color: #e9ecef;
}

.nav-pills .nav-link.active {
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  color: white;
  border: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.community-btn {
  background: linear-gradient(135deg, #007bff, #0056b3); /* 파란색 그라데이션 */
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
  background: linear-gradient(135deg, #0056b3, #003d80); /* 호버 시 더 어두운 파란색 */
  transform: translateY(-2px); /* 살짝 위로 올라가는 효과 */
}

.community-btn:active {
  transform: translateY(2px); /* 클릭 시 눌리는 효과 */
}
</style>