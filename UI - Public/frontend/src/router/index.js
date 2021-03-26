import Vue from 'vue'
import VueRouter from 'vue-router'

import SimpleSearchView from '../views/search/SimpleSearchView.vue';
import DetailedResultItemView from '../views/DetailedResultItemView.vue';

import LogoutView from '../views/LogoutView.vue';

Vue.use(VueRouter)

  const routes = [
    {path: "/", redirect: '/search/simple'},
    {path: "/search/simple", component: SimpleSearchView},
    {path: "/logout", component: LogoutView},
    {path: "/detailed-view/:id", component: DetailedResultItemView}
  ]

const router = new VueRouter({
  mode: "history",
  routes
})

export default router