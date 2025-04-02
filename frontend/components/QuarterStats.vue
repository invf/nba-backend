<template>



  <div class="video-background">
    <video autoplay muted loop class="background-video">
      <source src="/videos/default.mp4" type="video/mp4">
    </video>
  </div>
  <div class="quarter-stats-container">
      <!-- 🔙 Кнопка назад -->
    <router-link to="/" class="back-button">
      <img src="/icons/back-arrow.svg" alt="Back" class="back-icon" />
    </router-link>

    <h2 class="date">📅 {{ currentDate }}</h2>
    <div v-if="loading" class="loading">⏳ Loading quarter stats...</div>
    <div v-else-if="error" class="error">❌ {{ error }}</div>

    <div v-else class="games-list">
      <div v-for="game in games" :key="game.game_id" class="game-card">
        <!-- Таблиця рахунку по чвертях -->
        <table class="quarter-scores">
          <tbody>
            <tr>
              <td class="team-name">{{ game.away_team }} ({{ game.away_wins }}/{{ game.away_losses }})</td>
              <td class="quarter-info" rowspan="2">  <p class="status">📊 {{ game.status }}</p></td>
              <td v-for="p in game.away_periods" :key="p.period" class="score-cell">{{ p.score ?? 0 }}</td>
              <td class="total-score"><strong>{{ game.away_score }}</strong></td>
              <td class="score-bar-container">
                <div class="bar home-bar" :style="{ width: getBarWidth(game.away_score) }">{{ game.away_score }}</div>
              </td>
            </tr>
            <tr>
              <td class="team-name">{{ game.home_team }} ({{ game.home_wins }}/{{ game.home_losses }})</td>
              <td v-for="p in game.home_periods" :key="p.period" class="score-cell">{{ p.score ?? 0 }}</td>
              <td class="total-score"><strong>{{ game.home_score }}</strong></td>
              <td class="score-bar-container">
                <div class="bar away-bar" :style="{ width: getBarWidth(game.home_score) }">{{ game.home_score }}</div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

const games = ref([]);
const loading = ref(true);
const error = ref(null);
const currentDate = ref(new Date().toLocaleDateString());
let socket = null;

const connectWebSocket = () => {
  socket = new WebSocket("ws://127.0.0.1:8001/ws/quarter_stats/");

  socket.onopen = () => console.log("✅ WebSocket connected to quarter stats");

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      console.log("📩 Quarter stats received:", data);

      if (!data.games || !Array.isArray(data.games)) {
        throw new Error("Invalid data format");
      }

      games.value = data.games
        .map(game => ({
          game_id: game.game_id,
          home_team: game.home_team,
          away_team: game.away_team,
          home_score: game.home_score,
          away_score: game.away_score,
          status: game.status,
          home_periods: game.home_periods || [],
          away_periods: game.away_periods || [],
          current_quarter: game.current_quarter || "-",
          time_remaining: game.time_remaining || "--:--",
          home_wins: game.home_wins ?? 0,
          home_losses: game.home_losses ?? 0,
          away_wins: game.away_wins ?? 0,
          away_losses: game.away_losses ?? 0
        }))


      loading.value = false;
    } catch (err) {
      console.error("❌ Error parsing WebSocket data:", err);
      error.value = "Failed to load quarter stats.";
    }
};


  socket.onerror = () => {
    error.value = "WebSocket connection error.";
  };

  socket.onclose = () => {
    console.log("❌ WebSocket disconnected from quarter stats");
  };
};

const getBarWidth = (score) => {
  const maxScore = Math.max(...games.value.map(game => Math.max(game.home_score, game.away_score)), 1);
  return `${(score / maxScore) * 100}%`;
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
.quarter-stats-container {
  position: relative;
  text-align: center;
    font-family: Arial, sans-serif;
  font-size: 24px; /* ✅ Збільшує розмір шрифту */
  padding: 10px;
  color: white;
  min-height: 100vh;
}

/* Контейнер для дати */
.header-container {
  display: flex;
  justify-content: flex-start;
  width: 100%;
  padding-left: 20px;
}

.date {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
  color: black;
}

.video-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  z-index: 0;
}

.background-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}


.loading {
  font-size: 18px;
  color: #ffcc00;
}

.error {
  color: red;
  font-size: 16px;
}

.games-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  width: 100%;
}

.game-card {
  background: rgba(30, 30, 30, 0.8);
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ffcc00;
  text-align: center;
  width: 100%;
  max-width: 900px;
  font-size: 14px;
}

.quarter-scores {
  width: 100%;
  margin-top: 6px;
  border-collapse: collapse;
  font-size: 14px;
}

.quarter-scores td {
  border: 1px solid #ffcc00;
  padding: 5px;
  text-align: center;
}

.team-name {
  width: 150px;
  font-weight: bold;
}

.quarter-info {
  width: 80px;
  font-weight: bold;
  color: #ffcc00;
  text-align: center;
}

.score-cell {
  width: 50px;
}

.total-score {
  width: 70px;
  font-weight: bold;
}

.score-bar-container {
  width: 250px;
}

.bar {
  height: 20px;
  text-align: center;
  font-weight: bold;
  color: black;
  background-color: #ffcc00;
  border-radius: 4px;
}

.away-bar {
  background-color: red;
}

.home-bar {
  background-color: blue;
}
.back-button {
  position: fixed;
  top: 15px;
  left: 15px;
  font-size: 28px; /* Розмір стрілки */
  text-decoration: none;
  color: white;
  background: rgba(0, 0, 0, 0.5); /* Прозорий чорний фон */
  padding: 8px 12px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: 0.3s;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.2);
}
.back-icon {
  width: 24px;
  height: 24px;
}


</style>
