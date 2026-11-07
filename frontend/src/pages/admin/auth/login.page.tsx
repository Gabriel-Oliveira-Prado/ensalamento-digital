import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuthStore } from "@/stores/auth.store";
import { FormProvider, useForm, type UseFormReturn } from "react-hook-form";
import { Link, Navigate } from "react-router-dom";

interface Login {
    login: string;
    password: string;
}

export function LoginPage() {
    const token = useAuthStore((s) => s.token);

    const form = useForm<Login>({
        mode: "onChange",
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

function Sidebar() {
    return (
        <div className="bg-blue-nassau min-h-screen flex-1">
            <div className="mx-auto flex h-full flex-col justify-between px-16 py-16">
                <div className="space-y-16">
                    <div className="w-72">
                        <img src={logo} alt="Logo uninassau branca" />
                    </div>
                    <div className="space-y-4">
                        <div className="bg-red-nassau h-1.25 w-14 rounded-full" />
                        <div>
                            <h1 className="font-heading text-[40px] leading-none font-bold text-white">
                                Ensalamento sem conflitos.
                            </h1>
                            <h1 className="font-heading text-gold-nassau text-[40px] font-bold">
                                Todo professor na sala certa.
                            </h1>
                        </div>
                        <p className="text-foreground-nassau max-w-xl text-lg">
                            Cadastre turmas, aloque salas e acompanhe as trocas em um só lugar, com validação automática
                            de horários.
                        </p>
                    </div>
                </div>
                <footer className="text-foreground-nassau text-sm">
                    &copy; 2026 Uninassau. Todos os direitos reservados.
                </footer>
            </div>
        </div>
    );
}

import serEduLogo from "@/assets/ser_educacional.png";
import { InputText } from "@/components/input.text";
import { Eye, EyeClosed } from "lucide-react";
import { useState } from "react";

interface AuthCardType {
    form: UseFormReturn<Login>;
}

function AuthCard({ form }: AuthCardType) {
    const login = useAuthStore((s) => s.login);
    const [showPassword, setShowPassword] = useState(false);

    const onSubmit = (data: Login) => {
        // TODO apenas para teste.
        if (data.login !== "Rober" || data.password !== "123456") {
            form.setError("password", { message: "Nome ou senha incorretos" });
            return;
        }

        login({ login: data.login, password: data.password }, "fake-token");
        console.log(data);
    };

    const handleShowPassword = () => {
        setShowPassword((prev) => !prev);
    };

    return (
        <div className="bg-foreground-nassau relative flex min-h-screen flex-1 items-center justify-center">
            <div className="absolute top-16 right-0 w-32">
                <img className="object-cover" src={serEduLogo} alt="Ser Educacional Logo" />
            </div>
            <Card className="w-full max-w-125 p-8 ring-0">
                <CardHeader>
                    <CardTitle className="text-black-nassau text-2xl font-bold">Área da coordenação</CardTitle>
                    <CardDescription className="text-apoio">
                        Entre para gerenciar o ensalamento do semestre.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <FormProvider {...form}>
                        <form onSubmit={form.handleSubmit(onSubmit)} className="gap-2 space-y-4 py-4" id="form">
                            <InputText
                                name="login"
                                control={form.control}
                                label="Nome"
                                id="form-login"
                                placeholder="Digite seu nome"
                                rules={{
                                    required: true,
                                }}
                            />
                            <InputText
                                name="password"
                                control={form.control}
                                label="Senha"
                                id="form-password"
                                autoComplete="current-password"
                                placeholder="Digite sua Senha"
                                type={showPassword ? "text" : "password"}
                                rules={{
                                    required: true,
                                }}
                            >
                                <button
                                    className="text-green-nassau absolute top-1/2 right-0 -translate-y-1/2 cursor-pointer px-3"
                                    type="button"
                                    onClick={handleShowPassword}
                                >
                                    {showPassword ? <Eye /> : <EyeClosed />}
                                </button>
                            </InputText>
                        </form>
                    </FormProvider>
                    <Link
                        to="/forgot-password"
                        className="text-green-nassau hover:text-sky-nassau text-right text-xs font-semibold hover:underline"
                    >
                        Esqueceu sua senha?
                    </Link>
                    <Button
                        type="submit"
                        form="form"
                        disabled={!form.formState.isValid || form.formState.isSubmitting}
                        className="bg-green-nassau hover:bg-green-nassau/75 mt-1 h-12.5 w-full cursor-pointer"
                    >
                        Entrar
                    </Button>
                </CardContent>
                <CardFooter className="flex-col bg-transparent">
                    <p className="text-apoio text-xs">
                        Aplicativo institucional. Uso exclusivo da comunidade acadêmica.
                    </p>
                </CardFooter>
            </Card>
        </div>
    );
}
