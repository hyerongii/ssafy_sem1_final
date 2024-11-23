
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import VueApexCharts from 'vue3-apexcharts'
import 'bootstrap-icons/font/bootstrap-icons.css'

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(VueApexCharts)
app.use(pinia)
app.use(router)

app.mount('#app')
