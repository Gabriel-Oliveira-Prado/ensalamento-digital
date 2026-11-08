import { usePageHeaderStore } from "@/stores/header.store";
import { Bell } from "lucide-react";
import { useEffect } from "react";
import { Button } from "./ui/button";
import { SidebarTrigger } from "./ui/sidebar";

export function AdminHeader() {
    const setPageHeader = usePageHeaderStore((s) => s.setPageHeader);
    const resetPageHeader = usePageHeaderStore((s) => s.resetPageHeader);
    const metadata = usePageHeaderStore((s) => s.metadata);

    useEffect(() => {
        setPageHeader({
            shortTitle: "Ensalamento",
            spanTitle: "semanal",
            shortDescription: "Semestre 2026.2",
            spanDescription: "· alocação de turmas por dia e horário",
        });

        return () => {
            resetPageHeader();
        };
    }, [setPageHeader, resetPageHeader]);

    return (
        <header className="flex flex-1 items-center p-4 md:p-8">
            <SidebarTrigger className="-ml-2.5 md:hidden" />
            <div className="flex flex-1 items-center justify-between">
                <div className="items-left flex flex-col justify-center">
                    <h1 className="text-2xl leading-none font-bold">
                        {metadata.shortTitle} <span className="hidden md:inline">{metadata.spanTitle}</span>
                    </h1>
                    <span className="text-apoio text-xs">
                        {metadata.shortDescription}
                        <span className="hidden md:inline">{metadata.spanDescription}</span>
                    </span>
                </div>
                <Button variant="outline" size="icon" className="rounded-full">
                    <Bell />
                </Button>
            </div>
        </header>
    );
}
