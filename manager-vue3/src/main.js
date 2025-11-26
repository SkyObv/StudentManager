import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router'                                        // 路由器

// 创建 Vue 应用实例
const app = createApp(App)
app.use(ElementPlus)
app.use(router)
app.config.globalProperties.$http = axios
axios.defaults.baseURL = 'http://127.0.0.1:8000/'                    // 后端 API 地址
app.mount('#app')
