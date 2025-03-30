<script>
import axios from 'axios'

export default {
  data(){
    return {
      inputText: ''
    };
  },
  methods: {
    async sendData() {
      try{
        const response = await axios.post("http://127.0.0.1:8000/api/v1/simple/",{
          text: this.inputText
        });
        console.log('odpowiedz z backendu', response.data);
      }catch (err){
        console.error("Blad", err);
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
              <router-link to="/log-in" class="button is-light">Log In</router-link>

              <router-link to="/inventory" class="button is-success">
                <span class="icon"><i class="fas fa-shopping-cart"></i></span>
              </router-link>
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
