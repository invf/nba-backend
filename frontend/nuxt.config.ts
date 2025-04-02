export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBase: "http://127.0.0.1:8000/api",
    },
  },

  // Включає автоматичну маршрутизацію Nuxt 3
  pages: true,

  compatibilityDate: "2025-02-25"
});