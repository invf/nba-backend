<template>



  <div class="page-container">
    <!-- ✅ Меню у верхньому лівому куті -->
    <header class="header">
      <button @click="toggleMenu" class="menu-button">☰</button>
      <div v-if="menuOpen" class="dropdown-menu">
        <router-link to="/" class="menu-item">🏠 Home</router-link>
        <router-link to="/quarter-stats" class="menu-item">🏀 Quarters</router-link>
        <router-link to="/main-screen" class="menu-item">📋 Rotate</router-link>
      </div>
    </header>

    <!-- ✅ Відображення ігор -->
    <main class="games-container">
      <!-- 🔹 Фонове відео -->
  <div class="video-background">
    <video autoplay muted loop class="background-video">
      <source :src="videoPath" type="video/mp4" />
    </video>
  </div>
      <div v-if="loading" class="loading">⏳ Loading games...</div>
      <div v-else-if="error" class="error">❌ {{ error }}</div>
      <div v-else-if="games.length === 0" class="no-games">❌ No games found.</div>

      <div v-else class="games-grid">
        <div v-for="game in games" :key="game.game_id" class="game-card" @click="goToGame(game.game_id)">
          <div class="team-stats">
            <h3>
              {{ game.away_team }} <span class="score">{{ game.away_score }}</span> -
              <span class="score">{{ game.home_score }}</span> {{ game.home_team }}
            </h3>
            <p class="status">📊 {{ game.status }}</p>
          </div>

          <!-- ✅ Лідери команд -->
          <div class="leaders-container">
            <div class="leader">
              <p>👤 {{ game.away_leader?.name || "N/A" }}</p>
              <p>🏀 PTS: {{ game.away_leader?.points || 0 }}</p>
              <p>🛡️ REB: {{ game.away_leader?.rebounds || 0 }}</p>
              <p>🎯 AST: {{ game.away_leader?.assists || 0 }}</p>
            </div>
            <div class="leader">
              <p>👤 {{ game.home_leader?.name || "N/A" }}</p>
              <p>🏀 PTS: {{ game.home_leader?.points || 0 }}</p>
              <p>🛡️ REB: {{ game.home_leader?.rebounds || 0 }}</p>
              <p>🎯 AST: {{ game.home_leader?.assists || 0 }}</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const games = ref([]);
const loading = ref(true);
const error = ref(null);
const menuOpen = ref(false);
let socket = null;

// ✅ Вибір відео для бекграунду (останній матч або випадковий)
const selectedGame = computed(() => (games.value.length > 0 ? games.value[0] : null));
const videoPath = computed(() => (selectedGame.value ? `/videos/${selectedGame.value.game_id}.mp4` : "/videos/default.mp4"));

// ✅ Випадаюче меню (показати/сховати)
const toggleMenu = () => {
  menuOpen.value = !menuOpen.value;
};

// ✅ Перехід на сторінку гри
const goToGame = (gameId) => {
  router.push(`/game/${gameId}`);
};

// ✅ Запит до API перед WebSocket
const fetchGames = async () => {
  try {
    const response = await fetch("https://nba-backend-p2yt.onrender.com/api/todays_games/");
    if (!response.ok) throw new Error("Failed to fetch data");
    const data = await response.json();

    if (!data.games || data.games.length === 0) {
      error.value = "No games found.";
      return;
    }

    games.value = data.games;
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchGames();
});

onUnmounted(() => {
  if (socket) socket.close();
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
/* 📌 Фонове відео */
.video-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  z-index: -1; /* Відео не перекриває елементи */
}

.background-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.5; /* Зменшено прозорість для кращої видимості контенту */
  pointer-events: none; /* Запобігає блокуванню кліків */
}

/* 📌 Основний контейнер */
.page-container {
  position: relative;
  color: white;
  min-height: 100vh;
  text-align: center;
  font-family: 'Roboto', sans-serif;
  font-size: 18px; /* Змініть на потрібне значення */
  padding-top: 50px;
  z-index: 1;
}

/* 📌 Меню */
.header {
  position: fixed;
  top: 10px;
  left: 10px;
  z-index: 1000;
}

.menu-button {
  background: rgba(40, 44, 52, 0.5);
  border: 2px solid #ffcc00;
  color: #ffcc00;
  font-size: 20px;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
}

.dropdown-menu {
  position: absolute;
  top: 40px;
  left: 0;
  background: rgba(40, 44, 52, 0.5);
  border-radius: 5px;
  width: 140px;
  padding: 5px;

}

.menu-item {
  display: block;
  padding: 8px;
  color: white;
  text-decoration: none;
  transition: 0.3s;
}

.menu-item:hover {
  background: #ffcc00;
  color: black;
}

/* 📌 Сітка ігор */
.games-container {
  padding: 20px;
}

.games-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px;
}

/* 📌 Карточка гри */
.game-card {
  background: rgba(40, 44, 52, 0.5);
  padding: 15px;
  border-radius: 10px;
  border: 2px solid #ffcc00;
  text-align: center;
  width: 280px;
  cursor: pointer;
  transition: transform 0.2s, background 0.3s;
}

.game-card:hover {
  transform: scale(1.05);
  background: rgba(255, 204, 0, 0.2);
}

/* 📌 Лідери команд */
.leaders-container {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.leader {
  background: rgba(40, 44, 52, 0);
  padding: 10px;
  border-radius: 8px;
  width: 48%;
  text-align: center;
  font-family: 'Roboto', sans-serif;
}
</style>
