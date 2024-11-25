<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <!-- 게시글 카드 -->
        <div class="card shadow-sm mb-4">
          <div class="card-header bg-white">
            <div class="d-flex justify-content-between align-items-center">
              <div class="d-flex align-items-center">
                <img src="" alt="프로필" class="rounded-circle" style="width: 40px; height: 40px;">
                <div class="user-info ms-3">
                  <div class="d-flex align-items-center gap-2">
                    <h6 class="mb-0">{{ article?.article.author }}</h6>
                    <span class="mbti-badge">{{ article?.article.author_mbti }}</span>
                  </div>
                  <small class="text-muted">{{ article?.article.created_at }}</small>
                </div>
              </div>
            </div>
          </div>
          <div class="card-body">
            <h4 class="card-title">{{ article?.article.title }}</h4>
            <p class="card-text">{{ article?.article.content }}</p>
          </div>
        </div>

        <!-- 댓글 섹션 -->
        <div class="card shadow-sm">
          <div class="card-header bg-white">
            <h6 class="mb-0">댓글 {{ article?.comments?.length || 0 }}개</h6>
          </div>
          <!-- 댓글 목록 -->
          <ul class="list-group list-group-flush">
            <li v-for="comment in article?.comments" :key="comment.id" class="list-group-item">
              <div class="d-flex justify-content-between align-items-start">
                <div class="comment-content w-100">
                  <div class="d-flex justify-content-between align-items-center mb-1">
                    <small class="text-muted">{{ comment.user }}</small>
                    <div class="comment-actions" v-if="comment.user === userNickname">
                      <button class="btn btn-sm btn-link text-muted" @click="startEdit(comment)">
                        <i class="bi-pencil-square"></i>
                      </button>
                      <button class="btn btn-sm btn-link text-danger" @click="deleteComment(comment.id)">
                        <i class="bi-trash"></i>
                      </button>
                    </div>
                  </div>
                  <div v-if="comment.isEditing">
                    <div class="input-group mb-2">
                      <textarea 
                        v-model="comment.editContent" 
                        class="form-control"
                        rows="2"
                      ></textarea>
                      <button class="btn btn-outline-primary" @click="saveEdit(comment)">저장</button>
                      <button class="btn btn-outline-secondary" @click="cancelEdit(comment)">취소</button>
                    </div>
                  </div>
                  <p v-else class="comment-text mb-1">{{ comment.content }}</p>
                  <small class="text-muted">{{ formatDateTime(article?.article.created_at) }}</small>
                </div>
              </div>
            </li>
          </ul>
          <!-- 댓글 작성 폼 -->
          <div class="card-footer bg-white">
            <form @submit.prevent="submitComment(articleId, comment)">
              <div class="input-group">
                <textarea 
                  v-model="comment" 
                  class="form-control" 
                  placeholder="댓글을 입력하세요..."
                  rows="2"
                ></textarea>
                <button type="submit" class="btn btn-primary">작성</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const authstore = useAuthStore()
const route = useRoute()
const articleId = route.params.article_id
const comment = ref('')
const article = ref(null)
const userNickname = ref(null)

// 시간 포맷팅 함수 추가
const formatDateTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  
  return `${year}.${month}.${day} ${hours}:${minutes}`
}

const startEdit = (comment) => {
  comment.isEditing = true;
  comment.editContent = comment.content;
}

const cancelEdit = (comment) => {
  comment.isEditing = false;
  comment.editContent = '';
}

const saveEdit = (comment) => {
  editComment(comment.id, comment.editContent);
  comment.isEditing = false;
}


// 게시글 상세 조회
const getArticleDetail = function(articleId) {
  axios({
    method: 'get',
    url: `${authstore.API_URL}/api/v1/stock/article/${articleId}/`, 
    headers: {
      Authorization: `Bearer ${authstore.token}`,
    },
  })
    .then((res) => {
      console.log('상세 조회 완료')
      console.log(res.data)
      article.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
}

// 댓글 작성
const submitComment = function(articleId, commentText) {
  axios({
    method: 'post',
    url: `${authstore.API_URL}/api/v1/stock/article/${articleId}/`,
    headers: {
      Authorization: `Bearer ${authstore.token}`,
    },
    data: {
      content: commentText
    }
  })
    .then((res) => {
      console.log('댓글 작성 완료')
      comment.value = ''
      getArticleDetail(articleId)
    })
    .catch((err) => {
      console.log(err)
    })
}

// 댓글 수정
const editComment = function(commentId, commentText) {
  if (!commentText?.trim()) return;
  
  axios({
    method: 'put',
    url: `${authstore.API_URL}/api/v1/stock/comment/${commentId}/`,
    headers: {
      Authorization: `Bearer ${authstore.token}`,
    },
    data: {
      content: commentText
    }
  })
    .then(() => {
      getArticleDetail(articleId)
    })
    .catch((err) => {
      console.log(err)
    })
}

// 댓글 삭제
const deleteComment = function(commentId) {
  if (!confirm('댓글을 삭제하시겠습니까?')) return;
  
  axios({
    method: 'delete',
    url: `${authstore.API_URL}/api/v1/stock/comment/${commentId}/`,
    headers: {
      Authorization: `Bearer ${authstore.token}`,
    }
  })
    .then(() => {
      getArticleDetail(articleId)
    })
    .catch((err) => {
      console.log(err)
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
      userNickname.value = res.data.nickname
    })
    .catch((err) => {
      console.log(err)
    })
}


onMounted(() => {
  getArticleDetail(articleId)
  getUserInfo()
})

</script>

<style scoped>
.container {
  font-family: 'Godo', sans-serif;
  padding: 2rem;
}

.card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(139, 193, 72, 0.1);
  transition: all 0.3s ease;
  border: 1px solid rgba(139, 193, 72, 0.1);
  margin-bottom: 2rem;
}

.card-header {
  background: white;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(139, 193, 72, 0.1);
}

.card-title {
  color: var(--primary-word);
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.card-text {
  color: #555;
  line-height: 1.6;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

/* 댓글 섹션 */
.list-group-item {
  padding: 1.2rem;
  border-bottom: 1px solid rgba(139, 193, 72, 0.1);
  transition: all 0.2s ease;
}

.list-group-item:hover {
  background-color: #f8faf5;
}

.comment-content small {
  color: var(--primary-dark);
  font-weight: 500;
}

.comment-text {
  color: var(--primary-word);
  margin: 0.5rem 0;
}

/* 댓글 작성 폼 */
.card-footer {
  padding: 1.5rem;
  background: white;
}

.form-control {
  border: 1px solid rgba(139, 193, 72, 0.2);
  border-radius: 12px;
  padding: 0.8rem;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 0.2rem rgba(139, 193, 72, 0.1);
}

/* 버튼 스타일 */
.btn-primary {
  background: var(--primary-color);
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
}

.btn-link {
  color: var(--primary-color);
  transition: all 0.2s ease;
}

.btn-link:hover {
  color: var(--primary-dark);
}

/* 댓글 수정/삭제 버튼 */
.comment-actions {
  opacity: 0;
  transition: opacity 0.2s ease;
}

.list-group-item:hover .comment-actions {
  opacity: 1;
}

.comment-actions .btn {
  padding: 0.4rem;
  margin-left: 0.5rem;
}

/* 수정 폼 */
.input-group {
  gap: 0.5rem;
}

.input-group .btn {
  border-radius: 12px;
}

.btn-outline-primary {
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.btn-outline-primary:hover {
  background: var(--primary-color);
  color: white;
}

.btn-outline-secondary {
  color: var(--primary-dark);
  border-color: var(--primary-dark);
}

.btn-outline-secondary:hover {
  background: var(--primary-dark);
  color: white;
}

</style>