<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios' // es una biblioteca de JavaScript que permite hacer solicitudes HTTP. Se usa comúnmente para interactuar con APIs.

const pokemons = ref([]) // Lista de pokémones
const displayedPokemons = ref([]) // Pokémon que se mostrarán en la página actual
const selectedPokemon = ref(null) // Detalles del Pokémon seleccionado
const isModalOpen = ref(false) // Controla si el modal está abierto
const currentPage = ref(0) // Página actual de Pokémon (inicialmente la primera)
const pokemonsPerPage = 9 // Número de Pokémon por página
const searchQuery = ref('') // Almacena lo que el usuario escribe en la barra de búsqueda
const filteredPokemons = ref([]) // Filtra los Pokémon según la búsqueda

// Número total de páginas
const totalPages = ref(0)

// Función para obtener la lista de pokémones
const fetchPokemons = async () => {
  try {
    const response = await axios.get('https://pokeapi.co/api/v2/pokemon?limit=1000') // Cambiar el límite para tener más opciones
    pokemons.value = response.data.results
    totalPages.value = Math.ceil(pokemons.value.length / pokemonsPerPage)
    filteredPokemons.value = pokemons.value // Inicializamos las sugerencias con todos los Pokémon
    updateDisplayedPokemons()
  } catch (error) {
    console.error('Error fetching pokemons:', error)
  }
}

// Función para actualizar los Pokémon mostrados según la página actual
const updateDisplayedPokemons = () => {
  const start = currentPage.value * pokemonsPerPage
  const end = start + pokemonsPerPage
  displayedPokemons.value = filteredPokemons.value.slice(start, end)
}

// Función para manejar la búsqueda y actualizar las sugerencias
const handleSearch = () => {
  const query = searchQuery.value.toLowerCase()
  filteredPokemons.value = query
    ? pokemons.value.filter(pokemon => pokemon.name.toLowerCase().includes(query))
    : pokemons.value
  totalPages.value = Math.ceil(filteredPokemons.value.length / pokemonsPerPage)
  currentPage.value = 0
  updateDisplayedPokemons()
}

// Función para obtener detalles de un Pokémon seleccionado
const fetchPokemonDetails = async (url) => {
  try {
    const response = await axios.get(url)
    selectedPokemon.value = response.data
    isModalOpen.value = true // Abre el modal al hacer clic
  } catch (error) {
    console.error('Error fetching pokemon details:', error)
  }
}

// Función para cambiar de página (izquierda o derecha)
const changePage = (direction) => {
  if (direction === 'next' && (currentPage.value + 1) * pokemonsPerPage < filteredPokemons.value.length) {
    currentPage.value++
    updateDisplayedPokemons()
  } else if (direction === 'prev' && currentPage.value > 0) {
    currentPage.value--
    updateDisplayedPokemons()
  }
}

// Función para cambiar a una página específica
const goToPage = (page) => {
  if (page >= 0 && page < totalPages.value) {
    currentPage.value = page
    updateDisplayedPokemons()
  }
}

// Cierra el modal
const closeModal = () => {
  isModalOpen.value = false
}

// Capitaliza la primera letra del nombre del Pokémon
const capitalizeName = (name) => {
  if (!name) return ''
  return name.charAt(0).toUpperCase() + name.slice(1)
}

// Función para obtener el ID del Pokémon a partir de la URL
const getPokemonId = (url) => {
  const id = url.split('/').slice(-2, -1)[0]
  return id
}

// Función para calcular el rango de páginas visibles (máximo 10 botones)
const getVisiblePageNumbers = () => {
  const totalButtons = 10
  const startPage = Math.max(0, currentPage.value - Math.floor(totalButtons / 2))
  const endPage = Math.min(startPage + totalButtons, totalPages.value)

  // Ajustar el rango para no dejar huecos al principio o al final
  const adjustedStartPage = Math.max(0, endPage - totalButtons)
  return Array.from({ length: endPage - adjustedStartPage }, (_, i) => adjustedStartPage + i)
}

onMounted(() => {
  fetchPokemons()
})
</script>

<template>
  <div class="pokemon-container">

    <!-- Barra de búsqueda -->
    <input
      type="text"
      v-model="searchQuery"
      @input="handleSearch"
      placeholder="Busca un Pokémon ..."
      class="search-bar"
    />

    <!-- Grid de Pokémon -->
    <div class="pokemon-grid">
      <div v-for="(pokemon, index) in displayedPokemons" :key="pokemon.name" class="pokemon-card" @click="fetchPokemonDetails(pokemon.url)">
        <img :src="'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/' + getPokemonId(pokemon.url) + '.png'" alt="Pokemon image" class="pokemon-img" />
        <p class="pokemon-name">{{ capitalizeName(pokemon.name) }}</p>
      </div>
    </div>

    <!-- Paginación -->
    <div class="pagination">
      <button class="arrow-btn" @click="changePage('prev')">←</button>

      <!-- Números de página visibles -->
      <button
        v-for="page in getVisiblePageNumbers()"
        :key="page"
        @click="goToPage(page)"
        :class="{ 'active-page': currentPage === page }"
        class="page-btn"
      >
        {{ page + 1 }}
      </button>

      <button class="arrow-btn" @click="changePage('next')">→</button>
    </div>

    <!-- Modal con la información del Pokémon seleccionado -->
    <div v-if="isModalOpen" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h2 v-if="selectedPokemon && selectedPokemon.name" v-text="capitalizeName(selectedPokemon.name)"></h2>
        <img v-if="selectedPokemon" :src="selectedPokemon.sprites.other['official-artwork'].front_default" alt="Pokemon image" class="pokemon-details-img" />
        <p><strong>Altura:</strong> {{ selectedPokemon.height }} ft</p>
        <p><strong>Peso:</strong> {{ selectedPokemon.weight }} lb.</p>
        <p><strong>Tipo: </strong>
            <span v-for="(type, index) in selectedPokemon.types" :key="index">{{ type.type.name }}&nbsp;</span>
        </p>
        <button @click="closeModal" class="close-btn">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pokemon-container {
  padding: 20px;
  text-align: center;
}

.title {
  font-size: 2rem;
  color: #42b883;
  margin-bottom: 20px;
}

.search-bar {
  padding: 10px;
  width: 80%;
  max-width: 800px;
  font-size: 1.2rem;
  margin-bottom: 20px;
  border-radius: 8px;
  border: 1px solid #ddd;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.pokemon-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 20px;
  margin-top: 20px;
}

.pokemon-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  cursor: pointer;
}

.pokemon-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.pokemon-img {
  width: 200px;
  height: 200px;
  object-fit: contain;
  margin-bottom: 10px;
}

.pokemon-name {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.arrow-btn {
  font-size: 1.5rem;
  padding: 10px 20px;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin: 0 10px;
}

.arrow-btn:hover {
  background-color: #357a53;
}

.page-btn {
  font-size: 1rem;
  padding: 10px;
  margin: 0 5px;
  background-color: #ddd;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.page-btn:hover {
  background-color: #bbb;
}

.active-page {
  background-color: #42b883;
  color: white;
  font-weight: bold;
}

/* Estilos del modal (cuadro emergente) */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  width: 350px;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.pokemon-details-img {
  width: 300px;
  height: 300px;
  object-fit: contain;
  margin-bottom: 10px;
}

.close-btn {
  background-color: #ff4747;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.close-btn:hover {
  background-color: #e43f3f;
}
</style>