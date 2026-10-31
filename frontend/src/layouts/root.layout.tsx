import { Toaster } from "@/components/ui/toast";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Outlet } from "react-router-dom";

const queryClient = new QueryClient();

export function RootLayout() {
    return (
        <QueryClientProvider client={queryClient}>
            <Outlet />
            <Toaster />
        </QueryClientProvider>
    );
}
