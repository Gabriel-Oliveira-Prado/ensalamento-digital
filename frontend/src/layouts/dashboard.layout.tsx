import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarGroup,
    SidebarGroupLabel,
    SidebarHeader,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
    SidebarProvider,
    SidebarRail,
} from "@/components/ui/sidebar";
import { ArrowLeftRight, Calendar, Clock, LayoutGrid, type LucideIcon } from "lucide-react";
import { Link, Outlet, useLocation } from "react-router-dom";

interface menuItemsType {
    to: "" | "cadastros" | "solicitacoes" | "historico";
    label: "Ensalamento" | "Cadastros" | "Solicitações" | "Histórico";
    icon: LucideIcon;
}

const menuItems: menuItemsType[] = [
    {
        to: "",
        label: "Ensalamento",
        icon: Calendar,
    },
    {
        to: "cadastros",
        label: "Cadastros",
        icon: LayoutGrid,
    },
    {
        to: "solicitacoes",
        label: "Solicitações",
        icon: ArrowLeftRight,
    },
    {
        to: "historico",
        label: "Histórico",
        icon: Clock,
    },
];

export function DashboardLayout() {
    return (
        <SidebarProvider>
            <AppSidebar />
            <main>
                <Outlet />
            </main>
        </SidebarProvider>
    );
}

function AppSidebar() {
    const location = useLocation();

    return (
        <Sidebar>
            <SidebarHeader className="bg-blue-nassau" />
            <SidebarContent className="bg-blue-nassau">
                <SidebarGroup>
                    <SidebarGroupLabel className="text-apoio">Administração</SidebarGroupLabel>
                    <SidebarMenu>
                        {menuItems.map((item) => {
                            const Icon = item.icon;
                            const path = location.pathname.split("/")[2];

                            const isActive = path === item.to;

                            return (
                                <SidebarMenuItem key={item.label}>
                                    <SidebarMenuButton
                                        isActive={isActive}
                                        render={
                                            <Link
                                                to={`./${item.to}`}
                                                className="group flex h-11 data-active:bg-white/15"
                                            >
                                                <div className="group-data-active:bg-gold-nassau h-6 w-1 rounded-full bg-transparent"></div>
                                                <Icon
                                                    className="text-paragrafo group-data-active:text-white"
                                                    strokeWidth={2.5}
                                                />
                                                <span className="text-paragrafo text-sm font-normal group-data-active:font-bold group-data-active:text-white">
                                                    {item.label}
                                                </span>
                                            </Link>
                                        }
                                    ></SidebarMenuButton>
                                </SidebarMenuItem>
                            );
                        })}
                    </SidebarMenu>
                </SidebarGroup>
                <SidebarGroup />
            </SidebarContent>
            <SidebarFooter className="bg-blue-nassau" />
            <SidebarRail />
        </Sidebar>
    );
}
