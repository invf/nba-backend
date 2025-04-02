<template>
    <!-- 🔹 Відео-бекграунд -->
  <div class="video-background">
    <video autoplay muted loop class="background-video left">
      <source :src="awayVideoPath" type="video/mp4" />
    </video>
    <video autoplay muted loop class="background-video right">
      <source :src="homeVideoPath" type="video/mp4" />
    </video>
  </div>

  <div class="game-stats-container">
    <!-- 🔹 Кнопка "Назад" -->
    <button class="back-button" @click="goBack">⬅ Back</button>

    <!-- 🔹 Верхній блок (команди, рахунок) -->
    <div class="score-box">
      <div class="score-container">
        <div class="team-info">
          <img :src="getTeamLogo(awayTeam.name)" class="team-logo" />
          <h2>{{ awayTeam.name }}</h2>
        </div>
        <div class="game-score">
          <span class="score">{{ awayTeam.score }}</span> - <span class="score">{{ homeTeam.score }}</span>
        </div>
        <div class="team-info">
          <img :src="getTeamLogo(homeTeam.name)" class="team-logo" />
          <h2>{{ homeTeam.name }}</h2>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading">⏳ Loading...</div>
    <div v-else-if="error" class="error">❌ {{ error }}</div>

    <!-- 🔹 Таблиця статистики -->
    <div v-else class="stats-table-box">
      <h2>📊 Detailed Statistics</h2>
      <table class="stats-table">
        <thead>
          <tr>
            <th>Team</th>
            <th>Rebounds</th>
            <th>Assists</th>
            <th>Turnovers</th>
            <th>Steals</th>
            <th>Blocks</th>
            <th>🎯 FG%</th>
            <th>🎯 3P%</th>
            <th>🎯 FT%</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><img :src="getTeamLogo(homeTeam.name)" class="small-logo" />{{ homeTeam.name }}</td>
            <td>{{ homeTeam.rebounds }}</td>
            <td>{{ homeTeam.assists }}</td>
            <td>{{ homeTeam.turnovers }}</td>
            <td>{{ homeTeam.steals }}</td>
            <td>{{ homeTeam.blocks }}</td>
            <td>{{ homeTeam.fgp }}%</td>
            <td>{{ homeTeam["3pp"] }}%</td>
            <td>{{ homeTeam.ftp }}%</td>
          </tr>
          <tr>
            <td><img :src="getTeamLogo(awayTeam.name)" class="small-logo" />{{ awayTeam.name }}</td>
            <td>{{ awayTeam.rebounds }}</td>
            <td>{{ awayTeam.assists }}</td>
            <td>{{ awayTeam.turnovers }}</td>
            <td>{{ awayTeam.steals }}</td>
            <td>{{ awayTeam.blocks }}</td>
            <td>{{ awayTeam.fgp }}%</td>
            <td>{{ awayTeam["3pp"] }}%</td>
            <td>{{ awayTeam.ftp }}%</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 🔥 Бігучий рядок з оглядом матчу -->
    <div class="ticker-wrapper">
      <div class="ticker">
        <span>{{ matchSummary }}</span>
        <span>{{ matchSummary }}</span>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();
const gameId = route.params.game_id;

const homeTeam = ref({});
const awayTeam = ref({});
const matchSummary = ref("");
const loading = ref(true);
const error = ref(null);
let socket = null;

// ✅ Функція перевірки існування відеофайлу
const checkVideoExists = async (path) => {
  try {
    const response = await fetch(path, { method: "HEAD" });
    return response.ok;
  } catch {
    return false;
  }
};

// ✅ Функція встановлення відеофайлів команд або default.mp4
const awayVideoPath = ref("/videos/default.mp4");
const homeVideoPath = ref("/videos/default.mp4");

const setVideoPaths = async () => {
  if (awayTeam.value.name && homeTeam.value.name) {
    const awayPath = `/videos/${awayTeam.value.name}.mp4`;
    const homePath = `/videos/${homeTeam.value.name}.mp4`;

    const [awayExists, homeExists] = await Promise.all([
      checkVideoExists(awayPath),
      checkVideoExists(homePath)
    ]);

    awayVideoPath.value = awayExists ? awayPath : "/videos/default.mp4";
    homeVideoPath.value = homeExists ? homePath : "/videos/default.mp4";
  }
};

// ✅ Функція отримання логотипу команди
const getTeamLogo = (teamName) => {
  if (!teamName) return "";
  return `/logos/${teamName.replace(/\s+/g, "_").toLowerCase()}.png`;
};

// ✅ WebSocket-з'єднання
const connectWebSocket = () => {
  socket = new WebSocket(`ws://127.0.0.1:8001/ws/game/${gameId}/`);

  socket.onopen = () => console.log("✅ WebSocket connected");

  socket.onmessage = async (event) => {
    try {
      const data = JSON.parse(event.data);
      if (!data || !data.detailed_stats || !data.detailed_stats[gameId]) {
        throw new Error(`No data found for game ${gameId}`);
      }

      const gameStats = data.detailed_stats[gameId];
      homeTeam.value = { ...gameStats.home_team };
      awayTeam.value = { ...gameStats.away_team };

      matchSummary.value = generateMatchSummary(homeTeam.value, awayTeam.value);

      await setVideoPaths(); // ✅ Перевіряємо відеофайли

      loading.value = false;
    } catch (err) {
      console.error("❌ WebSocket error:", err);
      error.value = "Error retrieving statistics.";
    }
  };

  socket.onerror = () => (error.value = "WebSocket connection error.");
  socket.onclose = () => console.log("❌ WebSocket disconnected");
};

// ✅ Функція генерації огляду матчу
const generateMatchSummary = (home, away) => {
  return `
  🏀 ${away.name} ${away.score} - ${home.score} ${home.name}

  🎯 Shooting:
  - ${away.name}: FG% ${away.fgp || 0}% | 3P% ${away["3pp"] || 0}% | FT% ${away.ftp || 0}%
  - ${home.name}: FG% ${home.fgp || 0}% | 3P% ${home["3pp"] || 0}% | FT% ${home.ftp || 0}%

  🔄 Turnovers:
  - ${away.name}: ${away.turnovers || 0}
  - ${home.name}: ${home.turnovers || 0}

  🛡️ Defense:
  - ${away.name}: Steals ${away.steals || 0} | Blocks ${away.blocks || 0}
  - ${home.name}: Steals ${home.steals || 0} | Blocks ${home.blocks || 0}

  📊 Rebounds:
  - ${away.name}: Total ${away.rebounds || 0} | Offensive ${away.offensive_rebounds || 0} | Defensive ${away.defensive_rebounds || 0}
  - ${home.name}: Total ${home.rebounds || 0} | Offensive ${home.offensive_rebounds || 0} | Defensive ${home.defensive_rebounds || 0}

  🎯 Assists:
  - ${away.name}: ${away.assists || 0}
  - ${home.name}: ${home.assists || 0}
  `;
};


// ✅ Повернення на головну
const goBack = () => router.push("/");

onMounted(() => connectWebSocket());
onUnmounted(() => socket && socket.close());
</script>



<style scoped>
.loading {
  font-size: 18px;
  color: #ffcc00;
}

.error {
  color: red;
  font-size: 16px;
}

/* 📌 Video Background */
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
  opacity: 0.7;
}

/* 📌 Statistics Container */
.game-stats-container {
  text-align: center;
  font-family: Arial, sans-serif;
  font-size: 24px; /* ✅ Збільшує розмір шрифту */
  padding: 20px;
  color: white;
  position: relative;
  z-index: 1;
}



/* 📌 Бігучий рядок (Ticker) */


.ticker-wrapper {
  position: fixed;
  bottom: 0;
  left: 0; /* 🔹 Забираємо відступ зліва */
  width: 100%;
  background: rgba(0, 0, 0, 0.5); /* 👈 Прозорий фон */
  color: #ffcc00;
  overflow: hidden;
  white-space: nowrap;
  padding: 20px 0;
}

.ticker-wrapper {
  position: fixed;
  bottom: 0;
  width: 100%;
  background: rgba(0, 0, 0, 0.6);
  overflow: hidden;
  white-space: nowrap;
  padding: 15px;
  font-size: 24px; /* ✅ Збільшує розмір шрифту */
}

.ticker {
  display: flex;
  animation: tickerAnimation 30s linear infinite;
}

@keyframes tickerAnimation {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}



/* 📌 Верхній блок (Score) */
.score-box {
  background: rgba(0, 0, 0, 0.7);
  padding: 15px;
  border-radius: 12px;
  margin-bottom: 20px;
  width: 70%;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
  border: 2px solid #ffcc00;
}

.score-container {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 28px;
}

.team-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 200px;
}

.team-logo {
  width: 80px;
  height: auto;
  margin-bottom: 5px;
}

.game-score {
  font-size: 40px;
  font-weight: bold;
  margin: 0 20px;
}

/* 📌 Таблиця статистики */
.stats-table-box {
  background: rgba(40, 44, 52, 0.9);
  padding: 20px;
  border-radius: 12px;
  border: 2px solid #ffcc00;
}

.stats-table {
  width: 100%;
  border-collapse: collapse;
  color: white;
}

.stats-table th, .stats-table td {
  padding: 10px;
  border: 1px solid white;
  text-align: center;
}

.small-logo {
  width: 40px;
  height: auto;
  vertical-align: middle;
  margin-right: 5px;
}

/* 📌 Блоки лідерів */
.leader-box {
  background: rgba(40, 44, 52, 0.9);
  padding: 15px;
  border-radius: 12px;
  width: 180px;
  text-align: center;
}

.back-button {
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(0, 0, 0, 0.1);
  padding: 10px;
  border-radius: 5px;
  border: 2px solid #ffcc00;
  cursor: pointer;
}
</style>
