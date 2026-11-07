import { useAuthStore } from "@/stores/auth.store";
import { Navigate, Outlet } from "react-router-dom";

export function ProtectedRoute() {
    const token = useAuthStore((s) => s.token);

    if (!token) {
        return <Navigate to="/admin/auth" />;
    }

    return <Outlet />;
}
