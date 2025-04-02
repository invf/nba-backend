<template>
  <div class="video-only-container">
    <video autoplay muted loop class="full-video">
      <source src="/videos/playoff.mp4" type="video/mp4" />
      Your browser does not support the video tag.
    </video>
  </div>
</template>

<script setup>
// Можна додати логіку для динамічної підстановки відео з параметра URL
</script>

<style scoped>
.video-only-container {
  margin: 0;
  padding: 0;
  background: black;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.full-video {
  width: 100%;
  height: 100%;
  object-fit: contain; /* 🔄 замість cover */
  background-color: white;
}

</style>
