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
        <div
            v-if="data.description">
            <p>
                {{data.description}}
            </p>
        </div>
        <div
            v-if="data.url"
            v-on:click="redirect(data.url)">
            <nhs-action-link
                href="">
                Click here to be re-directed to the Office for National Statistics website
            </nhs-action-link>
        </div>
        <nhs-summary-list
            :data="keySummaryData">
            <template #item="item">
                <nhs-summary-list-item type="key">{{item.props.key}}</nhs-summary-list-item>
                <nhs-summary-list-item type="value" v-html="item.props.value"></nhs-summary-list-item>
            </template>
        </nhs-summary-list>
        <nhs-care-card
            v-if="data.main_points"
            heading="Main Points">
            <ul id="MainPoints">
                <li v-for="point in data.main_points.trim().split('\n')" :key="point">
                    {{point}}
                </li>
            </ul>
        </nhs-care-card>

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
                        v-if="validPreview[item.props.url] == true"
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
    </div>
</template>

<script>

const fetch = require('node-fetch')

import {
    NhsSummaryList,
    NhsSummaryListItem,
    NhsCareCard,
    NhsButton,
    NhsRow,
    NhsActionLink,
    NhsTable
} from 'nhsuk-frontend-vue';

import {mdbDatatable2, mdbModal, mdbModalHeader, mdbModalTitle, mdbModalBody, mdbModalFooter, mdbIcon} from 'mdbvue'

import Loading from 'vue-loading-overlay';

require('../../../node_modules/canvas-datagrid/dist/canvas-datagrid');

export default {
    name: "OnsItem",
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
        required: true
      }
    },
    components: {
        NhsSummaryList,
        NhsSummaryListItem,
        NhsCareCard,
        NhsRow,
        NhsButton,
        NhsTable,
        mdbDatatable2,
        mdbModal,
        mdbModalHeader,
        mdbModalTitle,
        mdbModalBody,
        mdbModalFooter,
        mdbIcon,
        Loading,
        NhsActionLink
    },
    computed:{
        keySummaryData(){
            var resultArray = [];
            if(this.data.contact){
                resultArray.push({
                    key: 'Contact',
                    value: this.data.contact
                });
            }
            if(this.data.type)
            {
                resultArray.push({
                    key: 'Data Type',
                    value: this.data.type
                });
            }
            if(this.data.release_date){
                resultArray.push({
                    key: 'Release Date',
                    value: this.data.release_date
                });
            }
            if(this.data.next_release){
                resultArray.push({
                    key: 'Next Release',
                    value: this.data.next_release
                });
            }
            else if(this.data.release_date)
            {
                resultArray.push({
                    key: 'Next Release',
                    value: 'TBA'
                });
            }
            if(this.data.resources){
                resultArray.push({
                    key: 'Resources',
                    value: this.data.resources.length
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
        }
    },
    methods: {
        redirect(link, target = '_blank'){
            this.$emit('redirect', link, target);
        },
        prettifyDate(date){
            this.$emit('prettifyDate', date);
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
    }
}
</script>
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

</style>