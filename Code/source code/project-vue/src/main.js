import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Vant from 'vant'
import axios from 'axios'
import 'vant/lib/index.css'
// 导入 rem 的 js, 动态的设置了, 不同屏幕的html根元素的 font-size
// import 'lib-flexible'
Vue.prototype.$axios = axios
axios.baseURL = ''
Vue.use(Vant)
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
