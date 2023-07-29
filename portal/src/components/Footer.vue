<template>
  <footer class="pa2">
    <div class="container">
      <h2 class="text-white">{{ info }}</h2>
    </div>
  </footer>
</template>

<script setup>
import { onBeforeMount, ref } from "vue";
import allUrl from "../services/apiUrl";
import axios from "axios";
const info = ref("...");
onBeforeMount(() => {
  axios.get(allUrl.infoContacto).then((response) => {
    info.value = response.data.contacto;
  });
});
</script>

<style scoped>
.pa2 {
  padding: 10px;
}
.text-white {
  color: white;
}
footer {
  background-color: #234781;
}
</style>
