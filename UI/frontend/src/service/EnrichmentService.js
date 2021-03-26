export default {
    
    async enrichCalendarEntries(imei, date) {
        const response = await fetch(`${process.env.VUE_APP_BACKEND_URL}api/device/calendar/enrich`, {
            method: 'POST',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                imei,
                date
            })
          })
        return response.json()
    },
}