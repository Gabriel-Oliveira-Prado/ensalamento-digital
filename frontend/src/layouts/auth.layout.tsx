import { Card } from "@/components/ui/card";
import { Outlet } from "react-router-dom";

export function AuthLayout() {
    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-100">
            <Card className="w-full max-w-md rounded-2xl bg-white p-4 shadow-lg">
                <Outlet />
            </Card>
        </div>
    );
}
