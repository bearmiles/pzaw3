<script>
import axios from 'axios'

export default{
    data() {
        return {
            isAuthenticated: true,
            skinsArray: [],
            listDataString: String,
        };
    },
    mounted(){
        this.fetchSkins();
    },
    methods: {
        async logout(){
            try{
                const token = localStorage.getItem('token')
                const response = await axios.post('http://127.0.0.1:8000/api/v1/logoutt', {} ,{
                    headers: {
                        Authorization: `Token ${token}`
                    }
                });
                    console.log("odpowiedz z logoutu", response.data);
                    delete axios.defaults.headers.common['Authorization'];
                    this.isAuthenticated = false;
                    this.$router.push('/')
                    this.$root.isAuthenticated = false
            }catch (error){
                console.log("blad z wylogowywaniem", error)
            }
        },
        async getData(){
            try{
                const token = localStorage.getItem('token')
                const response = await axios.get('http://127.0.0.1:8000/api/v1/userskins', {
                    // withCredentials: true,
                    headers: {
                        Authorization: `Token ${token}`
                    }
                });
                console.log("odpowiedz z get data", response.data)
            }catch(err){
                console.log(`blad ${err}`)
            }
        },
        async fetchSkins(){
            try{
                const token = localStorage.getItem('token')
                const response = await axios.get('http://127.0.0.1:8000/api/v1/userskins', {
                    headers: {
                        Authorization: `Token ${token}`
                    }
                });
                console.log(`skiny do tokena ${token}`, response.data)

                //`````````````do wypisania
                this.listDataString = JSON.stringify(response.data, null, "\t");
                this.skinsArray = response.data
                //`````````````````

                console.log(this.skinsArray)
                return this.skinsArray
            }catch (e) {
                // thorw new Error('blad', e)
                throw new TypeError('blad w fetchskins', e)
            }
        }
    }
}
</script>
<template>
    <div>
        <button @click="logout" class="button is-danger">Log out</button>
        <button @click="getData" class="button is-light">getData</button>
        <button @click="fetchSkins" class="button is-ghost">Fetch skins</button>

        <!-- wyswietlanie skinow uzytkownika -->
        
        <ul>
            <li v-for="(skin, index) in skinsArray" :key="index">
                Skin: {{ skin.skin_name }} - Rarity: {{ skin.rarity }}
            </li>
        </ul>

        
        <!-- <textarea v-model="listDataString" rows="20" cols="80"></textarea>
            <ul id="items">
            <li v-for="(item, index) in listData" :key="index">
                {{ `${item.text} [${item.id}]` }}
            </li>
            </ul> -->
        <!-- <pre v-if="response.ok">
            {{ JSON.stringify(data, null , '\t')}}
        </pre> -->
    </div>
</template>