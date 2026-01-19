import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// Vant UI
import Vant from 'vant'
import 'vant/lib/index.css'

// Touch emulator for desktop
import '@vant/touch-emulator'

// Global styles
import '@/styles/main.less'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(Vant)

app.mount('#app')