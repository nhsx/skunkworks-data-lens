<template>
  <mdb-container v-if="resultSize" style="padding-bottom: 10px">
      <div
        class="results-found">
        <p>Found {{resultTotal}} results.</p>
      </div>
      <div
          :href="results.dictionary[0]._source.url"
          v-if="results.dictionary"
          class="definition-card">
        <nhs-card
            feature
            :heading="results.dictionary[0]._source.title"
            heading-classes="nhsuk-heading-s"
            class="defintion-card">
            <template #description>
              <p
                class="nhsuk-body-s">
                {{results.dictionary[0]._source.description}}
              </p>
              <a
                v-if="results.dictionary[0]._source.url"
                :href="results.dictionary[0]._source.url"
                target="_blank">
                View full definition at NHS Data Dictionary
              </a>
            </template>
        </nhs-card>
      </div>
      <mdb-row class="result"  v-for="(item, index) in results.hits" :key="index">
        <mdb-col col="12">
          <generic-result-item
            v-bind:data="item"
            @onClick="onClick"
            @onFeedbackClick="onFeedbackClick"
            :index="index"/>
        </mdb-col>
      </mdb-row>
  </mdb-container>
  <mdb-container v-else>
    <mdb-row class="result">
        <mdb-col col="12">
          <h1>No results found...</h1>
        </mdb-col>
    </mdb-row>
  </mdb-container>

</template>


<script>
  import {
    NhsCard,
  } from 'nhsuk-frontend-vue';

  import { mdbContainer, mdbRow, mdbCol } from 'mdbvue';
  import GenericResultItem from '../components/resultItems/GenericResultItem.vue';
  export default {
    name: "ResultsView",
    components: {
      mdbContainer,
      mdbRow,
      mdbCol,  
      GenericResultItem,
      NhsCard
    }, 
    props: {
      results: Object,
    },
    computed: {
      resultSize(){
        return this.results.hits.length
      },
      resultTotal() {
        return this.results.total;
      }
    },
    methods: {
      onClick(resultData, index){
        this.$emit('onItemClick', {resultData, index});
      },
      onFeedbackClick(values){
        var index = values.index;
        var id = values.id;
        var sourceIndex = values.sourceIndex;
        var relevanceVote = values.relevanceVote;
        this.$emit('submitRelevanceVote', {index, id, sourceIndex, relevanceVote});
      }
    }
  }

</script>

<style scoped>

  a{
    color: #3f51b5;
  }
  
  .title{
    font-weight:500;
    font-size:1.3em;
    text-align: left;
    color: #3f51b5;
  }

  .vertical {
     border-left: 1px solid #3f51b5;
     height: 10px; 
  }


  .title:hover, a:hover{
    color: darkblue;
  }

  
  .quicklook{
    text-align: right;
    font-size: 0.7em;
    color:lightslategray;
  }

  /** CSS for featured card (to me moved when separated out) */
  .label{
    margin-left: 10px;
  }

  .row-margins{
    margin-top:10px;
  }

  .result{
    margin-top: 30px;
  }

  .featured-result{
    width:90%;
    padding: 20px 20px 20px 20px;
  }

  .definition-card{
    padding: 0px 16px;
    font: 5px
  }

  .results-found {
    padding: 0 16px;
  }
</style>

