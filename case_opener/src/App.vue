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
        const response = await axios.get('http://127.0.0.1:8000/api/v1/user', {
          withCredentials: true  // Kluczowe!
        });
          console.log('Odpowiedź z checkAuth:', response.data);
          if(response.data && response.data.username) {
            this.isAuthenticated = true;
            this.username = response.data.username;
          }
        } catch (err) {
          console.error("Błąd autoryzacji", err);
        }
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
              <router-link v-if="!isAuthenticated" to="/log-in" class="button is-light">Log In</router-link>
                <router-link v-else class="button is-light" to="/profile">{{ username }}</router-link>
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
