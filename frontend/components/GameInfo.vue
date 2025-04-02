<template>
  <div class="game-info">
    <h2>
      {{ game.away_team }} <span class="score">{{ game.away_score }}</span> -
      <span class="score">{{ game.home_score }}</span> {{ game.home_team }}
    </h2>
    <p class="match-status">📊 Quarter {{ game.period }}, ⏳ {{ game.clock }}</p>
    <p class="team-records">
      🏆 {{ game.home_team }}: {{ game.home_wins }}W - {{ game.home_losses }}L |
      🏆 {{ game.away_team }}: {{ game.away_wins }}W - {{ game.away_losses }}L
    </p>
  </div>
</template>

<script setup>
defineProps(["game"]);
</script>

<style scoped>
.game-info {
  text-align: center;
  background: #1e1e1e;
  padding: 15px;
  border-radius: 10px;
  border: 2px solid #ffcc00;
  width: 100%;
}
.score {
  font-size: 28px;
  font-weight: bold;
  color: #ffcc00;
}
</style>
