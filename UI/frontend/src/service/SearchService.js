export default {
    filterTabs: function(activeFilter){
        this.resultsData.results = this.resultsData[activeFilter];
    },

    filterAttributes(key, val){
        this.resultsData.results = this.filterOn(this.resultsData.results, key, val);
    },
    
    filterOn(d, key, val){
        var filteredData = [];
        d.forEach(function(obj){

            if (obj && obj[key] && obj[key]==val){
                filteredData.push(obj);
            }
        });
        return filteredData;
    },

    // Methods that you need, for e.g fetching data from server etc.
   
    async fetchData(searchTerm, page, contentType, filters, userid, multiLangEnabled, exactMatch) {
        const queryObject = {
            query: searchTerm,
            page: page,
            contentType: contentType,
            filters: filters,
            exactMatch: exactMatch,
            userid: userid,
            multiLangEnabled: multiLangEnabled,
        }
        const response = await fetch(`/api/query`, {
            method: 'POST',
            cache: 'no-cache',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(queryObject)
          })

        if(response.ok){  
          const html = document.documentElement // returns the html tag
          html.setAttribute('lang', response.headers.get('Content-Language'))          
          return response.json()
        }else{
          return response;
        }
    },

    async addClickLog(info){

        const response = await fetch(`/api/clicklog`, {
            method: 'POST',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(info)
          });

        return response;
    },

    async lookupId(id) {
        const response = await fetch(`/api/search/` + id, {
            method: 'GET',
            cache: 'no-cache',
            credentials: 'same-origin'
        })
        
        return response.json()
    },

    async smsLookup(source, destination, eventTime) {
        const response = await fetch(`/api/sms/${source}/${destination}/${eventTime}`, {
            method: 'GET',
            cache: 'no-cache',
            credentials: 'same-origin'
        })
        return response.json()
    },

    async getDevices() {
        const response = await fetch(`/api/device`, {
            method: 'GET',
            cache: 'no-cache',
            credentials: 'same-origin',
          })
        return response.json()
    },

    async getExhibits() {
        const response = await fetch(`/api/exhibits`, {
            method: 'GET',
            cache: 'no-cache',
            credentials: 'same-origin',
          })
        return response.json()
    },

    async getOperations() {
        const response = await fetch(`/api/operations`, {
            method: 'GET',
            cache: 'no-cache',
            credentials: 'same-origin',
          })
        return response.json()
    },

    async getSubjectOfInterest() {
        const response = await fetch(`/api/subject-of-interest`, {
            method: 'GET',
            cache: 'no-cache',
            credentials: 'same-origin',
          })
        return response.json()
    },

    async getLocations(imei) {
        const response = await fetch(`/api/device/locations/${imei}`, {
            method: 'GET',
            cache: 'no-cache',
            credentials: 'same-origin',
          })
        return response.json()
    },


    async getLocationsForOperation(operation) {
        const response = await fetch(`/api/operations/locations/${operation}`, {
            method: 'GET',
            cache: 'no-cache',
            credentials: 'same-origin',
          })
        return response.json()
    },
    
    async customQuery(index, queryBody) {
        const response = await fetch(`/api/query/custom/${index}`, {
            method: 'POST',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(queryBody)
          })
        return response.json()
    },

    async bulkLookup(terms) {
        const response = await fetch(`/api/query/bulk`, {
            method: 'POST',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(terms)
          })
        return response.json()
    }
}