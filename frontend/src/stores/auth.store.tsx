import { create } from "zustand";

// Registra e apaga usuário da memória local.

type User = {
    email: string;
};

interface AuthStore {
    user: User | null;
    access: string | null;
    refresh: string | null;
    login: (user: User, token: string, refresh: string) => void;
    logout: () => void;
}

const currentAccess = localStorage.getItem("access");
const currentRefresh = localStorage.getItem("refresh");

export const useAuthStore = create<AuthStore>((set) => ({
    user: null,
    access: currentAccess || null,
    refresh: currentRefresh || null,
    login: (user, access, refresh) => {
        localStorage.setItem("access", access);
        localStorage.setItem("refresh", refresh);
        set({ user, access, refresh });
    },
    logout: () => {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        set({ user: null, access: null, refresh: null });
    },
}));
