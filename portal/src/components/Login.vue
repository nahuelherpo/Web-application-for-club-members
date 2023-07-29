<script setup>
import axios from "axios";
import allUrl from "../sevices/apiUrl";
import { useNotification } from "@kyvg/vue3-notification";
import { useSesionStore } from "../stores/SesionStore";
import { ref } from "vue";
import Loader from "./Loader.vue";
import axios_instance from "../main";
const { notify } = useNotification();
const sesion = useSesionStore();
const show = ref(false);
const handleSubmit = (evt) => {
  evt.preventDefault();
  const dniForm = evt.target.elements.dni.value;
  const passwordForm = evt.target.elements.password.value;

  show.value = true;
  const body = {
    user: dniForm,
    password: passwordForm,
  };
  if (dniForm.length < 1) return;
  if (passwordForm.length < 1) return;

  try {
    axios_instance
      .post(allUrl.login, body)
      .then((response) => {
        notify({
          title: "Sesion iniciada",
          text: "Sesion iniciada con exito",
          type: "success",
          closeOnClick: true,
        });
        sesion.login(response);
      })
      .catch(() =>
        notify({
          title: "Ocurrio un error",
          text: "Usuario o contraseña incorrectos",
          type: "error",
          closeOnClick: true,
        })
      )
      .finally(() => (show.value = false));
  } catch {
    notify({
      title: "Ocurrio un error",
      text: "Error del servidor",
      type: "error",
      closeOnClick: true,
    });
  }
};
</script>

<template>
  <Loader :show="show"></Loader>
  <div class="container">
    <div class="login_card mt12">
      <w-card>
        <h2>Ingresa en el club</h2>
        <w-form @submit="handleSubmit" allow-submit>
          <w-input
            class="mb4"
            name="dni"
            label="Dni"
            type="numeric"
            :validators="[(value) => !!value || 'Este campo es requerido']"
          >
          </w-input>
          <w-input
            class="mb4"
            name="password"
            label="Contraseña"
            :validators="[(value) => !!value || 'Este campo es requerido']"
          >
          </w-input>
          <w-button type="submit">Ingresar</w-button>
        </w-form>
      </w-card>
    </div>
  </div>
</template>

<style scoped>
.centered {
  align-self: center;
  width: 50%;
  padding-top: 5%;
}

.btn-login {
  padding: 2%;
  font-size: larger;
}

h2 {
  padding-bottom: 10px;
}
</style>
