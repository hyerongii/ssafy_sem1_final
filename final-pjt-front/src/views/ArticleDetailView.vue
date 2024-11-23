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
                <div class="ms-3">
                  <h6 class="mb-0">{{ article?.author }}</h6>
                  <small class="text-muted">{{ article?.created_at }}</small>
                </div>
              </div>
            </div>
          </div>
          <div class="card-body">
            <h4 class="card-title">{{ article?.title }}</h4>
            <p class="card-text">{{ article?.content }}</p>
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
              <div class="d-flex justify-content-between">
                <div>
                  <h6 class="mb-1">{{ comment.author }}</h6>
                  <p class="mb-1">{{ comment.content }}</p>
                  <small class="text-muted">{{ comment.created_at }}</small>
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
      console.log(res)
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

onMounted(() => {
  getArticleDetail(articleId)
})

</script>

<style scoped>
.card {
  border: none;
  border-radius: 10px;
}

.card-header {
  border-bottom: 1px solid rgba(0,0,0,.125);
}

.btn-primary {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}

.form-control:focus {
  box-shadow: none;
  border-color: #ced4da;
}
</style>