import Vue from 'vue'
import VueRouter from 'vue-router';
import VCalendar from 'v-calendar';
import VueCookies from 'vue-cookies';

import App from './App.vue'
import VMdDateRangePicker from "v-md-date-range-picker";
import router from './router'
import store from './store'
// import { LMap, LTileLayer, LMarker } from 'vue2-leaflet';
import 'leaflet/dist/leaflet.css';
import { v4 as uuidv4 } from 'uuid';

import 'bootstrap-css-only/css/bootstrap.min.css'
import 'mdbvue/lib/css/mdb.min.css'
import '@fortawesome/fontawesome-free/css/all.min.css'

// Vue.component('l-map', LMap);
// Vue.component('l-tile-layer', LTileLayer);
// Vue.component('l-marker', LMarker);

Vue.config.productionTip = false
Vue.use(VMdDateRangePicker);
Vue.use(VueRouter);
Vue.use(VueCookies);

Vue.config.ignoredElements = ['canvas-datagrid'];

// Use v-calendar & v-date-picker components
Vue.use(VCalendar, {});

if(!Vue.$cookies.get("user_id")){
  Vue.$cookies.set("user_id", uuidv4());
}

new Vue({
  el: '#app',

  data(){
    return {
    }
  },

  router,
  store,

  render: function(createElement) {
    return createElement(App);
  }
});

