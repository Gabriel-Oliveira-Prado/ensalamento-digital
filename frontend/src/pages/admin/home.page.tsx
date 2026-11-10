import { InputSelect } from "@/components/input.select";
import { Button } from "@/components/ui/button";
import {
    Pagination,
    PaginationContent,
    PaginationItem,
    PaginationNext,
    PaginationPrevious,
} from "@/components/ui/pagination";
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

    return (
        <>
            <Header />
        </>
    );
}

const blocks = [
    { label: "Todos", value: "all" },
    { label: "A", value: "a" },
    { label: "B", value: "b" },
];

const major = [
    { label: "Todos", value: "all" },
    { label: "ADS-2", value: "ads-2" },
    { label: "CC-2", value: "cc-2" },
];

const semester = [
    { label: "2026.2", value: "2026.2" },
    { label: "2027.1", value: "2027.1" },
];

function Header() {
    return (
        <div className="flex gap-3">
            <InputSelect label="Bloco:" items={blocks} defaultValue={blocks[0].value} />
            <InputSelect label="Curso:" items={major} defaultValue={major[0].value} />
            <InputSelect label="Semestre:" items={semester} defaultValue={semester[0].value} />
            <Pagination className="ml-5 w-auto">
                <PaginationContent>
                    <PaginationItem>
                        <PaginationPrevious className="border-paragrafo flex h-fit items-center justify-center rounded-full bg-white p-2.5!" />
                    </PaginationItem>
                    <span className="px-2 text-sm font-bold">26 ou a 31 out 2026</span>
                    <PaginationItem>
                        <PaginationNext className="border-paragrafo flex h-fit items-center justify-center rounded-full bg-white p-2.5!" />
                    </PaginationItem>
                </PaginationContent>
            </Pagination>
            <Button className="bg-green-nassau ml-auto h-11 w-full max-w-45 font-bold">Nova Alocação</Button>
        </div>
    );
}
