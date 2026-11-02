import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Field, FieldError, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { useAuthStore } from "@/stores/auth.store";
import { Controller, FormProvider, useForm, type UseFormReturn } from "react-hook-form";
import { Link, Navigate } from "react-router-dom";

interface Login {
    login: string;
    password: string;
}

export function LoginPage() {
    const token = useAuthStore((s) => s.token);

    const form = useForm<Login>({
        mode: "onSubmit",
    });

    if (token) {
        return <Navigate to={"/admin"} replace />;
    }

    return (
        <>
            <Sidebar />
            <AuthCard form={form} />
        </>
    );
}

import logo from "@/assets/dark.svg";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertCircle } from "lucide-react";

function Sidebar() {
    return (
        <div className="bg-blue-nassau min-h-screen flex-1">
            <div className="mx-auto flex h-full w-full max-w-130 flex-col justify-between px-8 py-16">
                <div className="w-50">
                    <img src={logo} alt="Logo uninassau branca" />
                </div>
                <div className="max-w-80 space-y-2">
                    <h1 className="font-heading text-4xl font-bold text-white">
                        Ensalamento
                        <br />
                        Digital
                    </h1>
                    <p className="text-foreground-nassau font-light">
                        Uma única fonte de verdade sobre qual turma está em qual sala.
                    </p>
                </div>
                <footer className="text-foreground-nassau text-sm">
                    &copy; 2026 Uninassau. Todos os direitos reservados.
                </footer>
            </div>
        </div>
    );
}

interface AuthCardType {
    form: UseFormReturn<Login>;
}

function AuthCard({ form }: AuthCardType) {
    const login = useAuthStore((s) => s.login);

    const onSubmit = (data: Login) => {
        // TODO apenas para teste.
        if (data.login !== "01811863" || data.password !== "123456") {
            form.setError("password", { message: "Matrícula ou senha incorretas" });
            return;
        }

        login({ login: data.login, password: data.password }, "fake-token");
        console.log(data);
    };

    return (
        <div className="flex min-h-screen flex-2 items-center justify-center">
            <Card className="w-full max-w-130 ring-0">
                <CardHeader>
                    <CardTitle className="text-blue-nassau font-semibold">Entrar</CardTitle>
                    <CardDescription className="text-apoio">Use seu login institucional.</CardDescription>
                </CardHeader>
                <CardContent>
                    {form.getFieldState("password").error && <AuthAlert />}
                    <FormProvider {...form}>
                        <form onSubmit={form.handleSubmit(onSubmit)} className="gap-2 space-y-4 py-4" id="form">
                            <Controller
                                name="login"
                                control={form.control}
                                render={({ field }) => (
                                    <Field>
                                        <FieldLabel className="text-apoio" htmlFor="form-login uppercase">
                                            Matrícula ou email institucional
                                        </FieldLabel>
                                        <Input {...field} id="form-login" placeholder="nome@uninassau.edu.br"></Input>
                                    </Field>
                                )}
                            ></Controller>
                            <Controller
                                name="password"
                                control={form.control}
                                render={({ field, fieldState }) => (
                                    <Field data-invalid={fieldState.invalid}>
                                        <FieldLabel className="text-apoio" htmlFor="form-password">
                                            Senha
                                        </FieldLabel>
                                        <Input
                                            {...field}
                                            id="form-password"
                                            aria-invalid={fieldState.invalid}
                                            autoComplete="current-password"
                                            type="password"
                                        ></Input>
                                        {fieldState.invalid && <FieldError errors={[fieldState.error]} />}
                                        <Link
                                            to="/forgot-password"
                                            className="text-apoio hover:text-sky-nassau text-xs hover:underline"
                                        >
                                            Esqueceu sua senha?
                                        </Link>
                                    </Field>
                                )}
                            ></Controller>
                        </form>
                    </FormProvider>
                </CardContent>
                <CardFooter className="flex-col bg-transparent">
                    <Button
                        type="submit"
                        form="form"
                        disabled={!form.formState.isValid}
                        className="bg-blue-nassau hover:bg-sky-nassau w-full"
                    >
                        Entrar
                    </Button>
                    <p className="text-apoio mt-1 text-xs">Não consegue entrar? Procure a coordenação do seu curso.</p>
                </CardFooter>
            </Card>
        </div>
    );
}

function AuthAlert() {
    return (
        <Alert className="border-red-nassau bg-red-nassau/5">
            <AlertCircle color="#c2012e" />
            <AlertTitle className="text-red-nassau">Não foi possível entrar</AlertTitle>
            <AlertDescription>Matrícula ou senha incorreta. Restam 4 tentativas.</AlertDescription>
        </Alert>
    );
}
