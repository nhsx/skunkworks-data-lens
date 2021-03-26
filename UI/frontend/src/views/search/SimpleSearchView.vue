<template>
    <div
        class="loading-background"
        v-if="isLoading">
        <loading
            :active.sync="isLoading"
            :is-full-page="true"
            >
        </loading>
    </div>
    <div
        v-else>

        <language-pop-up
            v-if="this.showLanguagePopUp"
            :languageCode="this.popUpLanguageCode"
            @closeLanguagePopUp="this.closeLanguagePopUp"/>

        <div
            class="simple-search-container">
            <nhs-row>
                <nhs-col
                    v-if="this.lastSearchTerm !== ''"
                    :span="25">
                    <p/>
                </nhs-col>
                <nhs-col
                    v-if="this.lastSearchTerm !== ''"
                    :span="66">
                    <search-header
                        class="search-header-sticky"
                        @initiate-basic-search="this.searchTermChange"
                        @update-multi-lang="this.updateMultiLang"
                        @show-popup="showLanguagePopUp = true"
                        v-bind:searchTerm="lastSearchTerm"
                        v-bind:multiEnabled="multiLangEnabled" />
                    <div
                        class="filters">
                        <nhs-heading
                            size="m"
                            class="header">
                            <a
                                href="javascript:;"
                                v-on:click="toggleFilters">
                                Filters <i class="fa fa-caret-down"/>
                            </a>
                        </nhs-heading>
                        <refine-results
                            :class="this.showFilters ? 'show' : 'hide'"
                            v-if="this.lastSearchTerm !== ''"
                            v-bind:results="results"
                            v-bind:activeFilters="this.activeFilters"
                            v-on:search-params-changed="updateResults" />
                    </div>
                    <div
                        v-if="this.lastSearchTerm !== ''">
                        <results-view
                            v-bind:results="results"
                            v-on:modal-toggle="setModal"
                            @submitRelevanceVote="submitRelevanceVote"
                            @onItemClick="onItemClick" />
                        <search-pagination
                            v-if="this.results.pages > 0"
                            v-bind:results="results"
                            v-on:search-params-changed="updateResults" />
                    </div>
                </nhs-col>
                
                <nhs-col
                    v-else
                    class="home-search"
                    :span="50">
                    <search-header
                        class="home-header-sticky"
                        @initiate-basic-search="this.searchTermChange"
                        @update-multi-lang="this.updateMultiLang"
                        @show-popup="showLanguagePopUp = true"
                        v-bind:searchTerm="lastSearchTerm"
                        v-bind:multiEnabled="multiLangEnabled" />
                    <div
                        v-if="this.lastSearchTerm !== ''">
                        <results-view
                            v-bind:results="results"
                            v-on:modal-toggle="setModal"
                            @submitRelevanceVote="submitRelevanceVote"
                            @onItemClick="onItemClick" />
                        <search-pagination
                            v-if="this.results.pages > 0"
                            v-bind:results="results"
                            v-on:search-params-changed="updateResults" />                    
                    </div>
                    <div
                        v-else
                        class="pre-search-placeholder">
                        <nhs-body>
                            <nhs-row style="padding-bottom: 20px">
                                <nhs-col>
                                    Search for a keyword, phrase or anything in the bar above to get started.
                                </nhs-col>
                            </nhs-row>
                            <nhs-row style="padding-bottom: 20px">
                                <nhs-col>
                                    <b>About Data Lens</b>

                                    <br>
                                    
                                    Data Lens is a proof-of-concept project for the NHS AI Lab Skunkworks team which brings together information about multiple databases, providing a fast-access search in multiple languages.
                                    
                                    <br>
                                    <br>

                                    <ul>
                                    <b>Data Lens Aims to:</b>
                                    <li>Present information about data from across the sector with one search</li>
                                    <li>Give preview information and direct users to an original location (avoiding the need for another database)</li>
                                    <li>Provide multilingual support and a user focused approach</li>
                                    <li>Reduce workload and improve the quality of information available</li>
                                    <li>Build up a picture of what data is collected and how it flows through the health and social care system</li>
                                    </ul>

                                    <br>

                                    <b>Please note that the current system is a proof of concept and therefore there may be functionality missing, or errors may occasionally occur.</b> 

                                    <br>
                                    <br>

                                    <b>Data Sources</b>
                                    <br>
                                    Data Lens currently indexes metadata data from the following sources:
                                    <br>
                                    NHS England Data Catalogue
                                    <br>
                                    NHS England NCDR
                                    <br>
                                    MDX Cube
                                    <br>
                                    NHS Digital - Datasets, Publications, Series, Collections
                                    <br>
                                    Office for National Statistics - Health & Social Care
                                    <br>
                                    Health Data Research Innovation Gateway
                                    <br>
                                    Public Health England Fingertips
                                    <br>
                                </nhs-col>
                            </nhs-row>
                        </nhs-body>
                    </div>
                </nhs-col>
            </nhs-row>
        </div>
       
    </div>
</template>

<script>

    import {
        NhsCol,
        NhsRow,
        NhsBody,  
        NhsHeading,
    } from 'nhsuk-frontend-vue';

    import Loading from 'vue-loading-overlay';
    import SearchHeader from '../../components/search/headers/SearchHeader.vue';
    import RefineResults from '../../components/RefineResults.vue';
    import ResultsView from '../ResultsView.vue';
    import store from '../../store';
    import { mapState } from 'vuex';
    import {changeSearchModalState} from "../../store/mutations/savedSearchTypes";
    import {setSearchResults} from "../../store/mutations/searchTypes";
    import FilterService from '../../service/FilterService.js'
    import SearchService from '../../service/SearchService.js'
    import SearchPagination from '../../components/SearchPagination.vue';
    import LanguagePopUp from '../../components/LanguagePopUp.vue';

    export default {
        name: "SimpleSearchView",
        components: {
            SearchHeader,
            ResultsView,
            RefineResults,
            NhsRow,
            NhsCol,
            Loading,
            SearchPagination,
            NhsHeading,
            NhsBody,
            LanguagePopUp,
        },
        data(){
            return {
                checkboxVal: false,
                lastSearchTerm: "",
                history: false,
                pageNumber: 1,
                resultsData: SearchService.resultsData,
                filterLabels: FilterService.filterLabels,
                isLoading: false,
                multiLangEnabled: false,
                showFilters: false,
                showLanguagePopUp: false,
                popUpLanguageCode: "en",
            }
        },
        methods: {
            checkLanguagePopUp(){
                if(this.$cookies.get("remove_langauge_prompt") == "true" || !this.multiLangEnabled){
                    this.showLanguagePopUp = false;
                }else{
                    this.showLanguagePopUp = true;
                }
            },
            closeLanguagePopUp(){
                this.showLanguagePopUp = false;
            },
            toggleFilters(){
                this.showFilters = !this.showFilters;
            },
            async updateResults(){
                store.dispatch({
                    type: setSearchResults,
                    results: await SearchService.fetchData(
                        this.lastSearchTerm,
                        this.pageNumber,
                        this.activeTypeFilter,
                        this.activeFilters,
                        this.$cookies.get('user_id')
                    ),
                    page: this.pageNumber,
                    activeTypeFilter: this.activeTypeFilter,
                });
            },
            async getResults(searchTerm, pageNumber){
                const results = await SearchService.fetchData(
                    searchTerm,
                    pageNumber,
                    undefined,
                    this.activeFilters,
                    this.$cookies.get('user_id'),
                    this.multiLangEnabled
                );

                if(results.hits){
                    if (!pageNumber) { 
                        pageNumber = 1;
                    }

                    if (this.multiLangEnabled){ 
                        this.popUpLanguageCode = results.sourceLanguageCode;
                        this.showLanguagePopUp = true;
                    }else{
                        this.popUpLanguageCode = "en";
                    }

                    // this.updateUrl(this.getUrl(searchTerm, pageNumber));

                    store.dispatch({
                        type: setSearchResults,
                        results: results
                    });

                    this.lastSearchTerm = searchTerm;

                    if(this.$cookies.get('search_term') != searchTerm){
                        this.$cookies.set('search_time', new Date());
                        this.$cookies.set('search_term', searchTerm);
                        this.$cookies.set('details_click_through_order', 0);
                    }
                }else{
                    this.isLoading = false;
                    alert("No results were returned");
                    window.open(`/search/simple`, '_self');
                }
            },
            searchTermChange(searchTerm){
                if(searchTerm !== '' && searchTerm.trim() !== ''){
                    searchTerm = encodeURI(searchTerm);
                    searchTerm = searchTerm.replaceAll('&', '%26');
                    this.updateUrl(this.getUrl(searchTerm, 1));
                }
            },
            updateUrl(url){
                if(encodeURI(url) !== this.$route.fullPath){
                    this.$router.push(url);
                }
            },
            getUrl(searchTerm, pageNumber){
                let url = searchTerm && searchTerm !== "" ? `${this.$route.path}?query=${searchTerm}` : this.$route.path;
                if (this.multiLangEnabled){
                    url += '&multilang=true';
                }
                return url + `&page=${pageNumber}`;
            },
            setModal(modalState) {
                store.dispatch({
                    type: changeSearchModalState,
                    state: modalState
                })
            },
            filterAttributes(key, val){
                SearchService.filterAttributes(key,val);
            },
            navigateSearch(type){
                this.page = type;
                this.history=false;
            },
            checkQueryTerms(){
                this.searchTerm = this?.$route?.query?.query ? this.$route.query.query : "";
                this.multiLangEnabled = this?.$route?.query?.multilang ? true : false;
                this.pageNumber = this?.$route?.query?.page ? this.$route.query.page : 1;
            },
            updateMultiLang(multiLang){
                this.multiLangEnabled = multiLang
            },
            async onItemClick(itemContent, index){
                window.scroll({
                    top: 0, 
                    left: 0
                });

                var clickThroughOrder = this.$cookies.get('details_click_through_order');
                this.$cookies.set('details_click_through_order', clickThroughOrder++);
                this.$cookies.set('result_rank', ((this.pageNumber - 1) * 20) + index);
                this.$cookies.set('filters', store.state.search.filters);
            },
            toggleShowFeedback(){
                this.showFeedback = !this.showFeedback;
            },
            async submitRelevanceVote(values){
                var index = values.index;
                var id = values.id;
                var sourceIndex = values.sourceIndex;
                var relevanceVote = values.relevanceVote;
                var resultRank = ((this.pageNumber - 1) * 20) + index;
                const object = {};
                object["user_id"] = this.$cookies.get('user_id');
                object["search_term"] = this.$cookies.get('search_term');
                object["search_time"] = this.$cookies.get('search_time');
                object["document_id"] = id;
                object["result_rank"] = resultRank;
                object["index_name"] = sourceIndex;
                object["filters"] = store.state.search.filters;
                object["detail_click_time"] = new Date();
                object["feedbackResponse"] = {
                    "relevant": relevanceVote
                };

                await SearchService.addClickLog(object);
            },
        },
        computed: mapState({
            modalOpen: state => state.savedSearches.modalOpen,
            savedSearches: state => state.savedSearches.data,
            results: state => state.search.searchResults,
            activeSearchPage: state => state.search.activeSearchPage,
            activeTypeFilter: state => state.search.activeTypeFilter,
            activeFilters: state => state.search.filters,
        }),
        beforeMount() {
            this.checkQueryTerms();
            //this.$cookies.set("remove_langauge_prompt", false);
            this.checkLanguagePopUp();
        },
        watch:{
            async $route (to, from){
                if (to.redirectedFrom == '/'){
                    this.lastSearchTerm = ''
                }else if((to.query.query !== from.query.query) || (to.query.page !== from.query.page)){
                    window.scroll({
                        top: 0, 
                        left: 0
                    });
                    this.isLoading = true;
                    this.checkQueryTerms();
                    await this.getResults(this.searchTerm, this.pageNumber);
                    this.isLoading = false;
                }
            }
        },
        async mounted(){
            if(this.searchTerm){
                this.isLoading = true;
                await this.getResults(this.searchTerm, this.pageNumber);
                this.isLoading = false;
            }
        }
    }
</script>

<style lang="postcss">

    .simple-search-container{
        position: relative;
    }

  .search-header-sticky {
    position: sticky;
    top: -35px;
    background-color: #ffffff;
    z-index: 9999;
    border:#003087;
    padding-left: 31px;
    padding-right: 31px;

  }
  

  .search-header-sticky .nhsuk-main-wrapper {
    background-color: #ffffff;
    padding: 0px;
    border:#003087 solid;
  }

  .nhsuk-width-container main#maincontent.nhsuk-main-wrapper {
    padding-top: 0px;
  }

  .pre-search-placeholder {
      left:200px;
      background-color: #ffffff;
      padding-left: 5px;
        padding-right: 5px;
  }

    .loading-background {
        position: fixed;
        width: 100vw;
        height: 100vh;
        top: 0;
        left: 0;
        overflow: hidden;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 99;
    }

    .loading-background .vld-overlay {
        background-color: transparent;
    }

  .is-full-page {
      background-color: #ffffff;
      width: 100%;
      height: 100%;
  }

    .vld-background {
        background-color: #000000;
        opacity: 0.5;
        width: 100%;
        height: 100%;
    }

    .search-results-container{
        margin-bottom: 50px;
    }
  
  .vld-icon {
      text-align: center;
            position: absolute;
      top: calc(50% - 35px);
      left: calc(50% - 32px);
      color: #003087;
  }

    @media only screen and (min-width:1200px){
        .home-search{
            margin-left: 350px;
        }
    }

    @media only screen and (max-width:769px){
        .nhsuk-main-wrapper {
            margin-top: 10px;
        }

        .mobilefilters{
            top:10px;
        }

        .home-search{
            padding-left: -12px;
            padding-right: -12px;
        }

        .search-header-sticky {
            position:sticky;
            top: -35px;
            background-color: #ffffff;
            border:#003087;
        }

        .filters{
            padding: 0 31px;
        }

        .filters .show{
            display: block;
        }

        .filters .hide{
            display: none;
        }
    }

    @media only screen and (min-width:769px){
        .nhsuk-main-wrapper {
            margin-top: 10px;
        }

        .mobilefilters{
            top:10px;
            display:none; 
        }

        .home-search{
            margin-left: 400px;
        }

        .filters{
            position: absolute;
            left: 0;
            top: 0;
            padding-top: 37px;
            width: calc(25vw - 20px);
            padding: 10px;
            padding-top: 47px;
            max-height: 100%;
            overflow-y: auto;
            overflow-x: hidden;
        }

        .filters::-webkit-scrollbar {
            display: none;
        }

        /* Hide scrollbar for IE, Edge and Firefox */
        .filters {
            -ms-overflow-style: none;  /* IE and Edge */
            scrollbar-width: none;  /* Firefox */
        }

        .filters .header {
            display: none;
        }
    }


</style>