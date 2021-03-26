<template>
    <div>
        <h1
            class="nhsuk-heading-l">
            <a
                v-if="data.title"
                href="#"
                v-on:click="redirect(data.url)">
                {{data.title}}
            </a>
        </h1>
        <p
            v-if="data.description"
            class="text-clip-overflow use-white-space">
            {{data.description}}
        </p>
        <div
            v-if="data.datasetfields.abstract">
            <p
                class="nhsuk-heading-s">
                Abstract
            </p>
            <p
                v-html="data.datasetfields.abstract"/>
        </div>
       <div
            v-if="data.url"
            v-on:click="redirect(data.url)">
            <nhs-action-link
                href="">
                Click here to be re-directed to the Health Innovation Gateway website
            </nhs-action-link>
        </div>
        
            

        <nhs-card
            feature
            v-if="this.data"
            heading="Details"
            heading-classes="nhsuk-heading-m">
            <template #description>
                <nhs-summary-list
                    :data="keyDetailsData">
                    <template #item="item">
                        <nhs-summary-list-item type="key">{{item.props.key}}</nhs-summary-list-item>
                        <nhs-summary-list-item type="value" v-html="item.props.value"></nhs-summary-list-item>
                    </template>
                </nhs-summary-list>
            </template>
        </nhs-card>
        <nhs-card
            feature
            v-if="this.data"
            heading="Data Access"
            heading-classes="nhsuk-heading-m">
            <template #description>
                <nhs-summary-list
                    :data="keyDataAccessData">
                    <template #item="item">
                        <nhs-summary-list-item type="key">{{item.props.key}}</nhs-summary-list-item>
                        <nhs-summary-list-item type="value" v-html="item.props.value"></nhs-summary-list-item>
                    </template>
                </nhs-summary-list>
            </template>
        </nhs-card>
        <nhs-card
            feature
            v-if="this.data"
            heading="Coverage"
            heading-classes="nhsuk-heading-m">
            <template #description>
                <nhs-summary-list
                    :data="keyCoverageData">
                    <template #item="item">
                        <nhs-summary-list-item type="key">{{item.props.key}}</nhs-summary-list-item>
                        <nhs-summary-list-item type="value" v-html="item.props.value"></nhs-summary-list-item>
                    </template>
                </nhs-summary-list>
            </template>
        </nhs-card>
        <nhs-card
            feature
            v-if="this.data"
            heading="Demographics"
            heading-classes="nhsuk-heading-m">
            <template #description>
                <nhs-summary-list
                    :data="keyDemoData">
                    <template #item="item">
                        <nhs-summary-list-item type="key">{{item.props.key}}</nhs-summary-list-item>
                        <nhs-summary-list-item type="value" v-html="item.props.value"></nhs-summary-list-item>
                    </template>
                </nhs-summary-list>
            </template>
        </nhs-card>
        <nhs-card
            feature
            v-if="this.data"
            heading="Related Resources"
            heading-classes="nhsuk-heading-m">
            <template #description>
                <nhs-summary-list
                    :data="keyResourceData">
                    <template #item="item">
                        <nhs-summary-list-item type="key">{{item.props.key}}</nhs-summary-list-item>
                        <nhs-summary-list-item type="value" v-html="item.props.value"></nhs-summary-list-item>
                    </template>
                </nhs-summary-list>
            </template>
        </nhs-card>
                
    </div>
</template>

<script>

import {
     NhsSummaryList,
     NhsSummaryListItem,
     NhsCard,
     NhsActionLink
} from 'nhsuk-frontend-vue';

export default {
    name: "HdrItem",
    props: {
      data: {
        type: Object,
        required: true
      }
    },
    components:{
        NhsSummaryList,
        NhsSummaryListItem,
        NhsCard,
        NhsActionLink
    },
    computed: {
        keyDetailsData(){
            var resultArray = [];
            if(this.data.datasetfields.periodicity){
                resultArray.push({
                    key: 'Periodicity',
                    value: this.data.datasetfields.periodicity
                });
            }
            if(this.data.datasetfields.releaseDate){
                resultArray.push({
                    key: 'Release Date',
                    value: this.prettifyDate(this.data.datasetfields.releaseDate)
                });
            }
            if(this.data.datasetfields.conformsTo){
                resultArray.push({
                    key: 'Standard',
                    value: this.data.datasetfields.conformsTo
                });
            }
            return resultArray;
        },
        keyDataAccessData(){
            var resultArray = [];
            if(this.data.datasetfields.accessRights){
                resultArray.push({
                    key: 'Access Rights',
                    value: this.data.datasetfields.accessRights
                });
            }
            if(this.data.datasetfields.accessRequestDuration){
                resultArray.push({
                    key: 'Request Time',
                    value: this.data.datasetfields.accessRequestDuration
                });
            }
            return resultArray;
        },
        keyCoverageData(){
            var resultArray = [];
            if(this.data.datasetfields.jurisdiction){
                resultArray.push({
                    key: 'Jurisdiction',
                    value: this.data.datasetfields.jurisdiction
                });
            }
            if(this.data.datasetfields.geographicCoverage[0]){
                resultArray.push({
                    key: 'Geographical Coverage',
                    value: this.data.datasetfields.geographicCoverage[0]
                });
            }
            if(this.data.datasetfields.datasetStartDate){
                resultArray.push({
                    key: 'Dataset Start Date',
                    value: this.prettifyDate(this.data.datasetfields.datasetStartDate)
                });
            }
            if(this.data.datasetfields.datasetEndDate){
                resultArray.push({
                    key: 'Dataset End Data',
                    value: this.prettifyDate(this.data.datasetfields.datasetEndDate)
                });
            }
            if(this.data.datasetv2.coverage.pathway){
                resultArray.push({
                    key: 'Pathway',
                    value: this.prettifyDate(this.data.datasetv2.coverage.pathway)
                });
            }
            return resultArray;
        },
        keyDemoData(){
            var resultArray = [];
            if(this.data.datasetfields.statisticalPopulation){
                resultArray.push({
                    key: 'Statistical Population',
                    value: this.data.datasetfields.statisticalPopulation
                });
            }
            if(this.data.datasetfields.ageBand){
                resultArray.push({
                    key: 'Age Band',
                    value: this.data.datasetfields.ageBand
                });
            }
            return resultArray;
        },
        keyResourceData(){
            var resultArray = [];
            if(this.data.datasetfields.physicalSampleAvailability){
                resultArray.push({
                    key: 'Physical Sample Availability',
                    value: this.data.datasetfields.physicalSampleAvailability.join(", ")
                });
            }
            
            return resultArray;
        }
    },
    

    methods: {
        redirect(link, target = '_blank'){
            this.$emit('redirect', link, target);
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
    }
}
</script>

<style lang="postcss" scoped>

    
</style>
<style>
    .modal-dialog {
        max-width: 90% !important;
        width: 90% !important;
    }
    
</style>
<style>
    .modal-dialog {
        max-width: 90% !important;
        width: 90% !important;
    }
    .text-clip-overflow {
        word-wrap: break-word;
        width: 100%;
    }
    .use-white-space {
        white-space: pre-line;
    }
</style>