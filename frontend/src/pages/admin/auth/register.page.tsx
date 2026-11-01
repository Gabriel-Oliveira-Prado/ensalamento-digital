import { useAuthStore } from "@/stores/auth.store";
import { Navigate } from "react-router-dom";

export function RegisterPage() {
    const token = useAuthStore((s) => s.token);

    if (token) {
        return <Navigate to={"/admin"} replace />;
    }

    return <div>Registro</div>;
}
