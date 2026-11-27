import { create } from "zustand";

// Registra e apaga usuário da memória local.

type User = {
    email: string;
};

interface AuthStore {
    user: User | null;
    token: string | null;
    login: (user: User, token: string) => void;
    logout: () => void;
}

const currentToken = localStorage.getItem("token");

export const useAuthStore = create<AuthStore>((set) => ({
    user: null,
    token: currentToken || null,
    login: (user, token) => {
        localStorage.setItem("token", token);
        set({ user, token });
    },
    logout: () => {
        localStorage.removeItem("token");
        set({ user: null, token: null });
    },
}));
