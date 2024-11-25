<template>
  <div class="container mt-5" v-if="store.articles?.articles_data">
    <div class="community-header">
      <h1 class="text-center mb-4">
        <span @click="navigateToStock(stockcode)">{{ store.articles?.articles_data?.stock_name }}</span> 주주님들 모이세요!
      </h1>
      <div class="d-flex justify-content-end mb-4">
        <button class="btn btn-primary rounded-pill px-4" @click="articleCreate">
          <i class="bi bi-pencil-fill me-2"></i>글 작성하기
        </button>
      </div>
    </div>

    <!-- 게시글 목록 -->
    <div class="posts-container">
      <div v-for="article in store.articles.articles_data.articles" :key="article.id" class="post-card">
        <div @click="moveArticleDetail(article.id)">
          <!-- 게시글 헤더 -->
          <div class="post-header">
            <div class="user-info">
              <div class="user-avatar">
                <img src="" alt="프로필" class="rounded-circle">
              </div>
              <div class="user-details">
                <span class="author">{{ article.author_nickname || '익명' }}</span>
                <span class="mbti">{{ article.author_mbti}}</span>
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
            <!-- <p class="post-text">{{ article.content }}</p> -->
            <div class="theme-tag">
              <span class="badge rounded-pill bg-light text-dark">
                # {{ article.theme_name }}
              </span>
            </div>
          </div>
        </div>
          <!-- 게시글 액션 버튼 -->
          <div class="post-actions">
            <button class="action-btn">
              <i class="bi bi-heart"></i>
              <span>좋아요</span>
            </button>
            <button class="action-btn" @click="moveArticleDetail(article.id)">
              <i class="bi bi-chat"></i>
              <span>댓글</span>
            </button>
            <!-- 작성자와 현재 로그인한 사용자가 같을 때만 수정/삭제 버튼 표시 -->
            <template v-if="article.author_nickname === userNickname">
              <button class="action-btn" @click.stop="editArticle(article)">
                <i class="bi bi-pencil"></i>
                <span>수정</span>
              </button>
              <button class="action-btn" @click.stop="deleteArticle(article.id)">
                <i class="bi bi-trash"></i>
                <span>삭제</span>
              </button>
            </template>
          </div>
      </div>
    </div>
  </div>
  <div class="modal fade" id="deleteModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">게시글 삭제</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          정말 이 게시글을 삭제하시겠습니까?
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">취소</button>
          <button type="button" class="btn btn-danger" @click="confirmDelete">삭제</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import * as bootstrap from 'bootstrap'
import { useArticleStore } from '@/stores/article'
import { useAuthStore } from '@/stores/auth'
import { useStockItemStore } from '@/stores/stockitem'
import axios from 'axios'
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const authstore = useAuthStore()
const articlestore = useArticleStore()
const route = useRoute()
const router = useRouter()
const store = useStockItemStore()
const stockcode = route.params.stock_id
const userNickname = ref(null)
const userMbti = ref(null)

userMbti.value = articlestore.userMbti

// 삭제할 게시글 ID 저장용 ref 추가
const deleteArticleId = ref(null)

// 삭제 버튼 클릭 시 모달 표시
const showDeleteModal = (articleId) => {
  deleteArticleId.value = articleId
  const modalElement = document.getElementById('deleteModal')
  if (modalElement) {
    const modal = new bootstrap.Modal(modalElement)
    modal.show()
  }
}

const deleteArticle = function (article_id) {
  showDeleteModal(article_id)  // 먼저 모달을 보여주고
}

// 모달에서 삭제 확인 시 실행되는 함수
const confirmDelete = () => {
  if (deleteArticleId.value) {
    axios({
      method: 'delete',
      url: `${authstore.API_URL}/api/v1/stock/article/update_or_delete/`,
      headers: {
        Authorization: `Bearer ${authstore.token}`,
      },
      data: {
        article_id: deleteArticleId.value,
      }
    })
      .then(() => {
        const modalElement = document.getElementById('deleteModal')
        const modal = bootstrap.Modal.getInstance(modalElement)
        if (modal) {
          modal.hide()
        }
        store.getArticleInfo(stockcode, getCurrentTime())
      })
      .catch((err) => {
        console.log(err)
      })
  }
}

const getCurrentTime = () => {
  const now = new Date()
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')
  return `${hours}${minutes}${seconds}`
}

const currentTime = getCurrentTime()

onMounted(() => {
  console.log(store.articles)
  store.getArticleInfo(stockcode, currentTime)
  console.log(authstore.user.pk)
  getUserInfo()
})

const articleCreate = function () {
  router.push({name: 'CreateArticleView', params: {stock_id : stockcode}})
}

// 게시글 삭제
// const deleteArticle = function (article_id) {
//   showDeleteModal(article_id)
//   axios({
//     method: 'delete',
//     url: `${authstore.API_URL}/api/v1/stock/article/update_or_delete/`,
//     headers: {
//       Authorization: `Bearer ${authstore.token}`,
//     },
//     data: {
//       article_id: article_id, 
//     }
//   })
//     .then((res) => {
//       console.log('게시글 삭제 성공')
//       // 게시글 목록 새로고침
//       store.getArticleInfo(stockcode, getCurrentTime())
//     })
//     .catch((err) => {
//       console.log(err)
//     })
// }

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

const getUserInfo = function() {
  axios({
    method: 'get',
    url: `${authstore.API_URL}/api/v1/user_info/${authstore.user.pk}/`,
    headers: {
      Authorization: `Bearer ${authstore.token}`,
    },
  })
    .then((res) => {
      console.log('유저정보조회완료')
      console.log(res.data)
      userNickname.value = res.data.user.nickname
      userMbti.value = res.data.user_info.mbti
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

const navigateToStock = function (stock_id) {
  router.push({name: 'StockItemView', params:{ stock_id : stock_id }})
}

</script>

<style scoped>

.container {
  font-family: 'Godo', sans-serif;
  padding: 2rem;
}

/* 모달 스타일 */
.modal-content {
  border: none;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(139, 193, 72, 0.1);
  font-family: 'Godo', sans-serif;
}

.modal-header {
  background: white;
  border-bottom: 1px solid rgba(139, 193, 72, 0.1);
  border-radius: 15px 15px 0 0;
  padding: 1.5rem;
}

.modal-title {
  color: var(--primary-word);
  font-weight: 600;
  font-size: 1.3rem;
}

.modal-body {
  padding: 2rem;
  color: var(--primary-word);
  font-size: 1.1rem;
  text-align: center;
}

.modal-footer {
  border-top: 1px solid rgba(139, 193, 72, 0.1);
  padding: 1rem 1.5rem;
  border-radius: 0 0 15px 15px;
}

.btn-secondary {
  background-color: #f8faf5;
  color: var(--primary-word);
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background-color: #e9ecef;
  transform: translateY(-2px);
}

.btn-danger {
  background-color: var(--primary-dark);
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-danger:hover {
  background-color: var(--primary-verydark);
  transform: translateY(-2px);
}

.btn-close:focus {
  box-shadow: none;
}

.community-header h1 {
  font-size: 1.8rem;
  color: var(--primary-word);
  margin-top: 2rem;
  margin-bottom: 2rem;
  font-weight: 600;
}

.btn-primary {
  background-color: var(--primary-dark);
  border: none;
  padding: 0.8rem 1.5rem;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(139, 193, 72, 0.2);
}

.btn-primary:hover {
  background-color: var(--primary-color);
  transform: translateY(-2px);
}

.posts-container {
  max-width: 800px;
  margin: 0 auto;
}

.post-card {
  background: white;
  border-radius: 16px;
  padding: 1.8rem;
  margin-bottom: 1.5rem;
  border: 1px solid rgba(139, 193, 72, 0.1);
  transition: all 0.3s ease;
}

.post-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(139, 193, 72, 0.1);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.2rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-avatar img {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: 2px solid var(--primary-light);
}

.user-details {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.author {
  font-weight: 600;
  font-size: 1.3rem;
  color: var(--primary-word);
}

.mbti {
  font-size: 0.9rem;
  color: var(--primary-verydark);
  background: var(--primary-light);
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
}

.post-time {
  font-size: 0.8rem;
  color: #666;
  margin-left: auto;
}

.post-content {
  padding: 0.5rem 0;
}

.post-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--primary-word);
  margin-bottom: 1rem;
}

.post-text {
  color: #555;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.theme-tag {
  margin-bottom: 0.5rem;
}

.post-actions {
  display: flex;
  gap: 1.2rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(139, 193, 72, 0.1);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  color: var(--primary-word);
  font-size: 0.9rem;
  padding: 0.5rem 0.8rem;
  border-radius: 20px;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background-color: var(--primary-light);
  color: var(--primary-dark);
}

.action-btn i {
  font-size: 1.1rem;
}
</style>