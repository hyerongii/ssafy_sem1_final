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
  const samethemes = ref([])
  const nickname = ref('')

  const analyze = function () {
    // 먼저 로딩페이지로 이동 이후 실제 분석로직 실행
    router.push({ name: 'LoadingView'})
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
        samethemes.value = res.data.same_theme_names
        nickname.value = res.data.nickname
        console.log(res.data)
      })
      .catch((err) => {
        console.log(err)
      })
  }

  return {analyze, usermbti, userinterest, userperiod, recommendthemes, samethemes, nickname}
}
,{persist: true}
)
