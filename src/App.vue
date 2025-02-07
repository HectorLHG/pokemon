<script setup>
import PokemonList from './components/PokemonList.vue'
</script>

<template>
  <h1 class="title">App para buscar Pokemones</h1>
  <PokemonList />
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.title {
  font-size: 4rem;
  color: #42b883;
  margin-bottom: 20px;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
