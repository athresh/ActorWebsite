// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Vuex from 'vuex'
import store from './store';

Vue.use(Vuex)
//Vue.use(VueAxios, axios);
Vue.config.productionTip = false

/* eslint-disable */

new Vue({
  store,
  el: '#app',
  router,
  template: '<App/>',
  components: { App },
})

Vue.filter('currency', function (value) {
  return '$' + parseFloat(value).toFixed(2)
})
