import { defineStore } from "pinia";

interface State {
  token: string | null;
  role: string | null;
  userId: number | null;
}

export const useAuth = defineStore("auth", {
  state: (): State => ({
    token: localStorage.getItem("access_token"),
    role: localStorage.getItem("role"),
    userId: localStorage.getItem("userId") ? parseInt(localStorage.getItem("userId")!) : null,
  }),

  actions: {
    login(token: string) {
      try {
        const base64Url = token.split(".")[1];
        const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
        const payload = JSON.parse(atob(base64));
        console.log("Декодированный payload:", payload);
        
        this.token = token;
        this.userId = payload.user_id;
        this.role = payload.role;
        
        localStorage.setItem("access_token", token);
        localStorage.setItem("userId", this.userId?.toString() || "");
        localStorage.setItem("role", this.role || "");
      } catch (error) {
        console.error("Ошибка при декодировании токена:", error);
        this.token = token;
        localStorage.setItem("access_token", token);
      }
    },

    setRole(role: string) {
      this.role = role;
      localStorage.setItem("role", role);
    },



    logout() {
      this.token = null;
      this.role = null;
      this.userId = null;
      localStorage.removeItem("access_token");
      localStorage.removeItem("role");
      localStorage.removeItem("userId");
    },

    init() {
      const token = localStorage.getItem("access_token");
      const role = localStorage.getItem("role");
      const userId = localStorage.getItem("userId");
      
      if (token) {
        this.token = token;
        this.role = role;
        this.userId = userId ? parseInt(userId) : null;
      }
    },
  },
});
