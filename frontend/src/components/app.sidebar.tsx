import logo from "@/assets/dark.svg";
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
    SidebarRail,
} from "@/components/ui/sidebar";
import { useAuthStore } from "@/stores/auth.store";
import { ArrowLeftRight, Calendar, Clock, LayoutGrid, LogOut, type LucideIcon } from "lucide-react";
import { Link, useLocation } from "react-router-dom";
import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar";
import { Button } from "./ui/button";

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

export function AppSidebar() {
    const location = useLocation();

    return (
        <Sidebar>
            <SidebarHeader className="bg-blue-nassau p-4">
                <div className="w-full">
                    <img src={logo} alt="Logo uninassau branca" />
                </div>
            </SidebarHeader>
            <SidebarContent className="bg-blue-nassau">
                <SidebarGroup>
                    <SidebarGroupLabel className="text-apoio">Administração</SidebarGroupLabel>
                    <SidebarMenu>
                        {menuItems.map((item) => {
                            const Icon = item.icon;
                            const path = location.pathname.split("/")[2] ? location.pathname.split("/")[2] : "";

                            const isActive = path === item.to;

                            return (
                                <SidebarMenuItem key={item.label}>
                                    <SidebarMenuButton
                                        isActive={isActive}
                                        render={
                                            <Link
                                                to={`./${item.to}`}
                                                className="group flex h-11 transition-colors hover:bg-white/10 active:bg-white/15 data-active:bg-white/15"
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
            <SidebarFooter className="bg-blue-nassau p-4">
                <SidebarMenu>
                    <SidebarMenuItem>
                        <div className="flex items-center gap-2 rounded-lg bg-white/8 p-4">
                            <Avatar className="size-8">
                                <AvatarImage alt="Avatar" />
                                <AvatarFallback>CO</AvatarFallback>
                            </Avatar>
                            <div className="grid flex-1 text-left text-sm leading-tight">
                                <span className="truncate font-bold text-white">Coordenação</span>
                                <span className="text-paragrafo truncate text-xs">Secretaria acadêmica</span>
                            </div>
                            <Button variant="outline" size="icon" onClick={useAuthStore.getState().logout}>
                                <LogOut />
                            </Button>
                        </div>
                    </SidebarMenuItem>
                </SidebarMenu>
            </SidebarFooter>
            <SidebarRail />
        </Sidebar>
    );
}
