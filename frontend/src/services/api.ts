import { useAuthStore } from "@/stores/auth.store";
import axios, { type InternalAxiosRequestConfig } from "axios";

export const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || "/api",
    timeout: 10000,
    headers: {
        "Content-Type": "application/json",
    },
});

interface RetryConfig extends InternalAxiosRequestConfig {
    _retry?: boolean;
}

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("access");

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
    async (error) => {
        const originalRequest = error.config as RetryConfig;

        if (
            error.response?.status === 401 &&
            originalRequest &&
            !originalRequest._retry &&
            localStorage.getItem("access")
        ) {
            originalRequest._retry = true;

            try {
                const access = await refreshAccessToken();

                originalRequest.headers.Authorization = `Bearer ${access}`;
                return api(originalRequest);
            } catch (error) {
                useAuthStore.getState().logout();
                return Promise.reject(error);
            }
        }

        return Promise.reject(error);
    }
);

let refreshPromise: Promise<string> | null = null;

function refreshAccessToken() {
    if (!refreshPromise) {
        refreshPromise = (async () => {
            const refresh = localStorage.getItem("refresh");

            if (!refresh) {
                throw new Error("Refresh token não existe");
            }

            const { data } = await axios.post<{ access: string; refresh: string }>(
                `${api.defaults.baseURL}/auth/token/`,
                { refresh }
            );

            localStorage.setItem("access", data.access);

            if (data.refresh) {
                localStorage.setItem("refresh", data.refresh);
            }

            return data.access;
        })().finally(() => {
            refreshPromise = null;
        });

        return refreshPromise;
    }
}
