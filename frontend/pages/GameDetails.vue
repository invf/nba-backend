<template>
  <div class="game-container">
    <h1>Game Details</h1>
    <p v-if="loading">⏳ Loading game details...</p>
    <p v-else-if="error">❌ {{ error }}</p>

    <div v-else>
      <h2>{{ game.away_team }} {{ game.away_score }} - {{ game.home_score }} {{ game.home_team }}</h2>
      <p>Status: {{ game.status }}</p>
      <p>Game Time: {{ formatGameTime(game.game_time) }}</p>

      <h3>Top Players</h3>
      <p>🏀 {{ game.home_leader.name }} - PTS: {{ game.home_leader.points }}, REB: {{ game.home_leader.rebounds }}, AST: {{ game.home_leader.assists }}</p>
      <p>🏀 {{ game.away_leader.name }} - PTS: {{ game.away_leader.points }}, REB: {{ game.away_leader.rebounds }}, AST: {{ game.away_leader.assists }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const game_id = ref(route.params.game_id);
const game = ref(null);
const loading = ref(true);
const error = ref(null);

const fetchGameDetails = async () => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/game/${game_id.value}/`);
    if (!response.ok) throw new Error("Failed to fetch game details");
    game.value = await response.json();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

// 🔄 Перезапуск запиту, якщо зміниться ID матчу
watch(() => route.params.game_id, fetchGameDetails);

onMounted(fetchGameDetails);

const formatGameTime = (utcTime) => {
  const date = new Date(utcTime);
  return date.toLocaleString("en-US", { timeZone: "America/New_York" });
};
</script>

<style scoped>
.game-container {
  text-align: center;
  padding: 20px;
  background: #121212;
  color: white;
  min-height: 100vh;
}
</style>
