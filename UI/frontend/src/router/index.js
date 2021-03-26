import Vue from 'vue'
import VueRouter from 'vue-router'

//import HomeView from '../views/HomeView.vue';


import SimpleSearchView from '../views/search/SimpleSearchView.vue';
//import AdvancedSearchView from '../views/search/AdvancedSearchView.vue';
// import BulkSearchView from '../views/search/BulkSearchView.vue';
// import UploadReportPortal from '../views/UploadReportPortal.vue';
// import UploadFilePortal from '../views/UploadFilePortal.vue';
import DetailedResultItemView from '../views/DetailedResultItemView.vue';

import LogoutView from '../views/LogoutView.vue';

Vue.use(VueRouter)

  const routes = [
    {path: "/", redirect: '/search/simple'},
    {path: "/search/simple", component: SimpleSearchView},
    // {path: "/search/advanced", component: AdvancedSearchView},
    // {path: "/search/bulk", component: BulkSearchView},
    // {path: "/upload/report", component: UploadReportPortal},
    // {path: "/upload/file", component: UploadFilePortal},
    {path: "/logout", component: LogoutView},
    {path: "/detailed-view/:id", component: DetailedResultItemView}
  ]

const router = new VueRouter({
  mode: "history",
  routes
})

export default router