import { usePageHeaderStore } from "@/stores/header.store";
import { useEffect } from "react";

export function HistoryPage() {
    const setPageHeader = usePageHeaderStore((s) => s.setPageHeader);
    const resetPageHeader = usePageHeaderStore((s) => s.resetPageHeader);

    useEffect(() => {
        setPageHeader({
            shortTitle: "Histórico",
            shortDescription: "Consulte o histórico de alterações.",
            spanDescription: "Acompanhe as alterações realizadas nas salas, horários e alocações",
        });

        return () => {
            resetPageHeader();
        };
    }, [setPageHeader, resetPageHeader]);

    return <h1>Histórico de alterações</h1>;
}
