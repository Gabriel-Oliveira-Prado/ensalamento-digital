import { Button } from "@/components/ui/button";
import { CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Field, FieldError, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { useAuthStore } from "@/stores/auth.store";
import { zodResolver } from "@hookform/resolvers/zod";
import { Controller, FormProvider, useForm } from "react-hook-form";
import { Navigate } from "react-router-dom";
import { z } from "zod";

const loginSchema = z.object({
    login: z
        .string("A matrícula é obrigatória")
        .min(6, "Matrícula inválida")
        .max(8, "Matrícula inválida")
        .regex(/^\d+$/, "Matrícula inválida")
        .transform((val) => val.padStart(8, "0")),
    password: z.string().min(1),
});

export function RegisterPage() {
    const token = useAuthStore((s) => s.token);

    const form = useForm<z.infer<typeof loginSchema>>({
        mode: "onChange",
        resolver: zodResolver(loginSchema),
    });

    if (token) {
        return <Navigate to={"/admin"} replace />;
    }

    return (
        <FormProvider {...form}>
            <CardHeader>
                <CardTitle>Login</CardTitle>
            </CardHeader>
            <CardContent>
                <form onSubmit={form.handleSubmit(console.log)} className="gap-2 space-y-4 py-4" id="form">
                    <Controller
                        name="login"
                        control={form.control}
                        render={({ field, fieldState }) => (
                            <Field data-invalid={fieldState.invalid}>
                                <FieldLabel htmlFor="form-login">Matrícula</FieldLabel>
                                <Input
                                    {...field}
                                    id="form-login"
                                    aria-invalid={fieldState.invalid}
                                    placeholder="Coloque sua matrícula"
                                ></Input>
                                {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
                            </Field>
                        )}
                    ></Controller>
                    <Controller
                        name="password"
                        control={form.control}
                        render={({ field }) => (
                            <Field>
                                <FieldLabel htmlFor="form-password">Senha</FieldLabel>
                                <Input
                                    {...field}
                                    id="form-password"
                                    autoComplete="current-password"
                                    type="password"
                                ></Input>
                            </Field>
                        )}
                    ></Controller>
                </form>
            </CardContent>
            <CardFooter>
                <Button type="submit" form="form" disabled={!form.formState.isValid} className="flex-1">
                    Entrar
                </Button>
            </CardFooter>
        </FormProvider>
    );
}
