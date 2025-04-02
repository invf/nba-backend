<template>
  <div class="player-stats-container">
    <div v-if="loading" class="loading">⏳ Loading player stats...</div>
    <div v-else-if="error" class="error">❌ {{ error }}</div>

    <div v-else class="games-grid">
      <div v-for="game in games" :key="game.game_id" class="game-card">
        <!-- Заголовок з правильним форматом рахунку -->
        <h3 class="game-title">
          {{ game.away_team }} <span class="score">{{ game.away_score }}</span> -
          <span class="score">{{ game.home_score }}</span> {{ game.home_team }}
        </h3>

        <!-- Лідери команд -->
        <div class="leaders">
          <div class="leader">
            <h4>🔥 {{ game.home_team }} Leader</h4>
            <p>👤 {{ game.home_leader.name }}</p>
            <p>🏀 PTS: {{ game.home_leader.points }}</p>
            <p>🛡️ REB: {{ game.home_leader.rebounds }}</p>
            <p>🎯 AST: {{ game.home_leader.assists }}</p>
          </div>
          <div class="leader">
            <h4>🔥 {{ game.away_team }} Leader</h4>
            <p>👤 {{ game.away_leader.name }}</p>
            <p>🏀 PTS: {{ game.away_leader.points }}</p>
            <p>🛡️ REB: {{ game.away_leader.rebounds }}</p>
            <p>🎯 AST: {{ game.away_leader.assists }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

const games = ref([]);
const loading = ref(true);
const error = ref(null);
let socket = null;

const connectWebSocket = () => {
  socket = new WebSocket("ws://127.0.0.1:8001/ws/player_stats/");

  socket.onopen = () => console.log("✅ WebSocket connected to player stats");

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      console.log("📩 Player stats received:", data);

      if (!data.games || !Array.isArray(data.games)) {
        throw new Error("Invalid data format");
      }

      games.value = data.games.map(game => ({
        game_id: game.game_id,
        home_team: game.home_team,
        away_team: game.away_team,
        home_score: game.home_score,
        away_score: game.away_score,
        home_leader: game.home_leader,
        away_leader: game.away_leader
      }));

      loading.value = false;
    } catch (err) {
      console.error("❌ Error parsing WebSocket data:", err);
      error.value = "Failed to load player stats.";
    }
  };

  socket.onerror = () => {
    error.value = "WebSocket connection error.";
  };

  socket.onclose = () => {
    console.log("❌ WebSocket disconnected from player stats");
  };
};

onMounted(() => {
  connectWebSocket();
});

onUnmounted(() => {
  if (socket) {
    socket.close();
  }
});
</script>

<style scoped>
.player-stats-container {
  text-align: center;
  padding: 10px;
  background: #121212;
  color: white;
  min-height: 100vh;
}

.loading {
  font-size: 18px;
  color: #ffcc00;
}

.error {
  color: red;
  font-size: 16px;
}

/* Головна сітка: 2 ряди по 5 матчів */
.games-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-template-rows: repeat(2, auto);
  gap: 8px;
  justify-content: center;
  width: 95%;
  margin: 0 auto;
}

/* Оформлення кожного матчу */
.game-card {
  background: #1e1e1e;
  padding: 8px;
  border-radius: 6px;
  border: 1px solid #ffcc00;
  text-align: center;
  width: 200px;
  font-size: 12px;
}

/* Заголовок з рахунком */
.game-title {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 6px;
}

/* Оформлення рахунку */
.score {
  font-size: 18px;
  font-weight: bold;
  color: #ffcc00;
}

/* Лідери команд */
.leaders {
  display: flex;
  justify-content: space-around;
  margin-top: 5px;
}

.leader {
  background: #2a2a2a;
  padding: 5px;
  border-radius: 6px;
  width: 45%;
  border: 1px solid #ffcc00;
  text-align: center;
}
</style>
