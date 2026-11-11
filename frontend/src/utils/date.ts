export class Calendar {
    currentDate: Date;
    startOfWeek: Date;
    daysOfWeek: Date[];

    constructor(currentDate: Date) {
        this.currentDate = currentDate;
        this.startOfWeek = this.getStartOfWeek();
        this.daysOfWeek = this.getDaysOfWeek();
    }

    changeWeek(direction: number): Date {
        const newDate = new Date(this.currentDate);
        newDate.setDate(newDate.getDate() + direction * 7);
        return newDate;
    }

    getStartOfWeek(): Date {
        const startDate = new Date(this.currentDate);
        const dayOfWeek = startDate.getDay();
        startDate.setDate(startDate.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1)); // Começa na segunda
        return startDate;
    }

    isToday(date: Date): boolean {
        const today = new Date();
        return (
            date.getDate() === today.getDate() &&
            date.getMonth() === today.getMonth() &&
            date.getFullYear() === today.getFullYear()
        );
    }

    getDaysOfWeek(): Date[] {
        return Array.from({ length: 6 }, (_, i) => {
            const date = new Date(this.startOfWeek);
            date.setDate(date.getDate() + i);
            return date;
        });
    }
}
