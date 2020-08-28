import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import VueRouter from 'vue-router';

import HelloWorld from "./components/HelloWorld";
import PrivateChargingStations from "./components/PrivateChargingStations";


Vue.use(VueRouter)

Vue.config.productionTip = false

const router = new VueRouter({
  routes: [
    { path: '/', component: HelloWorld }, // Public charging stations
    { path: '/private', component: PrivateChargingStations },
  ]
})

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')
