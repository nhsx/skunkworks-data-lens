<template>
    <mdb-container>
      <nhs-row>
        <nhs-col :span="100">
          <nhs-card>
            <template
              #heading>
              <div
                class="vote-buttons-container">       
                <button
                    v-tooltip="'Vote that this result was relevant'"
                    id="thumbs-up"
                    aria-controls="thumbs-up"
                    aria-label="Thumbs Up"
                    @click="resultVote('yes')"
                    :class="feedbackRelevancy === true ? 'thumbs up chosen' : 'thumbs up'"
                    :disabled="feedbackGiven">
                    <i class="fas fa-thumbs-up"></i>
                </button>
                <button
                    v-tooltip="'Vote that this result was not relevant'"
                    id="thumbs-down"
                    aria-controls="thumbs-down"
                    aria-label="Thumbs Down"
                    @click="resultVote('no')"
                    :class="feedbackRelevancy === false ? 'thumbs down chosen' : 'thumbs down'"
                    :disabled="feedbackGiven">
                  <i class="fas fa-thumbs-up"></i>
                </button>           
              </div>
              <div
                v-if="highlight.title"
                @click="logDetails"
                class="nhsuk-heading-s result-title">
                <router-link
                  v-bind:to="`/detailed-view/${id}`"
                  v-html="highlight.title[0]"/>
              </div>
              <div
                v-else-if="content.title"
                @click="logDetails"
                class="nhsuk-heading-s result-title">
                <router-link
                  v-bind:to="`/detailed-view/${id}`"
                  v-html="content.title"/>
              </div>
            </template>
            <template class ="nhsuk-body-s" #description>
              <p
                class="nhsuk-body-s"
                v-if="highlight.notes"
                v-html="truncateText(highlight.notes)"/>
              <p
              class="nhsuk-body-s"
                v-else-if="highlight['description']"
                v-html="truncateText(highlight['description'])"/>
              <p
              class="nhsuk-body-s"
                v-else-if="highlight['resources.description']"
                v-html="truncateText(highlight['resources.description'])"/>
              <p
              class="nhsuk-body-s"
                v-else-if="highlight['introduction']"
                v-html="truncateText(highlight['introduction'])"/>
              <p
              class="nhsuk-body-s"
                v-else-if="highlight['denomsource']"
                v-html="truncateText(highlight['denomsource'])"/>
              <p
              class="nhsuk-body-s"
                v-else-if="highlight['table_description']"
                v-html="truncateText(highlight['table_description'])"/>
              <p
              class="nhsuk-body-s"
                v-else-if="content.description"
                v-html="truncateText(content.description)"/>
              <p
              class="nhsuk-body-s"
                v-else-if="content.definition"
                v-html="truncateText(content.definition)"/>
              <p
              class="nhsuk-body-s"
                v-else-if="content.introduction"
                v-html="truncateText(content.introduction)"/>
              <p
                v-if="content.coverage_start_date && content.coverage_end_date"
                class="coverage-dates nhsuk-body-s">
                  Coverage Start Date: {{prettifyDate(content.coverage_start_date)}}<br/>
                  Coverage End Date: {{prettifyDate(content.coverage_end_date)}}
              </p>
              <div
                class="source-tag"
                v-if="content.source">
                <nhs-tag
                  class="left">
                  {{content.source}}
                </nhs-tag>
                <nhs-tag
                  v-if="content.type"
                  class="right nhsuk-tag--white">
                  {{content.type}}
                </nhs-tag>
              </div>
            </template>
          </nhs-card>
        </nhs-col>
      </nhs-row>
    </mdb-container>
</template>

<script>

import {
    mdbContainer
} from 'mdbvue';

import SearchService from '../../service/SearchService';
import tooltip from 'vue-simple-tooltip';

import {
  NhsCard,
  NhsRow,
  NhsCol,
  NhsTag
} from 'nhsuk-frontend-vue';

export default {
    props: {
      data: Object,
      index: Number,
    },
    directives: {
      tooltip
    },
    components: {
      mdbContainer,
      NhsCard,
      NhsRow,
      NhsCol,
      NhsTag
    },
    data(){
      return {
        feedbackRelevancy: '',
        feedbackGiven: false,
      }
    },
    methods: {
      openQuickLook(id){
        this.$emit("openQuickLook", id)
      },
      resultVote(value){
        if(value == 'yes'){
            this.feedbackRelevancy = true;
        }else{
            this.feedbackRelevancy = false;
        }
        this.feedbackGiven = true;

        this.$cookies.set(this.data._id, this.feedbackRelevancy);
        var index = this.index;
        var id = this.data_id;
        var sourceIndex = this.data._index;
        var relevanceVote = this.feedbackRelevancy;
        this.$emit('onFeedbackClick', {index, id, sourceIndex, relevanceVote});
      },
      async addClickLog(){
        if(!this.clickLogged){
          const object = {};
          object["feedbackResponse"] = {
            "relevant": this.feedbackRelevancy
          };
          await SearchService.addClickLog(object);
          this.clickLogged = true;
        }
      },
      prettifyDate(date){
        if(!date){
          return "No date found"
        }
        if (new Date(date).toLocaleDateString()!== "Invalid Date"){
          return new Date(date).toLocaleDateString();
        }
        else {
          return date;
        }
      },
      accessData(field, returnAll){
        if(this.highlight && this.highlight[field]){
          return returnAll ? this.highlight[field].join('...') : this.highlight[field][0]
        } else if (this.content[field]) {
          return this.content[field]
        } else {
          ""
        }
      },
      truncateText(textArray){
        const textCharLength = 400;
        var text;

        if(Array.isArray(textArray)){
          text = textArray.join(' ');
        }else{
          text = textArray;
        }

        if(text.length <= textCharLength){
          return text;
        }

        var removedPTagText = text.replace("<p>", "").replace("</p>", "");
        var finalText = removedPTagText.slice(0, textCharLength) + "...";
        var startTag = finalText.search("<a");
        if(startTag > -1){
          finalText = removedPTagText.slice(0, startTag) + "...";
        }

        return finalText;
      },
      logDetails(){
        var data = this.data;
        var index = this.index;
        this.$emit('onClick', {data, index});
      },
    },
    computed: {
      content(){
        return this.data._source;
      },
      id(){
        return this.data._id;
      },
      highlight(){
        if(this.data.highlight){
          return this.data.highlight;
        }else{
          return "";
        }
      },
    },
    mounted(){
      if(this.$cookies.get(this.data._id) == "true"){
        this.feedbackRelevancy = true;
        this.feedbackGiven = true;
      }else if(this.$cookies.get(this.data._id) == "false"){
        this.feedbackRelevancy = false;
        this.feedbackGiven = true;
      }else{
        this.feedbackGiven = false;
      }      
    }
}
</script>
<style>

  .highlighted-text{
    background-color: lightgoldenrodyellow;
  }

  .result-title{
    width:calc(100% - 50px)
  }

  .coverage-dates {
    color: #4c6272;
  }

  .vote-buttons-container{
    background: white;
    position: absolute;
    top: 24px;
    right: 24px;
  }

  @media (min-width: 40.0625em) {
    .vote-buttons-container{
      top: 32px;
      right: 32px;
    }
  }

  .thumbs {
    background: transparent;
    border: transparent;
    color: #003087;
    opacity: 0.5 !important;
  }

  .thumbs.down {
    transform: rotate(180deg);
  }

  .thumbs:hover, .thumbs.chosen {
    opacity: 1 !important;
  }

  @media (min-width:40.0625em){
    .nhsuk-card {
      margin-bottom: 0 !important;
    }
  }

  .nhsuk-card {
    margin-bottom: 0 !important;
  }
  
  .source-tag {
    position: relative;
    height: 26px;
  }
  .source-tag .left {
    position: absolute;
    left: 0;
  }
  .source-tag .right {
    position: absolute;
    right: 0;
  }

  .description-font{
    font-size: 17px;
  }

  .result-title{
    overflow-x: hidden;
    font:5px;
  } 
</style>