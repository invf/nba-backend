<template>
  <div class="quarter-container">
    <QuarterStats />
  </div>
</template>

<script setup>
import QuarterStats from "@/components/QuarterStats.vue";
</script>

<style scoped>
.quarter-container {
  text-align: center;
  padding: 20px;
  background: #121212;
  color: white;
  min-height: 100vh;
}
</style>
