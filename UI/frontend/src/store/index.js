import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    search: {
      searchResults: undefined,
      activeTypeFilter: undefined,
      activeSearchPage: 1,
      filters: {},
    },
    advancedSearch: {
      searchResults: undefined,
    },
    bulkSearch: {
      searchResults: undefined,
    },
    savedSearches: {
      modalOpen: false,
      data: [
        {term: "07930112343", notifications: true, email: false},
        {term: "@daveedjordooon", notifications: false, email: true},
        {term: "07930112343 AND football", notifications: true, email: true},
        {term: "07930132123", notifications: false, email: false},
        {term: "honeywell", notifications: false, email: true},
        {term: "dj1@example.com, djaa@example2.com [+5]", notifications: false, email: false}
      ]
    },
    config: undefined
  },
  mutations: {
    setSearchResults(state, payload) {
      state.search.activeSearchPage = payload.page || 1;
      state.search.activeTypeFilter = payload.activeTypeFilter || undefined;
      return state.search.searchResults = payload.results;
    },
    setSearchFilters(state, payload){
      return state.search.filters = payload.filters;
    },
    setAdvancedSearchResults(state, payload) {
      return state.advancedSearch.searchResults = payload.results;
    },
    setBulkSearchResults(state, payload) {
      return state.bulkSearch.searchResults = payload.results;
    },
    setActiveTypeFilter(state, payload){
      state.search.activeSearchPage = 1;
      return state.search.activeTypeFilter = payload.filter;
    },
    setActiveSearchPage(state, payload){
      return state.search.activeSearchPage = payload.page;
    },
    changeSearchModalState(state, payload){
      return state.savedSearches.modalOpen = payload.state;
    },
    setConfigState(state, payload){
      return state.config = payload.state;
    }
  },
  actions: {
    setSearchResults(context, payload) {
      context.commit("setSearchResults", payload)
    },
    setSearchFilters(context, payload){
      context.commit("setSearchFilters", payload)
    },
    setAdvancedSearchResults(context, payload) {
      context.commit("setAdvancedSearchResults", payload)
    },
    setBulkSearchResults(context, payload) {
      context.commit("setBulkSearchResults", payload)
    },
    setActiveTypeFilter(context, payload) {
      context.commit("setActiveTypeFilter", payload)
    },
    setActiveSearchPage(context, payload) {
      context.commit("setActiveSearchPage", payload)
    },
    changeSearchModalState(context, payload) {
      context.commit("changeSearchModalState", payload)
    },
    setConfigState(context, payload) {
      context.commit("setConfigState", payload)
    }
  },
  modules: {
  }
})
