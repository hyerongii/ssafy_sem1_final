import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LogInView from '@/views/LogInView.vue'
import SignUpView from '@/views/SignUpView.vue'
import UserSelectView from '@/views/UserSelectView.vue'
import LoadingView from '@/views/LoadingView.vue'
import ThemeListView from '@/views/ThemeListView.vue'
import ThemeItemView from '@/views/ThemeItemView.vue'
import StockItemView from '@/views/StockItemView.vue'
import DayStockChart from '@/components/stocks/DayStockChart.vue'
import WeekStockChart from '@/components/stocks/WeekStockChart.vue'
import MonthStockChart from '@/components/stocks/MonthStockChart.vue'
import SixMonthStockChart from '@/components/stocks/SixMonthStockChart.vue'
import YearStockChart from '@/components/stocks/YearStockChart.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomeView',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView,
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView,
    },
    {
      path: '/userselect',
      name: 'UserSelectView',
      component: UserSelectView,
    },
    {
      path: '/loading',
      name: 'LoadingView',
      component: LoadingView,
    },
    {
      path: '/themelist',
      name: 'ThemeListView',
      component: ThemeListView,
    },
    {
      path: '/themeitem/:theme_id',
      name: 'ThemeItemView',
      component: ThemeItemView,
    },
    {
      path: '/stockitem/:stock_id',
      name: 'StockItemView',
      component: StockItemView,
      children:[
        {
          path: '',
          name: 'day',
          component: DayStockChart,
        },
        {
          path: 'week',
          name: 'week',
          component: WeekStockChart,
        },
        {
          path: 'month',
          name: 'month',
          component: MonthStockChart,
        },
        {
          path: 'sixmonth',
          name: 'sixmonth',
          component: SixMonthStockChart,
        },
        {
          path: 'year',
          name: 'year',
          component: YearStockChart,
        },
      ]
    }
  ],
})

export default router
