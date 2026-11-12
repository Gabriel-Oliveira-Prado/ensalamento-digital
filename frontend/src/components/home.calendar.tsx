import { Calendar } from "@/utils/date";
import { Plus } from "lucide-react";
import { Fragment } from "react";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { Item, ItemActions, ItemContent, ItemTitle } from "./ui/item";

interface HomeCalendarProps {
    currentDate: Date;
}

const times = [
    { start: "08:20", end: "09:10" },
    { start: "09:10", end: "10:00" },
    { start: "10:00", end: "10:50" },
    { start: "10:50", end: "11:40" },
];

const allocation = [
    {
        id: 1,
        horario: {
            id: 1,
            dia: "2026-11-09",
            hora_inicio: "19:00",
            hora_fim: "20:40",
        },
        professor: {
            id: 1,
            email: "tony.stark@vingadores.edu.br",
            nome: "Tony Stark",
        },
        sala: {
            id: 1,
            capacidade: 40,
            nome: "Sala 20",
            tipo: "Sala comum",
        },
        turma: {
            id: 1,
            qtd_aluno: 35,
            ano: 2026,
            periodo: 4,
        },
        disciplina: {
            id: 1,
            nome: "Back-end",
            codigo: 101,
        },
        coordenador: {
            id: 1,
            nome: "Albus Dumbledore",
            email: "direcao@hogwarts.edu.br",
            senha: "hashed_password",
        },
    },
];

export function HomeCalendar({ currentDate }: HomeCalendarProps) {
    const c = new Calendar(currentDate);

    return (
        <div className="mt-4.5 flex-1">
            <div className="grid h-full grid-cols-[80px_repeat(6,1fr)] grid-rows-[56px_repeat(4,1fr)] gap-2">
                <div />
                {c.daysOfWeek.map((date, index) => {
                    const isToday = c.isToday(date);
                    const dayName = date.toLocaleDateString("pt-BR", { weekday: "short" }).replace(".", "");
                    const dayNameCapitalized = dayName.charAt(0).toUpperCase() + dayName.slice(1);
                    const dayNumber = date.getDate();

                    return (
                        <Item key={index} variant="outline" className="border-paragrafo/50 items-center bg-white">
                            <ItemContent>
                                <ItemTitle className="text-apoio font-bold">{dayNameCapitalized}</ItemTitle>
                            </ItemContent>
                            <ItemActions>
                                <span className={`text-lg font-bold ${isToday ? "text-green-nassau" : "text-apoio"}`}>
                                    {dayNumber}
                                </span>
                            </ItemActions>
                        </Item>
                    );
                })}
                {times.map((time) => (
                    <Fragment key={time.start}>
                        <div className="text-apoio flex flex-col pt-2 text-center text-sm font-bold">
                            <span>{time.start}</span>
                            <span className="text-apoio/60 font-normal">{time.end}</span>
                        </div>
                        {c.daysOfWeek.map(() => (
                            <EmptyCard />
                        ))}
                    </Fragment>
                ))}
            </div>
        </div>
    );
}

function EmptyCard() {
    return (
        <Button
            variant="outline"
            size="lg"
            className="border-paragrafo outline-apoio flex h-full flex-1 cursor-pointer items-center justify-center border-2 border-dashed bg-transparent hover:bg-white active:bg-white"
        >
            <Plus size={14} className="text-apoio" />
        </Button>
    );
}

function AllocationCard() {
    return (
        <Card className="border-paragrafo flex h-full flex-1 cursor-pointer items-center justify-center border-2 bg-white"></Card>
    );
}
