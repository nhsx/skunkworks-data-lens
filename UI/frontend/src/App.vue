<template>
  <div id="app">
    <Navbar />

    <router-view></router-view>

    <nhs-footer/>

    <cookie-law></cookie-law>
    
  </div>
</template>

<script>
import store from './store';
import { mapState } from 'vuex';
import Navbar from './components/Navbar.vue'
import FilterService from './service/FilterService.js'
import SearchService from './service/SearchService.js'
import {changeSearchModalState} from "./store/mutations/savedSearchTypes";
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
      filterLabels: FilterService.filterLabels,
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
    setModal(modalState) {
      store.dispatch({
          type: changeSearchModalState,
          state: modalState
      })
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