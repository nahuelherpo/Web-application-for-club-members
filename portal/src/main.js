import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import router from "./router";
import WaveUI from "wave-ui";
import "wave-ui/dist/wave-ui.css";
import { createPinia } from "pinia";
import VueCookies from "vue-cookies";
import Notifications from "@kyvg/vue3-notification";
import axios from "axios";
const app = createApp(App);
const axios_instance = axios.create({ withCredentials: true });

new WaveUI(app, {});

app.use(VueCookies, { expires: "7d" }).use(Notifications).use(createPinia()).use(router).mount("#app");

export default axios_instance;
