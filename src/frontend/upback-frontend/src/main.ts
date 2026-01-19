import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import {createPinia} from "pinia";

import '@/assets/styles/global.scss'
import '@/assets/styles/colors.scss'
import '@/assets/styles/fonts.scss'
import '@/assets/styles/animations.scss'

const app = createApp(App)
const pinia = createPinia()

app.use(router)
app.use(pinia)

app.mount('#app')