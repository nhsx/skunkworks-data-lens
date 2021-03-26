import { categoriseKeywordResults} from '../service/DeviceDataService';

export default {
    getOperationData: async function(operation){
        const OP_DATA_URL = `${process.env.VUE_APP_BACKEND_URL}api/operations/${operation}`;
        const data = await fetch(OP_DATA_URL);
        return await data.json();
    },

    getOperationLocations: async function(operation){
        const OP_LOCATION_URL = `${process.env.VUE_APP_BACKEND_URL}api/operations/locations/${operation}`; 
        const data = await fetch(OP_LOCATION_URL);
        return await data.json();
    },

    getOperationKeywords: async function(operation, keywords) {
        let keywordMatches = [];
        for (let keyword of keywords)  {
            const OP_KEYWORD_SEARCH_URL = `${process.env.VUE_APP_BACKEND_URL}api/operations/${operation}/keyword/`
            const data = await fetch(OP_KEYWORD_SEARCH_URL + keyword)
            const response = await data.json()
    
            keywordMatches.push(categoriseKeywordResults(response, keyword))
        }
        return keywordMatches
      },
}
