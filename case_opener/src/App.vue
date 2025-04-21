<script>
import axios from 'axios'

export default {
  data(){
    return {
      isAuthenticated: false,
      username: "",
    };
  },
  mounted() {
    this.checkAuth();
  },
  methods: {
    async checkAuth() {
        try {
          const token = localStorage.getItem('token');
          const response = await axios.get('http://127.0.0.1:8000/api/v1/user', {
            // withCredentials: true
            headers: {
              'Authorization' : `Token ${token}`,
            }
          });
          this.isAuthenticated = true;
          this.username = response.data.username;
        } catch (err) {
          console.error("Błąd autoryzacji", err);
          this.isAuthenticated = false;

          localStorage.removeItem('token')
          if (err.response && err.response.status === 401) {
            this.$router.push('/log-in');
          }
        }
      },
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
    goToLogin(){
      this.$router.push('/log-in')
    }
  }
}

</script>

<template>

  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>Mini Casino</strong></router-link>
      </div>


      <div class="navbar-menu" id="navbar-menu">
        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <router-link v-if="!isAuthenticated" @click="goToLogin" class="button is-light">Log In</router-link>
              <template v-else>
                <button @click="logout" class="button is-danger">Log out</button>
                <router-link class="button is-light" to="/profile">{{ username }}</router-link>
              </template>
            </div>
          </div>

        </div>
      </div>
    </nav>
    <section class="section">
    <router-view/>
  </section>
  <footer class="footer">
      <!-- <input v-model="inputText" placeholder="wpisz cos" />
      <button @click="sendData">Wyslij</button> -->
      <p class="has-text-centered">Copyright (c) 2025</p>
  </footer>
</div>
</template>

<style lang="scss">
@import url('../node_modules/bulma');
</style>
