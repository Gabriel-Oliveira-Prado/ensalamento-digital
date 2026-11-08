import { usePageHeaderStore } from "@/stores/header.store";
import { useEffect } from "react";

export function HomePage() {
    const setPageHeader = usePageHeaderStore((s) => s.setPageHeader);
    const resetPageHeader = usePageHeaderStore((s) => s.resetPageHeader);
    useEffect(() => {
        setPageHeader({
            shortTitle: "Ensalamento",
            spanTitle: " semanal",
            shortDescription: "Semestre 2026.2",
            spanDescription: " · alocação de turmas por dia e horário",
        });

        return () => {
            resetPageHeader();
        };
    }, [setPageHeader, resetPageHeader]);

    return <div>Home</div>;
}
