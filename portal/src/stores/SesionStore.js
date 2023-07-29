import { defineStore } from "pinia";
import VueCookies from "vue-cookies";
import router from "../router";
export const useSesionStore = defineStore("SesionData", {
  state: () => ({
    isLoged: false,
    jwt: undefined,
  }),
  getters: {
    actualJwt(state) {
      return state.jwt;
    },
    isLogedIn(state) {
      return state.isLoged;
    },
  },
  actions: {
    login(newJwt) {
      this.isLoged = true;
      this.jwt = newJwt;
      VueCookies.set("jwt", newJwt);
      router.replace("/inicio");
    },
    hasPreviosSesion() {
      const oldJwt = VueCookies.get("jwt");
      if (oldJwt) {
        this.isLoged = true;
        this.jwt = oldJwt;
      } else {
        return false;
      }
      return true;
    },
    logout() {
      router.replace("/");
      VueCookies.remove("jwt");
      this.isLoged = false;
      this.jwt = undefined;
    },
  },
});
