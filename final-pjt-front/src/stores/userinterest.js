import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from './auth'

export const useUserInterestStore = defineStore('interest', () => {
  const store = useAuthStore()
  const router = useRouter()
  
  const usermbti = ref(null)
  const userinterest = ref([])
  const userperiod = ref(null)

  const recommendthemes = ref([])

  const analyze = function () {

    axios({
      method: 'post',
      url: `${store.API_URL}/api/v1/stock/analyze/`,
      headers: {
        Authorization: `Bearer ${store.token}`,
      },
      data: {
        mbti: usermbti.value,
        interest: userinterest.value,
        period: userperiod.value,
      },
    })
      .then((res) => {
        console.log('분석 요청 전송 완료')
        
        // 응답 데이터 처리
        // 추천 테마 6개 리스트 반환

        recommendthemes.value = res.data.recommended_themes
        console.log(res.data)

        // 테마리스트페이지로 이동
        router.push({ name: 'ThemeListView'})
        // console.log(recommendthemes.value)

      })
      .catch((err) => {
        console.log(err)
      })
  }

  return {analyze, usermbti, userinterest, userperiod, recommendthemes}
}
// ,{persist: true}
)
