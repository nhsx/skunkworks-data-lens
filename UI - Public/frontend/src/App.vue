<template>
  <div id="app">
    <Navbar />

    <router-view></router-view>

    <nhs-footer/>

    <cookie-law></cookie-law>
    
  </div>
</template>

<script>
import { mapState } from 'vuex';
import Navbar from './components/Navbar.vue'
import SearchService from './service/SearchService.js'
import {NhsFooter} from 'nhsuk-frontend-vue';
import CookieLaw from 'vue-cookie-law';

export default {
  name: 'App',
  components: {
    Navbar,
    NhsFooter,
    CookieLaw
  },
  data(){
    return {
      searchTerm: "",
      filterLabels: "",
      resultsData: SearchService.resultsData,
      modal: false,
      modalData: {},
      page: "simple", //change this back to simple
      searchTermsBulk: "",
      history:false,
    }
  },
  methods: {
    initiateBasicSearch(term){
      this.searchTerm=term;
    },
    initiateBulkSearch(term){
      this.searchTermsBulk=term;
    },
  },
  computed: mapState({
    modalOpen: state => state.savedSearches.modalOpen,
    savedSearches: state => state.savedSearches.data,
  }),
}

</script>

<style>
body {
  background-color: rgb(255, 255, 255) !important;
}
</style>