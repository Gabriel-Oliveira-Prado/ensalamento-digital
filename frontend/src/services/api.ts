import { useAuthStore } from "@/stores/auth.store";
import axios from "axios";

export const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || "/api",
    timeout: 10000,
    headers: {
        "Content-Type": "application/json",
    },
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("token");

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    (error) => {
        useAuthStore.getState().logout();
        return Promise.reject(error);
    }
);

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401 && localStorage.getItem("access")) {
            useAuthStore.getState().logout();
        }

        return Promise.reject(error);
    }
);
