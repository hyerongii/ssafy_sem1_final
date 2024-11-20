import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from './auth'

export const useStockStore = defineStore('stock', () => {
  const store = useAuthStore()
  const todaydate = ref(null) // YYYYMMDD
  const stocklist = ref([])
  const chartdata = ref([])

  const getStockChart = function (themename) {
    axios({
      //백에서 받아오기
      method: 'post',
      url: `${store.API_URL}/api/v1/stock/indus_chart/`,
      headers: {
        Authorization: `Bearer ${store.token}`,
      },
      data: {
        theme_name : themename,
        end_date : todaydate.value
      },
    })
      .then((res) => {
        console.log(res.data)
        stocklist.value = res.data.theme_info.stocks
        chartdata.value = res.data.chartdata
      })
      .catch((err) => {
        console.log(err)
      })
  }

  return {getStockChart, todaydate, stocklist, chartdata}
}
// ,{persist: true}
)
