<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>Case Opener</strong></router-link>
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
    <router-view/>
</div>
</template>

<style lang="scss">
@import url('../node_modules/bulma');
</style>
