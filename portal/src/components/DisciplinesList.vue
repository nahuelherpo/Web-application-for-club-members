<script setup>
  import axios from 'axios';
  import { ref } from "vue";
  import allUrl from '../services/apiUrl'
  import { useSesionStore } from "../stores/SesionStore";

  const sesion = useSesionStore();

  const disciplines = ref([]);

  const chbx_value = ref(false);

  const load = async () => {

    try {

      let response = await axios.get(allUrl.disciplines);

      if (!(response.status == 200)) {
        throw Error('Error occurs when loading data')
      }

      disciplines.value = response.data;

    } catch(e) {
      console.log("Failed to load data")
    }
  }

  const loadDisciplines = async () => {
    
    const chbx = chbx_value.value;

    try {

      let response = null;

      if (!chbx) {
        response = await axios.get(allUrl.disciplines);
      } else {
          response = await axios({
            method: 'get',
            url: allUrl.my_disciplines,
            headers : {
              Authorization: `Bearer ${sesion.jwt.data}`
            }
          });
      }

      if (!(response.status == 200)) {
        throw Error('Error occurs when loading data')
      }

      disciplines.value = response.data;

    } catch(e) {
      console.log("Failed to load data");
    }
  }

  load();

  function showCategories(cats) {
    let log_info = "Categorias: \n"
    cats.forEach(c => {
      log_info = log_info + c.name + " " + c.instructors + " " + c.hour_fence + " " + c.days + "\n"
    });
    alert(log_info);
  }

</script>

<template>
<div class="container">
  <h3>Listado de Disciplinas</h3>
  <w-divider horizontal class="mx2"></w-divider>
  <w-flex class="align-center">
    <w-checkbox v-model="chbx_value" v-if="sesion.isLoged" @click="loadDisciplines()">
      Mostrar solo mis disciplinas
    </w-checkbox>
  </w-flex>
  <br/>
  <li v-for="d in disciplines">
    {{ d.name }}, costo mensual: ${{ d.monthly_price }}
    <w-button @click="showCategories(d.categories)">Ver categorías</w-button>
  </li>
</div>
</template>

<style scoped>
  h3 {
    padding-top: 15px;
    padding-bottom: 15px;
    font-size: x-large;
  }
</style>
