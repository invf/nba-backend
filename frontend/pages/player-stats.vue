<template>
  <div class="player-container">
    <h1>🏀 Player Stats</h1>
    <PlayerStats />
  </div>
</template>

<script setup>
import PlayerStats from "@/components/PlayerStats.vue";
</script>

<style scoped>
.player-container {
  text-align: center;
  padding: 20px;
  background: #121212;
  color: white;
  min-height: 100vh;
}
</style>
