import { defineStore } from "pinia";

interface User {
  id: string;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  role: string;
  avatar?: string;
  bio?: string;
  phone?: string;
  website?: string;
  location?: string;
  date_joined: string;
  average_rating?: number;
  total_products?: number;
  total_orders?: number;
}

interface State {
  token: string | null;
  role: string | null;
  userId: string | null;
  user: User | null;
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
        this.userId = payload.user_id?.toString() || null;
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

    setUser(user: User) {
      this.user = user;
      this.userId = user.id;
      this.role = user.role;
    },

    updateUser(userData: Partial<User>) {
      if (this.user) {
        this.user = { ...this.user, ...userData };
      }
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
        this.userId = userId;
      }
    },
  },
});
