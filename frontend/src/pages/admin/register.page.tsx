import { usePageHeaderStore } from "@/stores/header.store";
import { useEffect } from "react";

export function RegisterPage() {
    const setPageHeader = usePageHeaderStore((s) => s.setPageHeader);
    const resetPageHeader = usePageHeaderStore((s) => s.resetPageHeader);

    useEffect(() => {
        setPageHeader({
            shortTitle: "Cadastros",
            shortDescription: "Registre e edite informações",
            spanDescription: " no nosso banco de dados",
        });

        return () => {
            resetPageHeader();
        };
    }, [setPageHeader, resetPageHeader]);

    return <h1>Página de cadastro kk</h1>;
}
