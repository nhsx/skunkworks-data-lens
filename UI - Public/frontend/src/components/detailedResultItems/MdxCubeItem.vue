<template>
    <div>
        <h1
            class="nhsuk-heading-l">
            <a

                v-if="data.title">
                {{data.title}}
            </a>
            
        </h1>
        <div>
            <p
                v-if="data.measure_group_notes">
                {{data.measure_group_notes}}
            </p>
        </div>
                <nhs-card
                    feature
                    heading="General Information"
                    heading-classes="nhsuk-heading-m">
                    <template #description>
                        <nhs-summary-list
                            :data="mdx_cube_SummaryData">
                            <template
                                #item="item">
                                <nhs-summary-list-item type="key">{{item.props.key}}</nhs-summary-list-item>
                                <nhs-summary-list-item type="value" v-html="item.props.value"></nhs-summary-list-item>
                            </template>
                        </nhs-summary-list>
                    </template>
                </nhs-card>
                <nhs-card
                    feature
                    class="largerKeySummaryList"
                    heading="Triggered by"
                    heading-classes="nhsuk-heading-m">
                    <template #description>
                        <nhs-summary-list
                            :data="triggered_by_SummaryData">
                            <template
                                #item="item">
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
     NhsCard
    
} from 'nhsuk-frontend-vue';

export default {
    name: "MdxCubeItem",
    props: {
      data: {
        type: Object,
        required: true
      }
    },
    components: {
         NhsSummaryList,
         NhsSummaryListItem,
         NhsCard
    },
    computed:{
        triggered_by_SummaryData(){
            var resultArray = [];
            if(this.data.triggered_by_commissioner_sign_off_deadline){
                resultArray.push({
                    key: 'Commisioner Sign of Deadline',
                    value: this.data.triggered_by_commissioner_sign_off_deadline
                });
            }
            if(this.data.triggered_by_data_publication){
                resultArray.push({
                    key: 'Data Publication',
                    value: this.data.triggered_by_data_publication
                });
            }
            if(this.data.triggered_by_hard_deadline){
                resultArray.push({
                    key: 'Hard Deadline',
                    value: this.data.triggered_by_hard_deadline
                });
            }
            if(this.data.triggered_by_provider_submission_deadline){
                resultArray.push({
                    key: 'Provider Submission Deadline',
                    value: this.data.triggered_by_provider_submission_deadline
                });
            }
            return resultArray;
        },
        mdx_cube_SummaryData(){
            var resultArray = [];
            if(this.data.frequency){
                resultArray.push({
                    key: 'Frequency',
                    value: this.data.frequency
                });
            }
            if(this.data.source_format){
                resultArray.push({
                    key: 'Source Format',
                    value: this.data.source_format
                });
            }
            if(this.data.dataset){
                resultArray.push({
                    key: 'Dataset',
                    value: this.data.dataset
                });
            }
            if(this.data.data_source){
                resultArray.push({
                    key: 'Data Source',
                    value: this.data.data_source
                });

            }
            if(this.data.data_file_notes){
                resultArray.push({
                    key: 'Data File Notes',
                    value: this.data.data_file_notes
                });
            }
            if(this.data.timetable){
                resultArray.push({
                    key: 'Timetable',
                    value: this.data.timetable
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
            this.$emit('prettifyDate', date);
        }
    }
}
</script>

<style>
    @media (min-width: 40.0525em){
        .largerKeySummaryList .nhsuk-summary-list__key {
            width: 70%;
        }
        .largerKeySummaryList .nhsuk-summary-list__value {
            width: 30%;
        }
    }
</style>