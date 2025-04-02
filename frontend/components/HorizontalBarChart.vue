<script setup>
import { defineProps } from "vue";
import { Chart } from "vue-chart-3";

defineProps(["chartData"]);
</script>

<template>
  <Chart type="bar" :data="chartData" :options="{ indexAxis: 'y' }" />
</template>
