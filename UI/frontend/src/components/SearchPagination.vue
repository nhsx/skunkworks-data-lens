<template>
  <nhs-main>
      <nhs-row>
        <sliding-pagination
          v-if="this.results.pages > 1"
          :current="Number(this.$route.query.page)"
          :total="this.results.pages"
          :aria-hidden="false"
          @page-change="paginationClickCallback"/>
        <div>
          <p>Page {{Number(this.$route.query.page)}} of {{this.results.pages}}</p>
        </div>
      </nhs-row>
  </nhs-main>
</template>


<script>

  import {
    NhsMain,
    NhsRow,
  } from 'nhsuk-frontend-vue';

import SlidingPagination from 'vue-sliding-pagination';

  export default {
    name: "SearchPagination",
    components: {
      NhsRow,
      NhsMain,
      SlidingPagination
    },
    data() {
      return {
        currentPage: Number(this.$route.query.page),
        totalPages: this.results.pages,
      }
    },
    computed: {
      previousPage() {
        return Number(this.$route.query.page) - 1;
      },
      nextPage() {
        return Number(this.$route.query.page) + 1;
      },
      getHrefPath(){
        return "/search/simple";
      },
      getSearchTerm(){
        let searchTerm = this.$route.query.query;
        searchTerm = encodeURI(searchTerm);
        searchTerm = searchTerm.replaceAll('&', '%26');
        return searchTerm;
      },
      getStaticItems(){
        return [
          {
            label: '<< First',
            value: 1,
            classes: 'left'
          },
          {
            label: '< Prev',
            value: this.currentPage - 1,
            classes: 'left'
          },
          {
            label: 'Next >',
            value: this.currentPage + 1,
            classes: 'right'
          },
          {
            label: 'Last >>',
            value: this.results.pages,
            classes: 'right'
          }
        ];
      },
      getItems(){
        const numberOfOptions = 5;
        const extraOptions = 2;

        var itemsArray = [];

        if(this.currentPage <= (numberOfOptions - extraOptions)){
          for(var x = 1; x < numberOfOptions + 1; x++){
            itemsArray.push({
              label: x,
              value: x
            });
          }

          itemsArray.push({
            label: '...',
            value: null
          });
        }else if(this.currentPage >= (this.totalPages - extraOptions)){
          itemsArray.push({
            label: '...',
            value: null
          });

          for(var y = numberOfOptions - 1; y >= 0 ; y--){
            itemsArray.push({
              label: this.totalPages - y,
              value: this.totalPages - y
            });
          }
        }else{
          itemsArray.push({
            label: '...',
            value: null
          });

          for(var z = 0 - extraOptions; z < (numberOfOptions - extraOptions) ; z++){
            itemsArray.push({
              label: this.currentPage + z,
              value: this.currentPage + z
            });
          }

          itemsArray.push({
            label: '...',
            value: null
          });
        }

        return itemsArray;
      }
    },
    methods: {
      paginationClickCallback(pageNum){
        if(pageNum){
          this.$router.push(`${this.getHrefPath}?query=${this.getSearchTerm}&page=${pageNum}`);
        }
      }
    },
    props:{
      results: Object
    }
  }
</script>

<style lang="postcss">

  .c-sliding-pagination {
    width: 100%;
  }

  .c-sliding-pagination__list {
    display: flex;
    justify-content: space-between;
    list-style: none;
  }

  .c-sliding-pagination__page {
    color: #1d70b8;
    font-size: 19px;
  }

  .c-sliding-pagination__list-element--disabled .c-sliding-pagination__page{
    color: grey;
  }

  .c-sliding-pagination__list-element--active .c-sliding-pagination__page{
    color: #000;
  }
</style>