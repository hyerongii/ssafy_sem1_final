<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow">
          <div class="card-header bg-white">
            <h2 class="text-center mb-0">{{ isEditing ? '게시글 수정' : '게시글 작성' }}</h2>
          </div>
          <div class="card-body">
            <form @submit.prevent="submitArticle">
              <div class="mb-4">
                <label for="title" class="form-label">제목</label>
                <input 
                  type="text" 
                  id="title" 
                  class="form-control"
                  v-model.trim="title"
                  placeholder="제목을 입력하세요"
                >
              </div>
              <div class="mb-4">
                <label for="content" class="form-label">내용</label>
                <textarea 
                  id="content" 
                  class="form-control" 
                  rows="8"
                  v-model.trim="content"
                  placeholder="내용을 입력하세요"
                ></textarea>
              </div>
              <div class="d-grid">
                <button 
                  type="submit" 
                  class="btn btn-primary btn-lg"
                >
                  {{ isEditing ? '수정하기' : '작성하기' }}
                </button>
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
import { useRoute, useRouter } from 'vue-router'
const route = useRoute()
const authstore = useAuthStore()
const router = useRouter()
const title = ref(null)
const content = ref(null)
const stockcode = route.params.stock_id
const isEditing = ref(false)
const articleId = ref(null)

onMounted(() => {
  if (route.query.edit) {
    isEditing.value = true
    title.value = route.query.title
    content.value = route.query.content
    articleId.value = route.query.articleId
  }
})

const submitArticle = function () {
  const requestData = {
    article_id: articleId.value,
    stock_code: stockcode,
    title: title.value,
    content: content.value,
  }

  const config = {
    method: isEditing.value ? 'put' : 'post',
    url: isEditing.value 
      ? `${authstore.API_URL}/api/v1/stock/article/update_or_delete/`
      : `${authstore.API_URL}/api/v1/stock/article/create/`,
    headers: {
      Authorization: `Bearer ${authstore.token}`,
      'Content-Type': 'application/json'
    },
    data: requestData
  }

  axios(config)
    .then((res) => {
      console.log(isEditing.value ? '게시글 수정 성공' : '게시글 작성 성공')
      router.push({name:'CommunityView', params:{stock_id : stockcode}})
    })
    .catch((err) => {
      console.log('Error:', err.response?.data || err.message)
    })
}
</script>

<style scoped>
.card {
  border: none;
  border-radius: 15px;
}

.card-header {
  border-bottom: 1px solid #eee;
  padding: 1.5rem;
}

.card-body {
  padding: 2rem;
}

.form-control {
  border-radius: 8px;
  padding: 0.8rem;
  border: 1px solid #dee2e6;
}

.form-control:focus {
  border-color: #80bdff;
  box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
}

.btn-primary {
  padding: 0.8rem;
  border-radius: 8px;
}
</style>