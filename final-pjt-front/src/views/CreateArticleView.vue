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
import axios from 'axios'
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
const route = useRoute()
const authstore = useAuthStore()
const router = useRouter()
const title = ref(null)
const content = ref(null)
const stockcode = route.params.stock_id

const createArticle = function () {
  axios({
    method: 'post',
    url: `${authstore.API_URL}/api/v1/stock/article/create/`,
    headers: {
      Authorization: `Bearer ${authstore.token}`,
    },
    data: {
      stock_code: stockcode, 
      title: title.value,
      content: content.value
    }
  })
    .then((res) => {
      console.log('게시글 작성 성공')
      router.push({name:'CommunityView', params:{stock_id : stockcode}})
    })
    .catch((err) => {
      console.log(err)
    })
}

</script>

<style scoped>

</style>