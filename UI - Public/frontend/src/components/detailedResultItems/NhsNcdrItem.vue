<template>
    <div>
        <h1
            class="nhsuk-heading-l">
            <a
                v-if="data.title"
                href="#"
                v-on:click="redirect(data.table_url)">
                {{data.title}}
            </a>
        </h1>
        <div
            v-if="data.db_description">
            <h1
                class="nhsuk-heading-s">
                Database Description
            </h1>
            <p>
                {{data.db_description}}
            </p>
        </div>
        <div
            v-if="data.table_description">
            <h1
                class="nhsuk-heading-s">
                Table Description
            </h1>
            <p>
                {{data.table_description}}
            </p>
        </div>
        <div
            v-if="data.table_url"
            v-on:click="redirect(data.table_url)">
            <nhs-action-link
                href="">
                Click here to be re-directed to the NHS England NCDR website
            </nhs-action-link>
        </div>

        <div
            v-if="data.columns">
            <nhs-list-panel
                label="Columns">
                <nhs-list-panel-item
                    v-for="(item, index) in data.columns"
                    :key="`column-${index}`"
                    :href="item.url">
                    {{item.name}}
                </nhs-list-panel-item>
            </nhs-list-panel>
        </div>
    </div>
</template>

<script>

import {
    NhsListPanel,
    NhsListPanelItem
} from 'nhsuk-frontend-vue';

export default {
    name: "NhsNcdrItem",
    props: {
      data: {
        type: Object,
        required: true
      }
    },
    components: {
        NhsListPanel,
        NhsListPanelItem
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