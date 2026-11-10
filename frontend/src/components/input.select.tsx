import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from "./ui/select";

interface InputSelectProps {
    label: string;
    items: { label: string; value: number | string }[];
    defaultValue: number | string | null | undefined;
}

export function InputSelect({ label, items, defaultValue }: InputSelectProps) {
    return (
        <Select items={items} defaultValue={defaultValue}>
            <SelectTrigger className="min-h-11 w-full max-w-44 bg-white">
                <span className="text-sm font-bold">{label}</span>
                <SelectValue className="text-sm font-bold" />
            </SelectTrigger>
            <SelectContent alignItemWithTrigger={false}>
                <SelectGroup>
                    {items.map((item) => (
                        <SelectItem key={item.value} value={item.value}>
                            {item.label}
                        </SelectItem>
                    ))}
                </SelectGroup>
            </SelectContent>
        </Select>
    );
}
