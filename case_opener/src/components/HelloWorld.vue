<template>
  <div class="hello">

      <h1 class="title is-1 has-text-centered">Wybierz Giereczke</h1>
      <br>
      <br>
      <br>
    <div class="buttons are-large is-flex is-justify-content-center">
      <button class="button is-light"><RouterLink to="/cases">Cases</RouterLink></button>
      <button class="button is-hovered"><RouterLink to="/roulette">Wheel</RouterLink></button>
    </div>
    

    </div>
</template>

<script>
export default {
  name: 'HelloWorld',
}
</script>

<style scoped lang="scss">
.button:hover {
  transform: scale(1.1);
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease-in-out;
}
</style>
