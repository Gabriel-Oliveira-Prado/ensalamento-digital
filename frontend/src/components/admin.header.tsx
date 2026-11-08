import { Bell } from "lucide-react";
import { Button } from "./ui/button";
import { SidebarTrigger } from "./ui/sidebar";

export function AdminHeader() {
    return (
        <header className="flex flex-1 items-center p-4 md:p-8">
            <SidebarTrigger className="-ml-2.5 md:hidden" />
            <div className="flex flex-1 items-center justify-between">
                <div className="items-left flex flex-col justify-center">
                    <h1 className="text-2xl leading-none font-bold">
                        Ensalamento <span className="hidden md:inline">semanal</span>
                    </h1>
                    <span className="text-apoio text-xs">
                        Semestre 2026.2 <span className="hidden md:inline">· alocação de turmas por dia e horário</span>
                    </span>
                </div>
                <Button variant="outline" size="icon" className="rounded-full">
                    <Bell />
                </Button>
            </div>
        </header>
    );
}
