import { useAuthStore } from "@/stores/auth.store";
import axios from "axios";

export const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    timeout: 10000,
    headers: {
        "Content-Type": "application/json",
    },
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("token");

        if (!token) {
            throw new Error();
        }

        return config;
    },
    (error) => {
        useAuthStore.getState().logout();
        return Promise.reject(error);
    }
);
