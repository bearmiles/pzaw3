<script>
import axios from 'axios'

export default{
    data() {
        return {
            isAuthenticated: true,
            skinsArray: [],
            listDataString: String,
            username: "",
        };
    },
    mounted(){
        this.fetchSkins();
        this.checkAuth();
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
        async checkAuth() {
        try {
          const token = localStorage.getItem('token');
          const response = await axios.get('http://127.0.0.1:8000/api/v1/user', {
            // withCredentials: true
            headers: {
              'Authorization' : `Token ${token}`,
            }
          });
        //   this.isAuthenticated = true;
        console.log("RESPONSE Z CHECKAUTH ",response.data)
          this.username = response.data.username;
        } catch (err) {
          console.error("Błąd autoryzacji", err);
        //   this.isAuthenticated = false;

        //   localStorage.removeItem('token')
          if (err.response && err.response.status === 401) {
            this.$router.push('/log-in');
          }
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
                this.skinsArray = this.skinsArray.reverse();
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
        <!-- <button @click="getData" class="button is-light">getData</button>
        <button @click="fetchSkins" class="button is-ghost">Fetch skins</button> -->
        <br><br><br>
        <h1 class="title has-text-centered">Skiny uzytkownika: <h1 class=" title has-text-success"> {{ username }}</h1></h1>

        <br><br><br><br><br><br>
        <!-- wyswietlanie skinow uzytkownika -->
         <div class="grid is-gap-6 is-col-min-12">
            <div class="cell" v-for="(skin, index) in skinsArray" :key="index">
                <div class="box">
                    <p>Skin: <strong>{{ skin.skin_name }}</strong></p>
                    <br>
                    <p>Rarity: <strong>{{ skin.rarity }}</strong></p>
                </div>
                
            </div>
         </div>
            <!-- <div class="box" v-for="(skin, index) in skinsArray" :key="index">
                <p>Skin: <strong>{{ skin.skin_name }}</strong></p>
                <p>Rarity: <strong>{{ skin.rarity }}</strong></p>
            </div> -->

            <!-- <li v-for="(skin, index) in skinsArray" :key="index">
                Skin: {{ skin.skin_name }} - Rarity: {{ skin.rarity }}
            </li> -->


        
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
<style scoped>
.chuj{
    color: red;
    text-align: center;
}
</style>