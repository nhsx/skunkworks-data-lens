<template>
    <div
        class="loading-background"
        v-if="isLoading">
        <loading
            :active.sync="isLoading"
            :is-full-page="true"/>
    </div>
    
    
    <div
    
        v-else-if="this.resultData">
        <nhs-card
            feature
            heading-classes="nhsuk-heading-m"
            :class="this.showFeedback ? 'feedbackBox' : 'feedbackBox showFeedbackBox'">
            <template #heading>
                <h2
                    @click="toggleShowFeedback"
                    class="nhsuk-card__heading nhsuk-card__heading--feature nhsuk-heading-m">
                    <div>Feedback</div>
                </h2>
            </template>
            <template #description>
                <p>Was this result relevant?</p>
                <p
                    v-if="feedbackGiven">
                    Thank you for your feedback.
                </p>
                <div
                    v-else
                    class="grid-container">
                    <nhs-button
                        class="grid-item feedback-button"
                        @click="buttonClick('yes')">
                        Yes
                    </nhs-button>
                    <nhs-button
                        class="grid-item feedback-button"
                        color="secondary"
                        @click="buttonClick('no')">
                        No
                    </nhs-button>
                </div>
            </template>
        </nhs-card>

        <nhs-main>

            <div>
                <a
                    class="back-button"
                    href="javascript:;"
                    onClick="history.go(-1)">
                    &lt; Go Back
                </a>
            </div>

            <div
                class="source-tag"
                v-if="this.resultData[0]._source.source">
                <a
                    href="javascript:;"
                    v-on:click="redirect(resultData[0]._source.source_url)">
                    <nhs-tag>
                        {{this.resultData[0]._source.source}}
                    </nhs-tag>
                </a>
            </div>
            
            <nhs-data-catalogue-item
                v-if="this.resultData[0]._source.source == 'NHS Data Catalogue'"
                :data="this.resultData[0]._source"
                @redirect="redirect"
                @prettifyDate="prettifyDate"/>

            <phe-fingertips-item
                v-if="this.resultData[0]._source.source == 'PHE Fingertips'"
                :data="this.resultData[0]._source"
                @redirect="redirect"
                @prettifyDate="prettifyDate"/>

            <nhs-ncdr-item
                v-if="this.resultData[0]._source.source == 'NHS England NCDR Reference Library'"
                :data="this.resultData[0]._source"
                @redirect="redirect"
                @prettifyDate="prettifyDate"/>

            <nhs-digital-item
                v-if="this.resultData[0]._source.source == 'NHS Digital'"
                :data="this.resultData[0]._source"
                @redirect="redirect"
                @prettifyDate="prettifyDate"/>
            
            <mdx-cube-item
                v-if="this.resultData[0]._source.source == 'MDX Cube'"
                :data="this.resultData[0]._source"
                @redirect="redirect"
                @prettifyDate="prettifyDate"/>

            <hdr-item
                v-if="this.resultData[0]._source.source == 'Health Data Innovation Gateway'"
                :data="this.resultData[0]._source"
                @redirect="redirect"
                @prettifyDate="prettifyDate"/>
            <ons-item
                v-if="this.resultData[0]._source.source == 'Office for National Statistics'"
                :data="this.resultData[0]._source"
                @redirect="redirect"
                @prettifyDate="prettifyDate"/>

            <div>
                <p
                    v-if="this.resultData[0]._source.coverage_start_date">
                    Coverage Start Date: {{prettifyDate(this.resultData[0]._source.coverage_start_date)}}
                </p>
                <p
                    v-if="this.resultData[0]._source.coverage_end_date">
                    Coverage End Date: {{prettifyDate(this.resultData[0]._source.coverage_end_date)}}
                </p>
            </div>

            <div
                class="recommendations"
                v-if="this.recommendations">
                <div
                    class="title nhsuk-heading-m">
                    Recommended Data Sets
                </div>

                <VueSlickCarousel
                    :slidesToShow="calculateSlidesToShow"
                    :arrows="true"
                    :dots="true"
                    :centerMode="true"
                    class="recommendation-carousel">
                    <div
                        class="recommendation-container"
                        :aria-hidden="false"
                        v-for="recommendation in this.recommendations"
                        :key="recommendation._id">
                        <nhs-heading
                            class="title"
                            size="xs">
                            <a
                                :aria-hidden="false"
                                href="javascript:;"
                                v-on:click="recommendationClick(recommendation._id)">
                                {{recommendation._source.title}}
                            </a>
                        </nhs-heading>
                        <nhs-tag
                            class="source-tag"
                            v-if="recommendation._source.source">
                            {{recommendation._source.source}}
                        </nhs-tag>
                    </div>  
                </VueSlickCarousel>
            </div>
        
        </nhs-main>
    </div>
</template>


<script>
import SearchService from '../service/SearchService';
import NhsDataCatalogueItem from '../components/detailedResultItems/NhsDataCatalogueItem.vue';
import PheFingertipsItem from '../components/detailedResultItems/PheFingertipsItem.vue';
import NhsNcdrItem from '../components/detailedResultItems/NhsNcdrItem.vue';
import NhsDigitalItem from '../components/detailedResultItems/NhsDigitalItem.vue';
import MdxCubeItem from  '../components/detailedResultItems/MdxCubeItem.vue';
import HdrItem from '../components/detailedResultItems/HdrItem.vue';
import OnsItem from '../components/detailedResultItems/OnsItem.vue';

import VueSlickCarousel from 'vue-slick-carousel'
import 'vue-slick-carousel/dist/vue-slick-carousel.css'
import 'vue-slick-carousel/dist/vue-slick-carousel-theme.css'

import {
    NhsMain,
    NhsTag,
    NhsCard,
    NhsButton,
    NhsHeading
} from 'nhsuk-frontend-vue';

import Loading from 'vue-loading-overlay';

import { json2csv } from 'json-2-csv';

export default {
    name: "DetailedResultsItemView",
    components: { 
        NhsMain,
        NhsTag,
        Loading,
        NhsDataCatalogueItem,
        PheFingertipsItem,
        NhsNcdrItem,
        NhsDigitalItem,
        MdxCubeItem,
        HdrItem,
        OnsItem,
        NhsCard,
        NhsButton,
        NhsHeading,
        VueSlickCarousel
    },
    data(){
        return {
            resultData: undefined,
            resultId: this.$route.params.id,
            isLoading: true,
            resultLoadTime: new Date(),
            feedbackGiven: false,
            feedbackRelevancy: null,
            showFeedback: false,
            clickLogged: false,
            externalPageClick: false,
        }
    },
    methods: {
        toggleShowFeedback(){
            this.showFeedback = !this.showFeedback;
        },
        buttonClick(value){
            if(value == 'yes'){
                this.feedbackRelevancy = true;
            }else{
                this.feedbackRelevancy = false;
            }
            this.feedbackGiven = true;
        },
        redirect(link, target = '_blank'){
            this.externalPageClick = true;
            window.open(link, target);
        },
        async addClickLog(){
            if(!this.clickLogged){
                const object = {};
                object["user_id"] = this.$cookies.get('user_id');
                object["search_term"] = this.$cookies.get('search_term');
                object["search_time"] = this.$cookies.get('search_time');
                object["document_id"] = this.resultData[0]._id;
                object["result_rank"] = this.$cookies.get('result_rank');
                object["external_click_through"] = this.externalPageClick;
                object["detail_click_time"] = this.resultLoadTime;
                object["index_name"] = this.resultData[0]._index;
                object["details_click_through_order"] = this.$cookies.get('details_click_through_order');
                object["filters"] = this.$cookies.get('filters');
                object["feedbackResponse"] = {
                    "relevant": this.feedbackRelevancy
                };

                await SearchService.addClickLog(object);
                this.clickLogged = true;
            }
        },
        exportResults(){
            const sourceData = this.resultData.map(item => item["_source"])
            json2csv(sourceData, (err, array) => {
                this.downloadCsv(`export-${new Date().toISOString()}`, array, {expandArrayObjects: true})
            })
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
        recommendationClick(recommendationId){
            const target = '_blank';
            const link = `/detailed-view/${recommendationId}`;

            var clickThroughOrder = this.$cookies.get('details_click_through_order');
            this.$cookies.set('details_click_through_order', clickThroughOrder++);

            window.open(link, target);
        },
    },
    computed: {
        contentType(){
            return this.resultData[0]._source.contentType.toLowerCase();
        },
        calculateSlidesToShow(){
            var windowWidth = window.innerWidth;
            if(windowWidth < 600){
                return 1;
            }else if(windowWidth < 1000){
                return 2;
            }
            return 3;
        }
    },
    async mounted(){
        this.isLoading = true;
        const id = this.$route.params.id;
        this.resultData = await SearchService.lookupId(id);
        this.isLoading = false;
        console.log(this.resultData);
        if(this.resultData[0]._recommendations){
            this.recommendations = this.resultData[0]._recommendations.splice(0, 10);
        }
    },
    beforeRouteLeave(to, from , next){
        this.addClickLog();
        next();
    },
    beforeUpdate(){
        this.addClickLog();
    },
    beforeDestroy(){
        this.addClickLog();
    }
}
</script>

<style lang="postcss" scoped>

    .coverage-dates {
        color: #4c6272;
    }

    .coverage-dates p {
        font-size: 1rem;
        margin: 0;
    }

    .nhsuk-care-card {
        overflow-wrap: break-word;
    }

    .source-tag{
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .is-full-page {
        width: 100%;
        height: 100%;
    }

    .loading-background {
        position: fixed;
        width: 100vw;
        height: 100vh;
        top: 0;
        left: 0;
        overflow: hidden;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 99;
    }

    .loading-background .vld-overlay {
        background-color: transparent;
    }
    
    .vld-background {
        background-color: #000000;
        opacity: 0.5;
        width: 100%;
        height: 100%;
    }

    .vld-icon {
        text-align: center;
        position: absolute;
        top: calc(50% - 35px);
        left: calc(50% - 32px);
        color: #003087;
    }

    .feedbackBox{
        z-index: 9;
        width: 200px;
        position: fixed;
        right: 10px;
        margin: 20px 10px;
    }

    .feedbackBox .nhsuk-card__content {
        padding: 20px;
    }

    .feedbackBox .nhsuk-card__heading {
        left: -20px;
    }

    .grid-container {
        display: grid;
        grid-gap: 10px;
    }

    .grid-item {
        grid-row: 1;
    }

    .feedback-button {
        padding: 3px 16px;
    }

    .feedback-button .nhsuk-button::before {
        content: normal;
    }

    .detailed-feedback-button {
        font-size: 11pt;
    }

    .detailed-feedback-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        padding: 15% 0;
        z-index: 9999;
    }

    .detailed-feedback-modal .background {
        background-color: #333;
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100vh;
        opacity: 0.5;
    }
    
    @media only screen and (min-width: 1200px) {
        .back-button{
            position: absolute;
            top:100px;
            left: 20px;
        }

    }

    @media only screen and (max-width: 1200px) {
        .nhsuk-main-wrapper {
            margin-top: 10px;
        }

        .feedbackBox {
            right: 10px;
            bottom: 0;
        }

        .feedbackBox.showFeedbackBox {
            right: -35px;
            bottom: -210px;
        }
    }

    .recommendations {
        padding-bottom: 30px;
    }

    .recommendation-container {
        position: relative;
        border: 1px solid #d8dde0;
        padding: 32px;
        height: 250px;
    }

    .recommendation-container .title {
        overflow: hidden;
        height: calc(100% - 2rem);
    }

    .recommendation-container .source-tag {
        position: absolute;
        left: 0;
        bottom: 0;
        margin: 32px;
    }

    /* .slick-arrow{
        background: #003087;
        color: #003087 !important;
    } */
</style>

<style>
    .slick-prev:before {
        color: #003087;
    }
    .slick-next:before {
        color: #003087;
    }
    .slick-arrow:hover{
        color: #003087;
    }
</style>