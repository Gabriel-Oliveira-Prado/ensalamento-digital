import { AdminHeader } from "@/components/admin.header";
import { AppSidebar } from "@/components/app.sidebar";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { Outlet } from "react-router-dom";

export function DashboardLayout() {
    return (
        <SidebarProvider>
            <AppSidebar />
            <SidebarInset>
                <div className="bg-foreground-nassau flex min-h-screen flex-col">
                    <AdminHeader />
                    <div className="flex flex-1 flex-col px-4 pb-6 sm:px-6 lg:px-8">
                        <Outlet />
                    </div>
                </div>
            </SidebarInset>
        </SidebarProvider>
    );
}
