import { api } from "@/services/api";
import { useAuthStore } from "@/stores/auth.store";
import { useMutation } from "@tanstack/react-query";

export function useLogin() {
    const login = useAuthStore((s) => s.login);

    return useMutation({
        mutationFn: (data: { email: string; password: string }) =>
            api.post<{ access: string; refresh: string }>("/auth/token/", data),
        onSuccess: (res, data) => {
            const { access, refresh } = res.data;
            login({ email: data.email }, access, refresh);
        },
    });
}
