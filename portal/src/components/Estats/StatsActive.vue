<template>
  <!--<Bar :chart-data="chartData" class="char" />-->
  <Pie class="char" :chart-data="charDataDos"></Pie>
</template>

<script setup>
import { Pie } from "vue-chartjs";
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from "chart.js";
const { activos, noActivos } = defineProps(["activos", "noActivos"]);

const charDataDos = {
  labels: ["Activos", "No activos"],
  datasets: [
    {
      backgroundColor: ["#41B883", "#E46651"],
      data: [activos, noActivos],
    },
  ],
};

ChartJS.register(Title, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement);
</script>

<style scoped>
.char {
  width: 40%;
  margin: auto;
}
</style>
