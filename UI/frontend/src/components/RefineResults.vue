<template>

  <div
    class="filter-container">
    <nhs-select
      v-model="searchOrder"
      class="search-order"
      label="Sort by">
      <option v-bind:value=1>Relevance</option>
      <option v-bind:value=2>Coverage Date (Newest first)</option>
      <option v-bind:value=3>Coverage Date (Oldest first)</option>
    </nhs-select>


    <div
        class="grid-container">
        <nhs-button
            class="grid-item feedback-button"
            color="secondary"
            @click="resetFilter">
            Clear filters
        </nhs-button>
        <nhs-button
            class="grid-item feedback-button"
            @click="applyFilter">
            Apply filters
        </nhs-button>
    </div>

    <nhs-details
      open  
      text="Coverage Date">
      <div
        class="nhsuk-form-group">
        <label
          for="NhsInput-dateFrom"
          class="nhsuk-label">
          Date from
        </label>
        <input
          id="NhsInput-dateFrom"
          type="date"
          class="nhsuk-input"
          v-model="startDate"
          :class="{'disabled': allDates}"
          :disabled="allDates">
      </div>
      <div
        class="nhsuk-form-group">
        <label
          for="NhsInput-dateTo"
          class="nhsuk-label">
          Date to
        </label>
        <input
          id="NhsInput-dateTo"
          type="date"
          class="nhsuk-input"
          v-model="endDate"
          :class="{'disabled': allDates}"
          :disabled="allDates">
      </div>
      <div
        class="nhsuk-checkboxes">
        <div
          class="nhsuk-checkboxes__item">
          <input
            aria-label="checkbox input"
            type="checkbox"
            class="nhsuk-checkboxes__input"
            v-model="allDates">
          <label
            class="nhsuk-checkboxes__label nhsuk-label">
            Any Date
          </label>
        </div>
      </div>
    </nhs-details>

    <div
      v-for="filter in this.filters"
      :key="filter.fieldName">
      <nhs-details
        open
        :text="filter.fieldTitle">
        <div
          class="nhsuk-checkboxes">
          <div
            class="nhsuk-checkboxes__item"
            v-for="value in filter.data"
            :key="value">
            <input
              :checked="isChecked(filter.fieldName, value)"
              type="checkbox"
              class="nhsuk-checkboxes__input"
              aria-label="checkbox input"
              :value="value"
              @click="checkFilter(filter.fieldName, value)">
            <label
              class="nhsuk-checkboxes__label nhsuk-label">
              {{value}}
            </label>
          </div>
        </div>
      </nhs-details>
    </div>        
  </div>
</template>


<script>
  import _ from 'lodash';
  import {setSearchFilters} from '../store/mutations/searchTypes';
  import store from '../store';
  import { json2csv } from 'json-2-csv';
  import {NhsSelect, NhsDetails, NhsButton} from 'nhsuk-frontend-vue';


  function prettifyDate(date){
    return date.toISOString().substr(0, date.toISOString().lastIndexOf("T"))
  }

  const DEFAULT_FILTERS = {
    searchOrder: 1,
    allDates: true,
    checkBoxFilters: [],
    startDate: prettifyDate(new Date()),
    endDate: prettifyDate(new Date()),
  }

  export default {
    name: "RefineResults",
    components: {
      NhsButton,
      NhsSelect,
      NhsDetails
    }, 
    methods: {
      exportResults(){
        const sourceData = this.results.hits.map(item => item["_source"]);
        json2csv(sourceData, (err, array) => {
          this.downloadCsv(`export-${new Date().toISOString()}`, array, {expandArrayObjects: true})
        });
      },
      downloadCsv(name, content) {
        var element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
        element.setAttribute('download', `${name}.csv`);

        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
      },
      applyFilter(){
        this.lastState = {
          searchOrder: this.searchOrder,
          allDates: this.allDates,
          checkBoxFilters: this.checkBoxFilters,
          startDate: this.startDate,
          endDate: this.endDate,
        }
        store.dispatch({
          type: setSearchFilters,
          filters: this.lastState,
        })
        this.$emit('search-params-changed');
      },
      resetFilter(){
        this.lastState = {
          searchOrder: 1,
          allDates: true,
          checkBoxFilters: [],
          startDate: prettifyDate(new Date()),
          endDate: prettifyDate(new Date()),
        };
        store.dispatch({
          type: setSearchFilters,
          filters: this.lastState,
        })
        this.$emit('search-params-changed');
      },
      dateEvent(_,b){
        //TODO: Can be removed as the model will attach the values to the start and end date variables
        const [start, end] = b;
        this.startDate = start;
        this.endDate = end;
      },
      filterAttribute(a,b){
        switch(a){
          case "Exhibit":
            this.filteredExhibits = b;
            break;
          case "Operation":
            this.filteredOperations = b
            break;
          default:
            break;
        }
        this.$emit('filter-attribute', a, b);
      },
      checkFilter(group, value){
        if(this.checkBoxFilters.some(element => element.name == group)){
          const index = this.checkBoxFilters.findIndex(element => element.name == group);
          if(this.checkBoxFilters.some(element => element.values.includes(value))){
            if(this.checkBoxFilters[index].values.length == 1){
              this.checkBoxFilters.splice(index, 1);
            }else{
              const valueIndex = this.checkBoxFilters[index].values.findIndex(element => element == value);
              this.checkBoxFilters[index].values.splice(valueIndex, 1);
            }
          }else{
            this.checkBoxFilters[index].values.push(value);
          }
        }else{
          this.checkBoxFilters.push(
            {
              "name": group,
              "values": [
                value
              ]
            }
          )
        }
      },
      isChecked(group, value){
        if(this.activeFilters.checkBoxFilters){
          var checkBoxFilter = this.activeFilters.checkBoxFilters.filter(item => item.name == group);
          if(checkBoxFilter.length > 0){
            if(checkBoxFilter[0].values.includes(value)){
              return true
            }
          }
        }
        return false;
      }
    },
    props: {
      results: Object,
      activeFilters: Object
    },
    mounted(){
      if(this.activeFilters){
        if(this.activeFilters.allDates != null){
          this.allDates = this.activeFilters.allDates;
        }
        if(this.activeFilters.startDate){
          this.startDate = this.activeFilters.startDate;
        }
        if(this.activeFilters.endDate){
          this.endDate = this.activeFilters.endDate;
        }
        if(this.activeFilters.searchOrder){
          this.searchOrder = this.activeFilters.searchOrder;
        }

        store.dispatch({
          type: setSearchFilters,
          filters: this.activeFilters,
        })

      }else{
        store.dispatch({
          type: setSearchFilters,
          filters: this.lastState,
        })
      }
    },
    computed: {
      hasChanged(){
        return (this.lastState.searchOrder !== this.searchOrder)
        || (this.lastState.allDates !== this.allDates)
        || (!this.allDates && (this.startDate != this.lastState.startDate))
        || (!this.allDates && (this.endDate != this.lastState.endDate))
        || !_.isEqual(_.sortBy(this.filteredExhibits), _.sortBy(this.lastState.filteredExhibits))
        || !_.isEqual(_.sortBy(this.filteredOperations), _.sortBy(this.lastState.filteredOperations));
      },
      filters(){
        return [
            {
                fieldName: 'source',
                fieldTitle: 'Sources',
                data: this.results['filters']['source']
            },
            // {
            //     fieldName: 'author',
            //     fieldTitle: 'Author',
            //     data: this.results['filters']['author']
            // },
              {
                  fieldName: 'type',
                  fieldTitle: 'Type',
                  data: this.results['filters']['type']
              },
            {
                fieldName: 'license_title',
                fieldTitle: 'Licence',
                data: this.results['filters']['license_title']
            }
            // ,
            // {
            //     fieldName: 'title.keyword',
            //     fieldTitle: 'Title',
            //     data: this.results['filters']['title']
            // }
        ]
      }
    },
    data(){
      return{
        ...DEFAULT_FILTERS,
        lastState: {...DEFAULT_FILTERS}
      }
    }
  }
</script>

<style scoped>
  .shadow-top{
    box-shadow: 0 6px 20px 0 rgba(0, 0, 0, 0.19), 0 8px 17px 0 rgba(0, 0, 0, 0.2);
  }

  .disabled {
    opacity: 0.4;
    pointer-events: none;
  }

  .grid-container {
    display: grid;
    grid-gap: 10px;
    margin-bottom: 24px;
  }

  .feedback-button.nhsuk-button{
    margin-bottom: 0;
  }

  .grid-item.feedback-button {
    padding: 3px 16px;
  }

  @media only screen and (max-width: 1200px) and (min-width: 768px){
    .grid-item:nth-child(1) {
      grid-row: 1;
      margin-bottom: 5px;
    }
    
    .grid-item:nth-child(2) {
      grid-row: 2;
    }

  }

</style>

<style lang="postcss">
  .search-order .nhsuk-select {
    width: 100%;
  }
</style>

