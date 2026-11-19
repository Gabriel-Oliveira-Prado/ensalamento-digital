import { usePageHeaderStore } from "@/stores/header.store";
import { useEffect } from "react";

export function RequestPage() {
    const setPageHeader = usePageHeaderStore((s) => s.setPageHeader);
    const resetPageHeader = usePageHeaderStore((s) => s.resetPageHeader);

    useEffect(() => {
        setPageHeader({
            shortTitle: "Solicitações",
            shortDescription: "Faça demandas para",
            spanDescription: "salas específicas",
        });

        return () => {
            resetPageHeader();
        };
    }, [setPageHeader, resetPageHeader]);

    return <h1>Página de solicitações</h1>;
}