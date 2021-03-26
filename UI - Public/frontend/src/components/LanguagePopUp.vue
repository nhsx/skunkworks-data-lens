<template>
  <div
    class="pop-up-container">
    <nhs-card
      feature
      :heading="instructions.title"
      heading-classes="nhsuk-heading-m"
      class="pop-up">
      <template #description>
        <nhs-main>
          <nhs-row>
            <nhs-col>
              <nhs-select
                v-model="languageSelect"
                class="search-order"
                :label="instructions.selectLabel">
                <option
                  v-for="languageOption in languageSelectOptions"
                  :key="languageOption.value"
                  :value="languageOption.value"
                  v-html="languageOption.label">
                </option>
              </nhs-select>
            </nhs-col>
          </nhs-row>
          <nhs-row>
          </nhs-row>
          <nhs-row>
            <nhs-col>
              <ol
                v-if="userBrowser.indexOf('Chrome') > -1">
                <nhs-col>
                    <p>{{instructions.headerLine}} - <i class="chrome fab fa-chrome"></i></p>
                </nhs-col>
                <li
                  v-for="instruction in instructions.list.chrome"
                  :key="instruction">
                  {{instruction}}
                </li>
              </ol>
              <ol
                v-else-if="userBrowser.indexOf('Safari') > -1">
                <nhs-col>
                    <p>{{instructions.headerLine}} - <i class="safari fab fa-safari"></i></p>
                </nhs-col>
                <li
                  v-for="instruction in instructions.list.safari"
                  :key="instruction">
                  {{instruction}}
                </li>
              </ol>
              <p
                v-else
                v-html="instructions.list.other"/>
            </nhs-col>
          </nhs-row>
          <nhs-row>
            <nhs-col
              :span="66">
              <div
                class="nhsuk-checkboxes">
                <div
                  class="nhsuk-checkboxes__item">
                  <input
                    aria-label="checkbox input"
                    type="checkbox"
                    class="nhsuk-checkboxes__input"
                    v-model="removePrompt">
                  <label
                    class="nhsuk-checkboxes__label nhsuk-label">
                    {{instructions.checkBox}}
                  </label>
                </div>
              </div>
            </nhs-col>
            <nhs-col
              :span="33">
              <nhs-button
                class="confirm-button"
                @click="confirmHandler">
                {{instructions.confirmButton}}
              </nhs-button>
            </nhs-col>
          </nhs-row>
        </nhs-main>
      </template>
    </nhs-card>
  </div>
</template>

<script>

import {
  NhsCard,
  NhsButton,
  NhsMain,
  NhsRow,
  NhsCol,
  NhsSelect
} from 'nhsuk-frontend-vue';

import {
  languageInstructions,
  languageSelectOptions
} from '../store/languageInstructions';

export default {
    components: {
      NhsCard,
      NhsButton,
      NhsMain,
      NhsRow,
      NhsCol,
      NhsSelect
    },
    props:{
      languageCode: String
    },
    data(){
        return {
            removePrompt: false,
            userBrowser: navigator.userAgent,
            languageSelect: this.languageCode,
            instructions: languageInstructions[this.languageCode],
            languageSelectOptions: languageSelectOptions,
        }
    },
    watch: {
      languageSelect: function(){
        this.handleLanguageSelect();
      }
    },
    methods: {
      confirmHandler(){
        this.$cookies.set("remove_langauge_prompt", this.removePrompt);
        this.$emit("closeLanguagePopUp");
      },
      openQuickLook(id){
        this.$emit("openQuickLook", id)
      },
      logDetails(){
        this.onClick(this.data, this.index);
      },
      handleLanguageSelect(){
        if(languageInstructions[this.languageSelect]){
          this.instructions = languageInstructions[this.languageSelect]
        }else{
          this.instructions = languageInstructions["en"];
        }
      }
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
    }
}
</script>

<style>

  body {
    overflow: hidden;
  }
  
  .chrome{
        color: #003087;
  }
  .safari{
        color: #003087;
  }
  

  .pop-up-container {
    position: fixed;
    overflow: hidden;
    height: 100vh;
    width: 100vw;
    top: 0;
    left: 0;
    z-index: 999999;
    background-color: rgba(0, 0, 0, 0.3);
    display: grid;
    align-items: center;
    justify-items: center;
  }

  .pop-up {
    width: 80%;
    max-width: 600px;
  }

  .pop-up .nhsuk-main-wrapper {
    padding: 0px;
  }

  .pop-up .nhsuk-width-container{
    max-height: 70vh;
    overflow-y: scroll;
    overflow-x: hidden;
    padding: 0 16px;
    margin: 0;
  }

  .confirm-button {
    width: 100%;
  }

  @media (max-width: 48.0625em){
    .nhsuk-grid-column-two-thirds {
      margin-bottom: 20px;
    }
  }
</style>