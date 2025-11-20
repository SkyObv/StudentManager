import Vue from "vue";
import Router from "vue-router";
import Login from "@/components/Login.vue";

// 导入可访问的组件（后续补充）
Vue.use(Router);

export default new Router({
  // 移除URL中的#号
  mode: "history",
  routes: [
      // 统一登入入口登入
    {
      path: "/",
      name: "Login",
      component:Login
    },

  ]
});