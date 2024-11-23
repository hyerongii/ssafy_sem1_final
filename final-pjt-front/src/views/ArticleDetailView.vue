<template>
  <div class="container mt-5">
    <h1>게시글 상세 페이지</h1>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';
import { onMounted } from 'vue';
import { useRoute } from 'vue-router'

const authstore = useAuthStore()
const route = useRoute()
const articleId = route.params.article_id

// 게시글 상세 조회
const getArticleDetail = function(articleId) {
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
      console.log(res)
      console.log('댓글 조회 완료')
    })
    .catch((err) => {
      console.log(err)
    })
}

// 댓글 작성
const submitComment = function(articleId, comment) {
  axios({
    method: 'post',
    url: `${authstore.API_URL}/api/v1/stock/article/detail/`,
    headers: {
      Authorization: `Bearer ${authstore.token}`,
    },
    data: {
      article_id: articleId,
      content: comment
    }
  })
    .then((res) => {
      console.log(res)
      console.log('댓글 작성 완료')
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

</style>