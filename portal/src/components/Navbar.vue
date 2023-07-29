<template>
  <nav>
    <w-toolbar shadow class="py1">
      <router-link to="/">
        <img src="/img/logo_club.png" class="logo" alt="logo club" />
      </router-link>
      <div class="spacer"></div>

      <w-button @click="openDrawer = true" outline> Menú </w-button>
      <w-divider vertical class="mx2"></w-divider>
      <w-button bg-color="error" @click="handleCloseSesion()" lg v-if="sesion.isLoged">Cerrar sesión</w-button>

      <router-link to="/login">
        <w-button lg v-if="sesion.isLoged == false"> Ingresar</w-button>
      </router-link>
    </w-toolbar>
  </nav>
  <w-drawer v-model="openDrawer" class="blockd">
    <div class="blockd w">
      <h2 class="pa2">
        <p @click="openDrawer = false">x</p>
      </h2>
      <template v-if="sesion.isLoged">
        <router-link class="nav-link pa5" to="/inicio">Inicio</router-link>

        <w-divider class="ma6 w"></w-divider>
        <router-link class="nav-link pa5" to="/estadisticas">Estadísticas</router-link>
        <w-divider class="ma6 w"></w-divider>
        <router-link class="nav-link pa5" to="/view-payments">Mis pagos</router-link>
        <w-divider class="ma6 w"></w-divider>
      </template>

      <router-link class="nav-link pa5" to="/disciplines">Disciplinas</router-link>
      <w-divider class="ma6 w"></w-divider>
    </div>
  </w-drawer>
</template>

<script setup>
import { useSesionStore } from "../stores/SesionStore";
import { ref } from "vue";
const sesion = useSesionStore();
const handleCloseSesion = () => {
  sesion.logout();
};
const openDrawer = ref(false);
</script>

<style scoped>
.logo {
  width: 50px;
}
.w {
  width: 100%;
}
.blockd {
  display: block;
}
.btn {
  padding: 17px;
}
.nav-link {
  color: rgb(100, 98, 98);
}
.nav-link:hover {
  color: black;
}
</style>
