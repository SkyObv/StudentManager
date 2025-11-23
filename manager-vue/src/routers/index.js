import Vue from "vue";
import Router from "vue-router";
import Login from "@/components/Login.vue";
import Admin from "@/components/Admin.vue";
import Teacher from "@/components/Teachers.vue";
import Student from "@/components/Students.vue";

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
      path: "/admins/",
      name: "AdminComp",
      component: Admin
    },
      // 老师页面
    {
      path: "/teacher/",
      name: "TeacherComp",
      component: Teacher
    },
      // 学生页面
    {
      path: "/student/",
      name: "StudentComp",
      component: Student
    }
  ]
});