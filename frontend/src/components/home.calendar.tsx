import { Calendar } from "@/utils/date";
import { useState } from "react";
import { Item, ItemActions, ItemContent, ItemTitle } from "./ui/item";

export function HomeCalendar() {
    const [currentDate, setCurrentDate] = useState(new Date());

    const c = new Calendar(currentDate);

    return (
        <div className="mt-4.5">
            <div className="grid grid-cols-6 gap-2">
                {c.daysOfWeek.map((date, index) => {
                    const isToday = c.isToday(date);
                    const dayName = date.toLocaleDateString("pt-BR", { weekday: "short" }).replace(".", "");
                    const dayNameCapitalized = dayName.charAt(0).toUpperCase() + dayName.slice(1);
                    const dayNumber = date.getDate();

                    return (
                        <Item key={index} variant="outline" className="border-paragrafo/50 bg-white">
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
            </div>
        </div>
    );
}
