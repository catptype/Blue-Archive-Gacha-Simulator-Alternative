<script setup lang="ts">
import { ref, onMounted } from 'vue';

// Define a TypeScript interface for the gacha item.
// This gives you type safety and autocompletion!
interface GachaItem {
  item_name: string;
  rarity: string;
}

// Create a reactive variable to hold the gacha result.
// It can be a GachaItem or null if no item has been pulled yet.
const lastPull = ref<GachaItem | null>(null);
const isLoading = ref(false);
const errorMessage = ref<string | null>(null);

// This function will be called when the button is clicked.
// 'async' allows us to use 'await' for the network request.
const performGachaPull = async () => {
  isLoading.value = true;
  errorMessage.value = null;
  lastPull.value = null;

  try {
    // Fetch data from your FastAPI backend.
    // Make sure your backend server is running!
    const response = await fetch('http://127.0.0.1:8000/api/gacha/pull');

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    // The 'await response.json()' part automatically parses the JSON
    // and we tell TypeScript it should match our GachaItem interface.
    const data: GachaItem = await response.json();
    lastPull.value = data;

  } catch (error) {
    console.error('There was a problem with the fetch operation:', error);
    errorMessage.value = 'Failed to fetch gacha result. Is the backend server running?';
  } finally {
    isLoading.value = false;
  }
};

// You can also trigger a pull when the component first loads
// by using onMounted, but for a gacha, a button click is better.
// onMounted(() => {
//   performGachaPull();
// });
</script>

<template>
  <div class="gacha-container">
    <header>
      <h1>Gacha Simulator</h1>
      <p>Powered by FastAPI + Vue 3 with TypeScript</p>
    </header>

    <main>
      <button @click="performGachaPull" :disabled="isLoading">
        {{ isLoading ? 'Pulling...' : 'Pull a Character!' }}
      </button>

      <div class="result-display">
        <!-- Show an error message if something went wrong -->
        <div v-if="errorMessage" class="error">
          <p>{{ errorMessage }}</p>
        </div>

        <!-- Show loading state -->
        <div v-if="isLoading" class="loading">
          <p>Contacting the server...</p>
        </div>
        
        <!-- Show the result of the last pull -->
        <div v-if="lastPull" class="item-card">
          <h2>You got a new item!</h2>
          <p class="item-name">{{ lastPull.item_name }}</p>
          <p class="item-rarity" :class="lastPull.rarity.toLowerCase()">
            Rarity: {{ lastPull.rarity }}
          </p>
        </div>

        <!-- Show a message if no pull has been made yet -->
        <div v-if="!lastPull && !isLoading && !errorMessage">
          <p>Click the button to try your luck!</p>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.gacha-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 20px;
  font-family: sans-serif;
  text-align: center;
  background-color: #f4f4f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

header h1 {
  color: #333;
}

button {
  background-color: #42b883;
  color: white;
  border: none;
  padding: 15px 30px;
  font-size: 1.2em;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #36a374;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.result-display {
  margin-top: 30px;
  padding: 20px;
  background-color: #fff;
  border-radius: 5px;
  min-height: 150px;
}

.item-card .item-name {
  font-size: 1.5em;
  font-weight: bold;
  color: #35495e;
}

.item-card .item-rarity {
  font-style: italic;
}

.item-rarity.ssr {
  color: #ffb800; /* Gold for SSR */
  font-weight: bold;
}

.error {
  color: #d8000c;
  background-color: #ffdddd;
  padding: 10px;
  border-radius: 5px;
}
</style>