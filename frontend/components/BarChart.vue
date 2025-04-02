<script setup>
import { defineProps } from "vue";
import { Chart, registerables } from "chart.js";
import { Bar } from "vue-chart-3";

Chart.register(...registerables);

defineProps(["chartData"]);
</script>

<template>
  <Bar :data="chartData" />
</template>
