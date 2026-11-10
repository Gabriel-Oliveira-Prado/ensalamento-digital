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
                    <div className="px-4 pb-6 sm:px-6 lg:px-8">
                        <Outlet />
                    </div>
                </main>
            </SidebarInset>
        </SidebarProvider>
    );
}
