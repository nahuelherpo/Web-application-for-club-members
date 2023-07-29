<template>
  <div>
    <w-select :items="disciplines" label="Disciplinas" v-model="selected"> </w-select>
  </div>

  <template v-if="isSelected && !noData">
    <w-flex wrap class="text-center pa3">
      <div class="xs6 pa1">
        <div class="py3"><Pie class="char" :chart-data="charData" /></div>
      </div>
      <div class="xs6 pa1">
        <div class="py3"><Line class="char" :chart-data="charDataDos" /></div>
      </div>
    </w-flex>
  </template>
  <h3 v-if="noData">No tenemos inscriptos en la disciplina</h3>
</template>

<script setup>
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  LineElement,
  PointElement,
} from "chart.js";
import { Pie, Line } from "vue-chartjs";
import LoaderVue from "../Loader.vue";
import allUrl from "../../services/apiUrl";
import axios from "axios";
import { onMounted } from "vue";
import { useSesionStore } from "../../stores/SesionStore";
import { ref, watch } from "vue";

const isSelected = ref(false);
const noData = ref(false);
const charDataDos = ref({});
const charData = ref({
  labels: ["Activos", "No activos"],
  datasets: [
    {
      backgroundColor: ["#41B883", "#E46651"],
      data: [1, 20],
    },
  ],
});
const sesion = useSesionStore();
const disciplines = ref([]);
const selected = ref();
let config = {
  headers: {
    Authorization: `Bearer ${sesion.jwt.data}`,
  },
};

const handleLoadDisciplines = async () => {
  const { data } = await axios.get(allUrl.allDisciplines, config);
  disciplines.value = data.map((element) => {
    const ret = {
      label: element.name,
      value: element.id,
    };
    return ret;
  });
};
onMounted(() => {
  handleLoadDisciplines();
});

watch(selected, (newSelected) => {
  isSelected.value = true;
  noData.value = false;
  handleLoadStatsDisciplines(newSelected);
});

const handleLoadStatsDisciplines = async (newSelected) => {
  const { data } = await axios.get(`${allUrl.disciplinesStats}?discipline=${newSelected}`, config);
  if (data.femenino == 0 && data.masculino == 0 && data.otro == 0) {
    noData.value = true;
  }
  charData.value = {
    labels: ["Femenino", "Masculino", "Otros"],
    datasets: [
      {
        backgroundColor: ["#E080F0", "#6095F7", "#EEEBE8"],
        data: [data.femenino, data.masculino, data.otro],
      },
    ],
  };

  const mapedData = data.edades.map((e, i) => {
    const r = { edad: i, cantidad: e };
    return r;
  });
  const filterData = mapedData.filter((e) => e.cantidad > 0);

  charDataDos.value = {
    labels: filterData.map((e) => `${e.edad} años`),
    datasets: [
      {
        label: "Cantidad",
        backgroundColor: "#f87979",
        data: filterData.map((e) => e.cantidad),
      },
    ],
  };
};

ChartJS.register(
  Title,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement,
  PointElement,
  LineElement
);
</script>

<style scoped>
.char {
  width: 40%;
  margin: auto;
}
</style>
