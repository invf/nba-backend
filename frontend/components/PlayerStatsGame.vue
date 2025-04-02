<template>
  <div class="players-container">
    <h3>🏀 Player Stats</h3>
    <div class="players-grid">
      <div v-for="player in game.players" :key="player.id" class="player-card">
        <p><strong>👤 {{ player.name }}</strong></p>
        <p>PTS: {{ player.points }} | REB: {{ player.rebounds }} | AST: {{ player.assists }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps(["game"]);
</script>

<style scoped>
.players-container {
  text-align: center;
  margin-top: 10px;
}
.players-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}
.player-card {
  background: #2a2a2a;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ffcc00;
  width: 150px;
  text-align: center;
}
</style>
