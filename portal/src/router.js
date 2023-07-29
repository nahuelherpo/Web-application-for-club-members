import { createRouter, createWebHistory } from "vue-router";
import Login from "./components/Login.vue";
import Home from "./components/Home.vue";
import DisciplinesList from "./components/DisciplinesList.vue";
import ViewPayments from "./components/ViewPayments.vue";
import Estats from "./components/Estats/Stats.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/inicio", component: Home },
  { path: "/login", component: Login },
  { path: "/disciplines", component: DisciplinesList },
  { path: "/view-payments", component: ViewPayments },
  { path: "/estadisticas", component: Estats },
];

const history = createWebHistory();

const router = createRouter({
  history,
  routes,
});

export default router;
