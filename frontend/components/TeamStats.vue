<template>
  <div class="team-stats-container">
    <h3>📊 Team Stats</h3>
    <table class="team-stats">
      <thead>
        <tr>
          <th>Team</th>
          <th>PTS</th>
          <th>REB</th>
          <th>AST</th>
          <th>TO</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{{ game.home_team }}</td>
          <td>{{ game.home_stats.points }}</td>
          <td>{{ game.home_stats.rebounds }}</td>
          <td>{{ game.home_stats.assists }}</td>
          <td>{{ game.home_stats.turnovers }}</td>
        </tr>
        <tr>
          <td>{{ game.away_team }}</td>
          <td>{{ game.away_stats.points }}</td>
          <td>{{ game.away_stats.rebounds }}</td>
          <td>{{ game.away_stats.assists }}</td>
          <td>{{ game.away_stats.turnovers }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps(["game"]);
</script>

<style scoped>
.team-stats-container {
  text-align: center;
  margin-top: 10px;
}
.team-stats {
  width: 100%;
  margin-top: 10px;
  border-collapse: collapse;
  font-size: 14px;
}
.team-stats th,
.team-stats td {
  border: 1px solid #ffcc00;
  padding: 5px;
  text-align: center;
}
</style>
