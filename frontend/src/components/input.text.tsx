import { cn } from "cn";
import type { InputHTMLAttributes } from "react";
import { Controller, type Control, type FieldValues, type Path, type RegisterOptions } from "react-hook-form";
import { Field, FieldError, FieldLabel } from "./ui/field";
import { Input } from "./ui/input";

interface InputTextProps<T extends FieldValues> extends InputHTMLAttributes<HTMLInputElement> {
    name: Path<T>;
    control: Control<T>;
    label: string;
    id: string;
    rules?: Omit<RegisterOptions<T, Path<T>>, "valueAsNumber" | "valueAsDate" | "setValueAs" | "disabled"> | undefined;
}

export function InputText<T extends FieldValues>({
    name,
    control,
    label,
    id,
    rules,
    placeholder,
    className,
    children,
}: InputTextProps<T>) {
    return (
        <Controller
            name={name}
            control={control}
            rules={rules}
            render={({ field, fieldState }) => (
                <Field data-invalid={fieldState.invalid}>
                    <FieldLabel className="text-black-nassau font-bold" htmlFor={id}>
                        {label}
                    </FieldLabel>
                    <div className="relative">
                        <Input
                            className={cn("bg-foreground-nassau border-paragrafo h-11.5", className)}
                            {...field}
                            aria-invalid={fieldState.invalid}
                            id={id}
                            placeholder={placeholder}
                        ></Input>
                        {children}
                    </div>
                    {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
                </Field>
            )}
        ></Controller>
    );
}
