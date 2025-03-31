<script>
import axios from 'axios'

export default{
    data() {
        return {
            isAuthenticated: true,
        };
    },
    methods: {
        async logout(){
            try{
                const response = await axios.get('http://127.0.0.1:8000/api/v1/logoutt', {
                    withCredentials: true
                });
                console.log("odpowiedz z logoutu", response.data);
                    this.isAuthenticated = false;
                    this.$router.push('/')
                    this.$root.isAuthenticated = false
            }catch (error){
                console.log("blad z wylogowywaniem", error)
            }
        }
    }
}
</script>
<template>
    <div>
        <button @click="logout" class="button is-danger">Log out</button>
    </div>
</template>