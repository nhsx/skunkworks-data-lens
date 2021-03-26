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
        <div>
            <p
                v-if="data.introduction">
                {{data.introduction}}
            </p>
            <div
                v-if="data.description">
                <p
                    v-for="descriptionString in descriptionArray"
                    :key="descriptionString"
                    v-html="descriptionString">
                </p>
            </div>
            
        <div
            v-if="data.url"
            v-on:click="redirect(data.url)">
            <nhs-action-link
                href="">
                Click here to be re-directed to the NHS Digital website
            </nhs-action-link>
        </div>
        </div>

        <nhs-summary-list
            :data="keySummaryData">
            <template #item="item">
                <nhs-summary-list-item type="key">{{item.props.key}}</nhs-summary-list-item>
                <nhs-summary-list-item type="value" v-html="item.props.value"></nhs-summary-list-item>
            </template>
        </nhs-summary-list>

        <div
            v-if="data.resources">
            <h1
                class="nhsuk-heading-m">
                Resources
            </h1>
            <nhs-table
                :headers="[
                    {
                        text: 'Name',
                        value: 'name'
                    },
                    {
                        text: 'Format',
                        value: 'format'
                    },
                    {
                        text: 'URL',
                        value: 'url'
                    },
                    {
                        text: 'Preview',
                        value: 'preview'
                    }

                ]"
                :data="keyResourceDataV2"
                :responsive="false">
                <template #[`item.url`]="item">
                    <a class="nhs-body-s" :href="item.props.url" target="_blank">View Source</a>
                </template>
                <template #[`item.preview`]="item">
                    <a
                        class="nhs-body-s"
                        href="#"
                        v-if="item.props.csv || item.props.pdf || item.props.xls || item.props.docx"
                        v-on:click.prevent="openModal(item.props)">
                        Preview Data
                    </a>
                </template>
            </nhs-table>
            
        </div> 

        <mdb-modal :show="csvModal" @close="csvModal = false">
            <mdb-modal-header>
                <mdb-modal-title>Preview For {{modalName}}</mdb-modal-title>
            </mdb-modal-header>
            <mdb-modal-body>
                <nhs-row>
                    <mdb-datatable-2
                        :value="'/api/getCSV?CSVURL=' + modalDataURL"
                        striped
                        bordered
                        :display="3"
                    />
                </nhs-row>
            </mdb-modal-body>
            <mdb-modal-footer>
                <nhs-button @click.native="csvModal = false">Close</nhs-button>
            </mdb-modal-footer>
        </mdb-modal>

        <div v-if="pdfModal" @click="pdfModal = false" class="closeButton"><mdb-icon far icon="window-close" class="hoverButton" size="2x"/></div>
        <mdb-modal :show="pdfModal" @close="pdfModal = false">
            <iframe
                class="pdfViewer"
                :src="'/api/getPDF?DataURL=' + modalDataURL"
                :title="modalName"/>
        </mdb-modal>

        <mdb-modal :show="xlsxModal" @close="xlsxModal = false">
            <mdb-modal-header>
                <mdb-modal-title>Preview For {{modalName}}</mdb-modal-title>
            </mdb-modal-header>
            
            <mdb-modal-body>
                <nhs-row class="sheetButtons">
                    <nhs-button  v-for="(value, key) in xlsData" v-bind:key="key" @click.native="changeSheet(value)" style="margin-bottom:15px; margin-left:10px; margin-right:10px;">{{key}}</nhs-button>
                </nhs-row>
                <loading
                :active.sync="isLoading"
                :is-full-page="false"/>
                <nhs-row style="height:62vh;">
                    <canvas-datagrid class="myGridStyle" :data.prop="currentSheet" v-bind:style="{width : tableWidth, height:tableHeight, display:displayType}"></canvas-datagrid>
                </nhs-row>
            </mdb-modal-body>
            <mdb-modal-footer>
                <nhs-button color="secondary" @click.native="xlsxModal = false">Close</nhs-button>
            </mdb-modal-footer>
        </mdb-modal>

        <!-- <div
            v-if="checkTableKeyString('Launch and submission dates')">
            <nhs-card
                feature
                heading="Launch and submission dates"
                heading-classes="nhsuk-heading-m">
                <template #description>
                    <p
                        v-if="data['Launch and submission dates'].strings"
                        v-html="data['Launch and submission dates'].strings"/>
                    <nhs-table
                        :headers="keyTableHeaders('Launch and submission dates')"
                        :data="keyTableData('Launch and submission dates')"
                        :responsive="false">
                    </nhs-table>
                </template>
            </nhs-card>
        </div> -->

        <div
            v-if="stringOrTableKeys.length > 0">
            <div
                v-for="stringOrTableKey in stringOrTableKeys"
                :key="stringOrTableKey.key">
                <nhs-card
                    feature
                    :heading="stringOrTableKey.key"
                    heading-classes="nhsuk-heading-m">
                    <template #description>
                        <nhs-body
                            size="s"
                            v-if="data[stringOrTableKey.key]['html']"
                            v-html="data[stringOrTableKey.key]['html'].replaceAll('<h3>', '<p>').replaceAll('</h3>', '</p>').replaceAll('width:377.45pt', '')"/>
                        <div
                            v-else>
                            <div
                                v-if="data[stringOrTableKey.key]['strings']">
                                <p
                                    v-html="data[stringOrTableKey.key]['strings']"/>
                            </div>
                            <div
                                v-if="data[stringOrTableKey.key]['table']">
                                <nhs-table
                                    :headers="keyTableHeaders(stringOrTableKey.key, 'table')"
                                    :data="keyTableData(stringOrTableKey.key, 'table')"
                                    :responsive="false">
                                </nhs-table>
                            </div>
                        </div>
                    </template>
                </nhs-card>
            </div>
        </div>
    </div>
</template>

<script>
import {
    NhsSummaryList,
    NhsSummaryListItem,
    NhsTable,
    NhsRow,
    NhsCard,
    NhsButton,
    NhsActionLink,
    NhsBody
} from 'nhsuk-frontend-vue';

import {mdbDatatable2, mdbModal, mdbModalHeader, mdbModalTitle, mdbModalBody, mdbModalFooter, mdbIcon} from 'mdbvue'

import Loading from 'vue-loading-overlay';

require('../../../node_modules/canvas-datagrid/dist/canvas-datagrid');

export default {
    name: "NhsDigitalItem",
    data: function () {
        return {
                csvModal: false,
                pdfModal: false,
                xlsxModal: false,
                isLoading: false,
                xlsData: {},
                currentSheet: {},
                modalName: '',
                modalDataURL: '',
                validPreview: {},
                tableWidth: '99%',
                tableHeight: '99%',
                displayType: 'block'
            }
    },
    props: {
      data: {
        type: Object,
        required: true,
      }
    },
    components: {
        NhsSummaryList,
        NhsSummaryListItem,
        NhsTable,
        NhsCard,
        NhsButton,
        NhsRow,
        mdbDatatable2,
        mdbModal,
        mdbModalHeader,
        mdbModalTitle,
        mdbModalBody,
        mdbModalFooter,
        mdbIcon,
        NhsActionLink,
        Loading,
        NhsBody
    },
    computed: {
        keySummaryData(){
            var resultArray = [];
            if(this.data.spatial_coverage){
                resultArray.push({
                    key: 'Spatial Coverage',
                    value: this.data.spatial_coverage
                });
            }
            if(this.data.date_published){
                resultArray.push({
                    key: 'Date Published',
                    value: this.data.date_published
                });
            }
            if(this.data.temporal_coverage){
                resultArray.push({
                    key: 'Temporal Coverage',
                    value: this.data.temporal_coverage
                });
            }
            return resultArray;
        },
        keyResourceDataV2(){
            var resultArray = [];
            if(this.data.resources){
                this.data.resources.forEach(element => {
                    var object = {};
                    let fileType = '';
                    let fileType2 = '';
                    if(element.title){
                        object["name"] = element.title;
                    }
                    if(element.url){
                        object["url"] = element.url;
                        fileType = element.url.split('.').pop().toLowerCase();
                        fileType2 = element.url.split('/').pop().toLowerCase();
                        if(fileType == 'pdf' || fileType2 == 'pdf'){

                            fileType2.length < fileType.length ? object["format"] = fileType2 : object["format"] = fileType;

                            object['pdf'] = {
                                src: element.url,
                                name: element.name,
                            };
                            fetch('/api/getPDF?DataURL=' + element.url)
                            .then(response => {
                                const contentType = response.headers.get("Content-Type");
                                const contentURL = response.headers.get('Content-URL');
                                if (contentType && contentType.indexOf("application/json") !== -1) {
                                    return response.json().then(() => {
                                        this.$set(this.validPreview, contentURL, false)
                                    });
                                } else {
                                    this.$set(this.validPreview, contentURL, true)
                                }
                            })
                            console.log(object);
                        }
                        else if (fileType == 'csv')
                        {
                            object["format"] = fileType;
                            object['csv'] = {
                                name: element.title,
                                src: element.url,
                            };
                            this.$set(this.validPreview, encodeURI(element.url), true)
                        }
                        else if (fileType == 'xlsx' || fileType == 'xls')
                        {
                            object["format"] = fileType;
                            object['xls'] = {
                                name: element.title,
                                src: element.url,
                            };
                            this.$set(this.validPreview, encodeURI(element.url), true)
                        }
                        else
                        {
                            this.$set(this.validPreview, encodeURI(element.url), false)
                        }
                    }
                    resultArray.push(object);
                });
            }
            return resultArray;
        },
        stringOrTableKeys(){
            var keyArray = [];
            var keys = Object.keys(this.data);
            keys.forEach((key) => {
                var childKeys = Object.keys(this.data[key]);
                var childKeysArray = []
                childKeys.forEach((childKey) => {
                    if(childKey.indexOf("table") > -1 || childKey.indexOf("strings") > -1 || childKey.indexOf("html") > -1){
                        childKeysArray.push(childKey);
                    }
                });
                if(childKeysArray.length > 0){
                    childKeysArray.sort();
                    keyArray.push({
                        key: key,
                        childKeys: childKeysArray
                    });
                }
            });

            return keyArray;

        },
        descriptionArray(){
            if(this.data.description){
                if(typeof this.data.description == "string"){
                    return [this.data.description];
                }
                return this.data.description.filter(value => value.trim() !== '');
            }
            return [];
        }
    },
    methods: {
        redirect(link, target = '_blank'){
            this.$emit('redirect', link, target);
        },
        prettifyDate(date){
            this.$emit('prettifyDate', date);
        },
        checkTableKeyString(tableString){
            if(this.data[tableString]){
                var keys = Object.keys(this.data[tableString]);
                var tableKeyString;
                keys.forEach((key) => {
                    if(key.indexOf("table") > -1){
                        tableKeyString = key;
                    }
                });
                if(tableKeyString){
                    return true;
                }
            }
            return false;
        },
        keyTableHeaders(tableString, tableKeyString){
            var headers = [];
            var keys = Object.keys(this.data[tableString][tableKeyString][0]);
            keys.forEach((key) => {
                headers.push({
                    text: key,
                    value: key
                })
            });
            return headers;
        },
        keyTableData(tableString, tableKeyString){
            return this.data[tableString][tableKeyString];
        },
        stringContains(string, likeString) {
            return string.indexOf(likeString) > -1;
        },
        openModal(resource){
            if (resource.csv)
            {
                this.modalName = resource.csv.name;
                this.modalDataURL = resource.csv.src;
                this.csvModal = true;
            }
            else if (resource.pdf)
            {
                this.modalName = resource.pdf.name;
                this.modalDataURL = resource.pdf.src;
                this.pdfModal = true;
            }
            else if(resource.xls)
            {
                this.isLoading = true;
                this.xlsxModal = true;
                fetch('/api/getXLS?DataURL=' + resource.xls.src)
                .then(res => res.json())
                .then(json => {
                    this.isLoading = false;
                    this.modalName = resource.xls.name;
                    this.xlsData = json;
                    let firstSheet = json[Object.keys(json)[0]]

                    let L = 0;
                    firstSheet.forEach(function(r) { if(L < r.length) L = r.length; });
                    for(var i = firstSheet[0].length; i < L; ++i) {
                        firstSheet[0][i] = "";
                    }

                    this.currentSheet = firstSheet

                    this.tableWidth = '99%';
                    this.tableHeight = '99%';
                });
            }
        },
        changeSheet(value){
            let L = 0;
            value.forEach(function(r) { if(L < r.length) L = r.length; });
            for(var i = value[0].length; i < L; ++i) {
                value[0][i] = "";
            }
            this.tableWidth = '100%';
            this.tableHeight = '100%';
            this.currentSheet = value;
        }
    },
}
</script>
<style lang="postcss" scoped>
    
    .pdfViewer {
        width: 100%;
        height: 93vh;
    }

    .sheetButtons {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
    }

    .closeButton {
        position: fixed;
        right: 1%;
        top: 1%;
        z-index: 10000;
        font-weight: 700;
        font-size: large;
        cursor: pointer;
    }

    .hoverButton {
        transition: 0.3s;
        color: white;
    }

    .hoverButton:hover {
        transition: 0.3s;
        color: rgb(61, 61, 61) !important;
    }
</style>

<style>

    .pdfViewer {
        width: 100%;
        height: 93vh;
    }

    .sheetButtons {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
    }

    .closeButton {
        position: fixed;
        right: 1%;
        top: 1%;
        z-index: 10000;
        font-weight: 700;
        font-size: large;
        cursor: pointer;
    }

    .hoverButton {
        transition: 0.3s;
        color: white;
    }

    .hoverButton:hover {
        transition: 0.3s;
        color: rgb(61, 61, 61) !important;
    }

    .modal-dialog {
        max-width: 90% !important;
        width: 90% !important;
    }

    .table {
        width: 100%;
    }
</style>