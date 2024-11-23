<template>
  <div class="container mt-5" v-if="store.articles?.articles_data">
    <div class="community-header">
      <h1 class="text-center mb-4">{{ store.articles?.articles_data?.stock_name }} 주주님들 모이세요!</h1>
      <div class="d-flex justify-content-end mb-4">
        <button class="btn btn-primary rounded-pill px-4" @click="articleCreate">
          <i class="bi bi-pencil-fill me-2"></i>글 작성하기
        </button>
      </div>
    </div>

    <!-- 게시글 목록 -->
    <div class="posts-container">
      <div v-for="article in store.articles.articles_data.articles" :key="article.id" class="post-card">
        <!-- 게시글 헤더 -->
        <div class="post-header" @click="moveArticleDetail(article.id)">
          <div class="user-info">
            <div class="user-avatar">
              <img src="" alt="프로필" class="rounded-circle">
            </div>
            <div class="user-details">
              <span class="author">{{ article.author__nickname || '익명' }}</span>
              <span class="post-time">{{ article.created_at }}</span>
            </div>
          </div>
          <div class="post-menu dropdown">
            <i class="bi bi-three-dots-vertical"></i>
          </div>
        </div>

        <!-- 게시글 내용 -->
        <div class="post-content" >
          <h5 class="post-title">{{ article.title }}</h5>
          <p class="post-text">{{ article.content }}</p>
          <!-- <div class="theme-tag">
            <span class="badge rounded-pill bg-light text-dark">
              # {{ article.theme__name }}
            </span>
          </div> -->
        </div>

        <!-- 게시글 액션 버튼 -->
        <div class="post-actions">
          <button class="action-btn">
            <i class="bi bi-heart"></i>
            <span>좋아요</span>
          </button>
          <button class="action-btn">
            <i class="bi bi-chat"></i>
            <span>댓글</span>
          </button>
          <button class="action-btn" @click="editArticle(article)">
            <i class="bi bi-pencil"></i>
            <span>수정</span>
          </button>
          <button class="action-btn" @click="deleteArticle(article.id)">
            <i class="bi bi-trash"></i>
            <span>삭제</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useStockItemStore } from '@/stores/stockitem'
import axios from 'axios'
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const store = useStockItemStore()
const stockcode = route.params.stock_id
const authstore = useAuthStore()

const getCurrentTime = () => {
  const now = new Date()
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')
  return `${hours}${minutes}${seconds}`
}

const currentTime = getCurrentTime()

onMounted(() => {
  store.getArticleInfo(stockcode, currentTime)
  console.log(store.articles)
})

const articleCreate = function () {
  router.push({name: 'CreateArticleView', params: {stock_id : stockcode}})
}

// 게시글 삭제
const deleteArticle = function (article_id) {
  axios({
    method: 'delete',
    url: `${authstore.API_URL}/api/v1/stock/article/update_or_delete/`,
    headers: {
      Authorization: `Bearer ${authstore.token}`,
    },
    data: {
      article_id: article_id, 
    }
  })
    .then((res) => {
      console.log('게시글 삭제 성공')

    })
    .catch((err) => {
      console.log(err)
    })
}

// 게시글 수정
const editArticle = function (article) {
  router.push({
    name: 'CreateArticleView', 
    params: { stock_id: stockcode },
    query: {
      edit: true,
      articleId: article.id,
      title: article.title,
      content: article.content
    }
  })
}

// 댓글 조회
const getArticleComments = function(articleId) {
  axios({
    method: 'get',
    url: `${authstore.API_URL}/api/v1/stock/article/detail/`, 
    headers: {
      Authorization: `Bearer ${authstore.token}`,
    },
    data: {
      article_id: articleId,
    }
  })
    .then((res) => {
      console.log('댓글 조회 완료')
    })
    .catch((err) => {
      console.log(err)
    })
}

const toggleComments = function(article) {
  article.showComments = !article.showComments;
  if (article.showComments && !article.comments) {
    getArticleComments(article.id);
  }
}

const moveArticleDetail = function (articleId) {
  router.push({name: 'ArticleDetailView', params:{ article_id : articleId }})
}

</script>

<style scoped>
.community-header {
  max-width: 800px;
  margin: 0 auto;
}

.posts-container {
  max-width: 800px;
  margin: 0 auto;
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

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-avatar img {
  width: 45px;
  height: 45px;
  object-fit: cover;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.author {
  font-weight: 600;
  font-size: 1rem;
}

.post-time {
  font-size: 0.8rem;
  color: #666;
}

.post-content {
  margin: 1rem 0;
}

.post-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.post-text {
  color: #444;
  font-size: 0.95rem;
  margin-bottom: 1rem;
}

.theme-tag {
  margin-bottom: 0.5rem;
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
  transition: all 0.3s ease;
}

.action-btn:hover {
  background-color: #f0f2f5;
  color: #2575fc;
}

.btn-primary {
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  border: none;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}
</style>