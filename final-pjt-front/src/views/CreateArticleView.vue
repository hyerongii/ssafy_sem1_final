<template>
  <div class="container mt-5">
    <h1>게시글 작성</h1>
    <form @submit.prevent="createArticle">
      <div>
        <label for="title">제목 : </label>
        <input type="text" id="title" v-model.trim="title">
      </div>
      <div>
        <label for="content">내용 : </label>
        <textarea id="content" v-model.trim="content"></textarea>
      </div>
      <input type="submit">
    </form>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const authstore = useAuthStore()
const router = useRouter()
const title = ref(null)
const content = ref(null)

const createArticle = function () {
  axios({
    method: 'post',
    url: `${authstore.API_URL}/api/v1/stock/article/create/`,
    headers: {
      Authorization: `Bearer ${store.token}`,
    },
    data: {
      title: title.value,
      content: content.value
    }
  })
    .then((res) => {
      console.log('게시글 작성 성공')
    })
}

</script>

<style scoped>

</style>