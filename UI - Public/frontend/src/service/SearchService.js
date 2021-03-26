export default {

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
}