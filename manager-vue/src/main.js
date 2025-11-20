import Vue from 'vue'
import App from './App.vue'
import settings from "@/settings";                                   // 导入配置文件
import ElementUI from 'element-ui';                                  // 导入element-ui组件
import 'element-ui/lib/theme-chalk/index.css';                       // 导入element-ui组件样式表
import router from "@/routers/index";                                // 导入路由

Vue.config.productionTip = false
Vue.prototype.$settings = settings;
Vue.use(ElementUI);

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
