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
      data: []
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
    changeSearchModalState(state, payload){
      return state.savedSearches.modalOpen = payload.state;
    }
  },
  actions: {
    setSearchResults(context, payload) {
      context.commit("setSearchResults", payload)
    },
    setSearchFilters(context, payload){
      context.commit("setSearchFilters", payload)
    },
    changeSearchModalState(context, payload) {
      context.commit("changeSearchModalState", payload)
    }
  },
  modules: {
  }
})
