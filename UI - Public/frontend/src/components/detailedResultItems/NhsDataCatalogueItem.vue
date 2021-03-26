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
        <h1
            class="nhsuk-heading-xs"
            v-if="data.author_email">
            Author Email: 
            <a
                :href="`mailto:${data.author_email}`"
                target="_blank">
                {{data.author_email}}
            </a>
        </h1>
        <div>
            <p
                v-if="data.notes">
                {{data.notes}}
            </p>
        </div>
        <div
            v-if="data.url"
            v-on:click="redirect(data.url)">
            <nhs-action-link
                href="">
                Click here to be re-directed to the NHS Data Catalogue website
            </nhs-action-link>
        </div>
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
                        text: 'Description',
                        value: 'description'
                    },
                    {
                        text: 'Format',
                        value: 'format'
                    },
                    {
                        text: 'State',
                        value: 'state'
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

        <div
            v-if="data.resources">
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

            <div v-if="docModal" @click="docModal = false" class="closeButton"><mdb-icon far icon="window-close" class="hoverButton" size="2x"/></div>
            <mdb-modal :show="docModal" @close="docModal = false">
                <iframe
                    class="pdfViewer"
                    :src="'/api/getDOCX?DataURL=' + modalDataURL"
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
            
        <div
            v-if="data.groups">
            <h1
                class="nhsuk-heading-m">
                Groups
            </h1>
            <div
                v-for="group in data.groups"
                :key="group.id">
                <nhs-expander
                    :text="group.title">
                    <p>
                        {{group.description}}
                    </p>
                </nhs-expander>
            </div>
        </div>
        <nhs-summary-list
            :data="keySummaryData">
            <template #item="item">
                <nhs-summary-list-item type="key">{{item.props.key}}</nhs-summary-list-item>
                <nhs-summary-list-item type="value" v-html="item.props.value"></nhs-summary-list-item>
            </template>
        </nhs-summary-list>

        </div>
    </div>
</template>

<script>

import {
    NhsSummaryList,
    NhsSummaryListItem,
    NhsExpander,
    NhsButton,
    NhsRow,
    NhsActionLink,
    NhsTable
} from 'nhsuk-frontend-vue';

import {mdbDatatable2, mdbModal, mdbModalHeader, mdbModalTitle, mdbModalBody, mdbModalFooter, mdbIcon} from 'mdbvue'

import Loading from 'vue-loading-overlay';

export default {
    name: "NhsDataCatalogueItem",
    data: function () {
    return {
            csvModal: false,
            pdfModal: false,
            docModal: false,
            xlsxModal: false,
            isLoading: false,
            modalName: "",
            modalDataURL: '',
            xlsData: {},
            currentSheet: {},
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
        NhsExpander,
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
        NhsTable,
        Loading
    },
    computed: {
        keySummaryData(){
            var resultArray = [];
            if(this.data.frequency){
                resultArray.push({
                    key: 'Frequency',
                    value: this.data.frequency[0]
                });
            }
            if(this.data.state){
                resultArray.push({
                    key: 'State',
                    value: this.data.state
                });
            }
            if(this.data.license_url && this.data.license_title){
                resultArray.push({
                    key: 'License',
                    value: '<a href="' + this.data.license_url + '" target="_blank">' + this.data.license_title + '</a>'
                });
            }
            if(this.data.origin){
                resultArray.push({
                    key: 'Origin',
                    value:  this.data.origin 
                });
            }
            return resultArray;
        },
        keyResourceDataV2(){
            var resultArray = [];
            if(this.data.resources){
                this.data.resources.forEach(element => {
                    var object = {};
                    if(element.name){
                        object["name"] = element.name;
                    }
                    if(element.description){
                        object["description"] = element.description;
                    }
                    if(element.format){
                        object["format"] = element.format;
                    }
                    if(element.format){
                        object["format"] = element.format;
                        if(element.format.toLowerCase() == 'pdf'){
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
                        }
                        if(element.format.toLowerCase() == 'csv'){
                            object['csv'] = {
                                src: element.url,
                                name: element.name,
                            };
                            this.$set(this.validPreview, element.url, true)
                        }

                        if (element.format.toLowerCase()== 'xlsx' || element.format.toLowerCase() == 'xls')
                        {
                            object['xls'] = {
                                name: element.name,
                                src: element.url,
                            };
                            this.$set(this.validPreview, encodeURI(element.url), true)
                        }

                        if (element.format.toLowerCase()== 'docx')
                        {
                            object['docx'] = {
                                name: element.name,
                                src: element.url,
                            };
                            this.$set(this.validPreview, encodeURI(element.url), true)
                        }
                    }
                    if(element.state){
                        object["state"] = element.state;
                    }
                    if(element.url){
                        object["url"] = element.url;
                    }
                    resultArray.push(object);
                });
            }
            return resultArray;
        },
        isValidPreview(resource)
        {
            if(resource.csv)
            {
                return this.validPreview[resource.csv.src]
            }
            if(resource.pdf)
            {
                return this.validPreview[resource.pdf.src]
            }
            if(resource.docx)
            {
                return this.validPreview[resource.docx.src]
            }
             return false
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
            console.log(resource)
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
            else if (resource.docx)
            {
                this.modalName = resource.docx.name;
                this.modalDataURL = resource.docx.src;
                this.docModal = true;
            }
            else if (resource.xls)
            {
                this.xlsData = {}
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
<style lang="postcss" scoped>
    
    .pdfViewer {
        width: 100%;
        height: 93vh;
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
    .modal-dialog {
        max-width: 90% !important;
        width: 90% !important;
    }
</style>