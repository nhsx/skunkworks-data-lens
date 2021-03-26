export default {
    async logout(){
        const response = await fetch(`${process.env.VUE_APP_BACKEND_URL}auth/logout`)
        return response.json()
    }
}