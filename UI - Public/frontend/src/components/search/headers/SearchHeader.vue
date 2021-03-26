<template>
  <div
    class="nhs-searchbar">
    <nhs-heading
      class="search-title"
      size="m">
      Search
    </nhs-heading>
    
    <div
      class="search-container">
        <form
          id="search"
          v-on:submit.prevent="search(searchTerm)"
          method="get"
          role="search">
          <input
            id="search-field"
            name="q"
            type="search"
            autocomplete="off"
            v-model="searchTerm"
            placeholder="Search key term or word....."
            aria-label="search-field"
            class="search-input"/>
          <button
            id="toggle-search"
            aria-controls="search"
            aria-label="Open search"
            type="submit"
            class="search-button">
            <i class="fa fa-search"/>
          </button>
          <div class="custom-control custom-switch multi-switch">
            <input type="checkbox" class="custom-control-input" id="customSwitches" v-model="multiEnabled" @change="getSwitchValue">
            <label class="custom-control-label" for="customSwitches">Multilingual Mode <i v-on:click.prevent="showPopup" class='info-button fas fa-info-circle'></i></label>
          </div>
          
        </form>
    </div>
  </div>
</template>
<script>
  import {NhsHeading} from 'nhsuk-frontend-vue';
  
  export default {
    name: "SearchHeader",
    components: {
      // NhsInput,
      // NhsButton
      NhsHeading,
    },
    props:{
      searchTerm: String,
      multiEnabled: Boolean,
    },
    methods: {
      search(searchTerm){
        this.$emit('initiate-basic-search', searchTerm)
      },
      getSwitchValue: function(){
        this.$emit('update-multi-lang', this.multiEnabled);
      },
      showPopup: function(){
        this.$emit('show-popup');
      }
    }
  }
</script>

<style scoped>

  .nhs-searchbar {
    height: 130px;
  }

  .search-title {
    padding: 10px 0px;
    margin: 0px;
    margin: 12px 0px;
    padding-left: 6px;
    padding-right: 5px;
  }

  .search-container {
    width: 100%;
    height: 40px;
    padding-left: 5px;
    padding-right: 5px;
  }

  .search-button {
    width: 44px;
    height: 40px;
    background-color: #003087;
    color: #fff;
    border: none;
    border-bottom-right-radius: 4px;
    border-top-right-radius: 4px;
  }

  .search-input {
    width: calc(100% - 44px);
    height: 40px;
    padding-left: 12px;
    border: 2px solid #003087;
    border-right: none;
    border-bottom-left-radius: 4px;
    border-top-left-radius: 4px;
  }

  input.search-input:focus{
    outline-offset: 0;
    outline: none;
    border: 2px solid rgb(0, 95, 204);
    border-right: none;
  }

  .search-title {
    padding: 10px 0px;
  }

  #search { 
    display:flex;
    align-items: center;
  }

  .nhsuk-header__search-form{
    display:flex;
    align-items: center;
  }

  .multi-switch{
    line-height: normal !important;
    padding-left: 3rem;
  }

  .info-button {
    color: rgb(0, 95, 204);
  }

  .info-button:hover {
    color: rgba(0, 95, 204, 0.5);
  }
</style>
