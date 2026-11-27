import { usePageHeaderStore } from "@/stores/header.store";
import { useEffect } from "react";

export function RequestPage() {
    const setPageHeader = usePageHeaderStore((s) => s.setPageHeader);
    const resetPageHeader = usePageHeaderStore((s) => s.resetPageHeader);

    useEffect(() => {
        setPageHeader({
            shortTitle: "Solicitações de troca de sala",
            shortDescription: "Só a coordenação altera o ensalamento. Professores solicitam, você decide.",
        });

        return () => {
            resetPageHeader();
        };
    }, [setPageHeader, resetPageHeader]);

    return <h1>Essa é a tela de solicitação.</h1>;
}
