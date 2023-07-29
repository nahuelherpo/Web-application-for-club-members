<script setup>
import EstatsByAgeVue from "./StatsByAge.vue";
import StatsByGenderVue from "./StatsByGender.vue";
import allUrl from "../../sevices/apiUrl";
import StatsDisciplinesVue from "./StatsDisciplines.vue";
import axios from "axios";
import { useSesionStore } from "../../stores/SesionStore";
import StatsActiveVue from "./StatsActive.vue";
import { ref } from "vue";
import Loader from "../Loader.vue";
const sesion = useSesionStore();
const activos = ref(0);
const loading = ref(true);
const inactivos = ref(0);

const tabs = {
  tabsCount: 4,
  currentTab: 1,
};

let config = {
  headers: {
    Authorization: `Bearer ${sesion.jwt.data}`,
  },
};
try {
  axios.get(allUrl.statsAso, config).then((response) => {
    inactivos.value = response.data.noActivos;
    activos.value = response.data.activos;
    loading.value = false;
  });
  //refactor please
} catch (e) {
  notify({
    title: "Ocurrió un error",
    text: "Espere un momento y vuelta a intentar",
    type: "error",
    closeOnClick: true,
  });
}
</script>

<template>
  <div class="container mt6">
    <h2>Estadisticas del sistema</h2>
    <Loader :show="loading"></Loader>
    <w-tabs ref="tabs" :items="tabs.tabsCount" v-model="tabs.currentTab" v-if="!loading">
      <template #item-title="{ index }">
        <template v-if="index === 1">Asociados activos</template>
        <template v-if="index === 2">Asociados género</template>
        <template v-if="index === 3">Asociados edad</template>
        <template v-if="index === 4">Disciplinas</template>
      </template>

      <template #item-content="{ index }">
        <template v-if="index === 1"><StatsActiveVue :activos="activos" :noActivos="inactivos" /></template>
        <template v-if="index === 2"><StatsByGenderVue /></template>
        <template v-if="index === 3"><EstatsByAgeVue /></template>
        <template v-if="index === 4"><StatsDisciplinesVue /></template>
      </template>
    </w-tabs>
  </div>
</template>

<style scoped>
h2 {
  padding-bottom: 10px;
  padding-top: 15px;
  font-size: larger;
}
</style>
