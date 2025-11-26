import { createRouter, createWebHistory } from 'vue-router'
import homeComp from "@/components/home.vue";

const routes = [
  {
    path: '/',
    name: 'Home',
    component: homeComp
  },
]

// 创建路由实例
const router = createRouter({
  // 使用 history 模式
  history: createWebHistory(),
  routes                             // `routes: routes` 的缩写
})

export default router