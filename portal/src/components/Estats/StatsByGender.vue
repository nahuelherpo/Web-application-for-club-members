<template>
  <!--<Bar :chart-data="chartData" class="char" />-->
  <template v-if="!loading">
    <Pie class="char" :chart-data="charDataDos"></Pie>
  </template>
</template>

<script setup>
import { Pie } from "vue-chartjs";
import allUrl from "../../sevices/apiUrl";
import axios from "axios";
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from "chart.js";
import { onMounted, ref } from "vue";
import { useSesionStore } from "../../stores/SesionStore";
const responseFemenino = ref(0);
const responseOtro = ref(0);
const responseMasc = ref(0);
const loading = ref(true);
const sesion = useSesionStore();
//const { femenino, masculino, otro } = defineProps(["femenino", "masculino", "otro"]);

const handleLoadStats = async () => {
  let config = {
    headers: {
      Authorization: `Bearer ${sesion.jwt.data}`,
    },
  };
  const { data } = await axios.get(allUrl.statsGender, config);
  responseFemenino.value = data.femenino;
  responseOtro.value = data.otro;
  responseMasc.value = data.masculino;
  loading.value = false;
};

onMounted(() => {
  try {
    handleLoadStats();
  } catch {
    notify({
      title: "Ocurrio un error",
      text: "Espere un momento y vuelta a intentar",
      type: "error",
    });
  }
});

const charDataDos = {
  labels: ["Masculino", "Femenino", "Otro"],
  datasets: [
    {
      backgroundColor: ["#6095F7", "#E080F0", "#EEEBE8"],
      data: [responseMasc, responseFemenino, responseOtro],
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
