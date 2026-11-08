import { AdminHeader } from "@/components/admin.header";
import { AppSidebar } from "@/components/app.sidebar";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { Outlet } from "react-router-dom";

export function DashboardLayout() {
    return (
        <SidebarProvider>
            <AppSidebar />
            <SidebarInset>
                <main className="bg-foreground-nassau min-h-screen">
                    <AdminHeader />
                    <Outlet />
                </main>
            </SidebarInset>
        </SidebarProvider>
    );
}
