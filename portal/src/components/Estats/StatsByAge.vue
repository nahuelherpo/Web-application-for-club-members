<template>
  <Loader :show="loading" />
  <template v-if="!loading">
    <Line class="char" :chart-data="chartData" />
  </template>
</template>

<script setup>
import { Line } from "vue-chartjs";
import Loader from "../Loader.vue";
import axios from "axios";
import allUrl from "../../sevices/apiUrl";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  CategoryScale,
} from "chart.js";
import { onBeforeMount, onMounted, ref } from "vue";
import { useSesionStore } from "../../stores/SesionStore";

const sesion = useSesionStore();
const { activos, noActivos } = defineProps(["activos", "noActivos"]);
const loading = ref(true);
let chartData = ref([]);
onBeforeMount(() => {
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

const handleLoadStats = async () => {
  let config = {
    headers: {
      Authorization: `Bearer ${sesion.jwt.data}`,
    },
  };
  const { data } = await axios.get(allUrl.statsAge, config);
  const mapedData = data.map((e, i) => {
    const r = { edad: i, cantidad: e };
    return r;
  });
  const filterData = mapedData.filter((e) => e.cantidad > 0);

  chartData.value = {
    labels: filterData.map((e) => `Edad ${e.edad} años`),
    datasets: [
      {
        label: "Edades",
        backgroundColor: "#f87979",
        data: filterData.map((e) => e.cantidad),
      },
    ],
  };
  loading.value = false;
};

ChartJS.register(Title, Tooltip, Legend, LineElement, LinearScale, PointElement, CategoryScale);
</script>

<style scoped>
.char {
  width: 40%;
  margin: auto;
}
</style>
