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
            <p
                v-else-if="data.name">
                {{data.name}}
            </p>
        </h1>
        <div>
            <p
                v-if="data.definition"
                v-html="data.definition"/>
        </div>
        <div>
            <nhs-summary-list
                :data="fingertipsSummaryData">
                <template
                    #item="item">
                    <nhs-summary-list-item type="key">{{item.props.key}}</nhs-summary-list-item>
                    <nhs-summary-list-item type="value" v-html="item.props.value"></nhs-summary-list-item>
                </template>
            </nhs-summary-list>
        </div>
        <div
            v-if="data.url"
            v-on:click="redirect(data.url)">
            <nhs-action-link
                href="">
                Click here to be re-directed to the PHE Fingertips website
            </nhs-action-link>
        </div>

        <nhs-care-card
        class="text-clip-overflow use-white-space"
            v-if="data.rationale"
            heading="Rationale">
            <p
                v-html="data.rationale"/>
        </nhs-care-card>
    </div>
</template>

<script>

import {
    NhsSummaryList,
    NhsSummaryListItem,
    NhsCareCard,
    NhsActionLink
} from 'nhsuk-frontend-vue';

export default {
    name: "PheFingertips",
    props: {
      data: {
        type: Object,
        required: true
      }
    },
    components: {
        NhsSummaryList,
        NhsSummaryListItem,
        NhsCareCard,
        NhsActionLink
    },
    computed: {
        fingertipsSummaryData(){
            var resultArray = [];
            if(this.data.frequency){
                resultArray.push({
                    key: 'Frequency',
                    value: this.data.frequency
                });
            }
            if(this.data.unit){
                resultArray.push({
                    key: 'Unit',
                    value: this.data.unit.label
                });
            }
            if(this.data.links){
                resultArray.push({
                    key: 'Links',
                    value: this.data.links
                });
            }
            if(this.data.datasource){
                resultArray.push({
                    key: 'Data Source',
                    value: this.data.datasource
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
.text-clip-overflow {
        word-wrap: break-word;
        width: 100%;
    }
    .use-white-space {
        white-space: pre-line;
    }
</style>