import { usePageHeaderStore } from "@/stores/header.store";
import { useEffect } from "react";

export function HistoryPage() {
    const setPageHeader = usePageHeaderStore((s) => s.setPageHeader);
    const resetPageHeader = usePageHeaderStore((s) => s.resetPageHeader);

    useEffect(() => {
        setPageHeader({
            shortTitle: "Histórico",
            shortDescription: "ammmmm",
            spanDescription: "sei la",
        });

        return () => {
            resetPageHeader();
        };
    }, [setPageHeader, resetPageHeader]);

    return <h1>am tu e lok kkkkk</h1>;
}