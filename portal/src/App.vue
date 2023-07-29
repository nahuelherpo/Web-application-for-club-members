<script setup>
import NavbarVue from "./components/Navbar.vue";

import { useSesionStore } from "./stores/SesionStore";
import { onBeforeMount } from "vue";
import router from "./router";
import FooterVue from "./components/Footer.vue";

const sesion = useSesionStore();

onBeforeMount(() => {
  if (sesion.hasPreviosSesion()) {
    router.replace("/inicio");
  }
});
</script>

<template>
  <w-app>
    <NavbarVue />
    <div><router-view /></div>
  </w-app>
  <notifications />
  <FooterVue></FooterVue>
</template>

<style scoped>
* {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  font-weight: 500;
}
</style>
