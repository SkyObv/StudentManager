import Vue from 'vue'
import App from './App.vue'
import settings from "@/settings";                                   // 导入配置文件
import ElementUI from 'element-ui';                                  // 导入element-ui组件
import 'element-ui/lib/theme-chalk/index.css';                       // 导入element-ui组件样式表
import router from "@/routers/index";                                // 导入路由
import axios from 'axios';                                           // 导入前端请求模块

Vue.config.productionTip = false
Vue.prototype.$settings = settings;
Vue.prototype.$axios = axios;
axios.defaults.withCredentials = true;
Vue.use(ElementUI);
document.title = '宿舍管理系统';
new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
