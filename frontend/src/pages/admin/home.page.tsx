import { HomeCalendar } from "@/components/home.calendar";
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
import { Calendar } from "@/utils/date";
import { useEffect, useState } from "react";

export function HomePage() {
    const setPageHeader = usePageHeaderStore((s) => s.setPageHeader);
    const resetPageHeader = usePageHeaderStore((s) => s.resetPageHeader);
    const [currentDate, setCurrentDate] = useState(() => new Date());

    useEffect(() => {
        let timeoutId: number;

        const scheduleMidnightUpdate = () => {
            const now = new Date();
            const nextMidnight = new Date(now);
            nextMidnight.setHours(24, 0, 0, 0);

            timeoutId = window.setTimeout(() => {
                setCurrentDate(new Date());
                scheduleMidnightUpdate();
            }, nextMidnight.getTime() - now.getTime());
        };

        scheduleMidnightUpdate();
        return () => window.clearTimeout(timeoutId);
    }, []);

    useEffect(() => {
        setPageHeader({
            shortTitle: "Ensalamento",
            spanTitle: " integrado",
            shortDescription: "Dados em tempo real",
            spanDescription: " · frontend conectado à API Django",
        });

        return () => resetPageHeader();
    }, [setPageHeader, resetPageHeader]);

    return (
        <div className="flex flex-1 flex-col">
            <Header currentDate={currentDate} />
            <HomeCalendar currentDate={currentDate} />
        </div>
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

function Header({ currentDate }: { currentDate: Date }) {
    const calendar = new Calendar(currentDate);
    const firstDay = calendar.daysOfWeek[0];
    const lastDay = calendar.daysOfWeek.at(-1)!;
    const rangeLabel = formatDateRange(firstDay, lastDay);

    return (
        <div className="flex gap-3">
            <InputSelect label="Bloco:" items={blocks} defaultValue={blocks[0].value} />
            <InputSelect label="Curso:" items={major} defaultValue={major[0].value} />
            <InputSelect label="Semestre:" items={semester} defaultValue={semester[0].value} />
            <Pagination className="ml-5 w-auto">
                <PaginationContent>
                    <PaginationItem>
                        <PaginationPrevious className="border-paragrafo/50 flex h-fit items-center justify-center rounded-full bg-white p-2.5!" />
                    </PaginationItem>
                    <span className="px-2 text-sm font-bold">{rangeLabel}</span>
                    <PaginationItem>
                        <PaginationNext className="border-paragrafo/50 flex h-fit items-center justify-center rounded-full bg-white p-2.5!" />
                    </PaginationItem>
                </PaginationContent>
            </Pagination>
            <Button className="bg-green-nassau ml-auto h-11 w-full max-w-45 font-bold">Nova Alocação</Button>
        </div>
    );
}

function formatDateRange(startDate: Date, endDate: Date) {
    const startMonth = startDate.toLocaleDateString("pt-BR", { month: "short" }).replace(".", "");
    const endMonth = endDate.toLocaleDateString("pt-BR", { month: "short" }).replace(".", "");
    const startDay = startDate.getDate();
    const endDay = endDate.getDate();
    const startYear = startDate.getFullYear();
    const endYear = endDate.getFullYear();

    if (startYear !== endYear) {
        return `${startDay} ${startMonth} ${startYear} a ${endDay} ${endMonth} ${endYear}`;
    }

    if (startDate.getMonth() !== endDate.getMonth()) {
        return `${startDay} ${startMonth} a ${endDay} ${endMonth} ${endYear}`;
    }

    return `${startDay} a ${endDay} ${endMonth} ${endYear}`;
}
