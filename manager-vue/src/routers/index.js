import Vue from "vue";
import Router from "vue-router";
import Login from "@/components/Login.vue";
import Admin from "@/components/Admin.vue";
import Teachers from "@/components/Teachers.vue";
import Students from "@/components/Students.vue";

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
      // 管理员登入页面
    {
      path: "/admin",
      name: "AdminComp",
      component: Admin
    },
      // 老师页面
    {
      path: "/teachers",
      name: "Teachers",
      component: Teachers
    },
      // 学生页面
    {
      path: "/students",
      name: "Students",
      component: Students
    }
  ]
});