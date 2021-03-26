<template>
    <div>
        Logging out...
    </div>
</template>

<script>

import AuthService from "../service/AuthService"

export default {
    async mounted(){
        try{
            await AuthService.logout()
        } catch(err){
            console.log(err)
        }
        document.location.href= process.env.BASE_URL;
    }
}
</script>