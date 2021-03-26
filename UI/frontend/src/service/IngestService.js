export default {
    
    async submitIngest(params) {
        const headers = {
            'Content-Type': 'application/json'
        };
        Object.entries(params).map(([k,v]) => {
            headers[`form-upload-${k}`] = v;
        });
        const response = await fetch(`${process.env.VUE_APP_BACKEND_URL}api/upload`, {
            method: 'POST',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers,
            body: JSON.stringify({...params})
          })
        if(response.status !== 200){
            throw new Error()
        }
    },

    async submitFile(file, caseId) {
        const headers = {
            'form-upload-case_id': caseId
        };
        const form = new FormData();
        form.append('file', file)
        form.append('case_id', caseId)
        const response = await fetch(`${process.env.VUE_APP_BACKEND_URL}api/upload/file`, {
            method: 'POST',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers,
            body: form
          })
        if(response.status !== 200){
            throw new Error()
        }
    },

    async getIngestFiles() {
        const response = await fetch(`${process.env.VUE_APP_BACKEND_URL}api/upload`)
        return response.json()
    },

    async getCaseIDs() {
        const response = await fetch(`${process.env.VUE_APP_BACKEND_URL}api/cases`)
        return response.json()
    },
}
