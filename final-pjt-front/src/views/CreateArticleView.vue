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

.container {
  font-family: 'Godo', sans-serif;
  padding: 2rem;
}

.card {
  background: white;
  border: 1px solid rgba(139, 193, 72, 0.1);
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(139, 193, 72, 0.1);
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 6px 16px rgba(139, 193, 72, 0.15);
}

.card-header {
  background: white;
  border-bottom: 1px solid rgba(139, 193, 72, 0.1);
  padding: 1.8rem;
}

.card-header h2 {
  color: var(--primary-word);
  font-size: 1.8rem;
  font-weight: 600;
}

.card-body {
  padding: 2rem;
}

.form-label {
  color: var(--primary-word);
  font-weight: 500;
  margin-bottom: 0.8rem;
  font-size: 1.1rem;
}

.form-control {
  border-radius: 12px;
  padding: 1rem;
  border: 1px solid rgba(139, 193, 72, 0.2);
  transition: all 0.3s ease;
  font-size: 1rem;
  color: var(--primary-word);
}
.form-control:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 0.2rem rgba(139, 193, 72, 0.1);
}

.form-control::placeholder {
  color: #999;
  font-size: 0.95rem;
}

.btn-primary {
  background: var(--primary-color);
  border: none;
  padding: 1rem;
  border-radius: 12px;
  font-weight: 500;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(139, 193, 72, 0.2);
}

.btn-primary:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(139, 193, 72, 0.25);
}

.btn-primary:active {
  transform: translateY(1px);
}

textarea {
  min-height: 200px;
  resize: vertical;
}
</style>