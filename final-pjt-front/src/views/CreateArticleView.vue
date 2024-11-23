<template>
  <div class="container mt-5">
    <h1>{{ isEditing ? '게시글 수정' : '게시글 작성' }}</h1>
    <form @submit.prevent="submitArticle">
      <div>
        <label for="title">제목 : </label>
        <input type="text" id="title" v-model.trim="title">
      </div>
      <div>
        <label for="content">내용 : </label>
        <textarea id="content" v-model.trim="content"></textarea>
      </div>
      <input type="submit" :value="isEditing ? '수정하기' : '작성하기'">
    </form>
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

</style>