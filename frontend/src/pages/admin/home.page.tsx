import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/services/api";
import { usePageHeaderStore } from "@/stores/header.store";
import { BookOpen, CalendarClock, DoorOpen, GraduationCap, Package, Users } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const indicators = [
    {
        key: "salas",
        label: "Salas",
        endpoint: "/ensalamento/salas/",
        icon: DoorOpen,
    },
    {
        key: "recursos",
        label: "Recursos",
        endpoint: "/ensalamento/recursos/",
        icon: Package,
    },
    {
        key: "disciplinas",
        label: "Disciplinas",
        endpoint: "/ensalamento/disciplinas/",
        icon: BookOpen,
    },
    {
        key: "turmas",
        label: "Turmas",
        endpoint: "/ensalamento/turmas/",
        icon: GraduationCap,
    },
    {
        key: "horarios",
        label: "Horários",
        endpoint: "/ensalamento/horarios/",
        icon: CalendarClock,
    },
    {
        key: "usuarios",
        label: "Usuários",
        endpoint: "/usuarios/lista/",
        icon: Users,
    },
] as const;

type IndicatorKey = (typeof indicators)[number]["key"];

export function HomePage() {
    const setPageHeader = usePageHeaderStore((state) => state.setPageHeader);
    const resetPageHeader = usePageHeaderStore((state) => state.resetPageHeader);
    const [counts, setCounts] = useState<Partial<Record<IndicatorKey, number>>>({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        setPageHeader({
            shortTitle: "Ensalamento",
            spanTitle: " integrado",
            shortDescription: "Dados em tempo real",
            spanDescription: " · frontend conectado à API Django",
        });

        return () => resetPageHeader();
    }, [setPageHeader, resetPageHeader]);

    useEffect(() => {
        async function loadIndicators() {
            try {
                const responses = await Promise.all(
                    indicators.map((indicator) => api.get<unknown[]>(indicator.endpoint))
                );
                const nextCounts: Partial<Record<IndicatorKey, number>> = {};

                indicators.forEach((indicator, index) => {
                    nextCounts[indicator.key] = responses[index].data.length;
                });

                setCounts(nextCounts);
            } catch {
                setError("Não foi possível carregar os dados da API.");
            } finally {
                setLoading(false);
            }
        }

        void loadIndicators();
    }, []);

    return (
        <div className="space-y-6">
            <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
                {indicators.map((indicator) => {
                    const Icon = indicator.icon;
                    return (
                        <Card key={indicator.key} className="border-slate-200 bg-white shadow-sm">
                            <CardHeader className="flex flex-row items-center justify-between pb-2">
                                <CardTitle className="text-sm font-medium text-slate-600">{indicator.label}</CardTitle>
                                <Icon className="text-green-nassau size-5" />
                            </CardHeader>
                            <CardContent>
                                <p className="text-3xl font-bold text-slate-900">
                                    {loading ? "—" : (counts[indicator.key] ?? 0)}
                                </p>
                                <p className="mt-1 text-xs text-slate-500">registros na API</p>
                            </CardContent>
                        </Card>
                    );
                })}
            </div>

            {error ? (
                <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>
            ) : (
                <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-800">
                    API conectada. Os números acima vêm diretamente do backend.
                </div>
            )}

            <Card className="border-slate-200 bg-white shadow-sm">
                <CardHeader>
                    <CardTitle className="text-lg">Gerenciar cadastros</CardTitle>
                </CardHeader>
                <CardContent className="flex items-center justify-between gap-4">
                    <p className="text-sm text-slate-600">Cadastre e atualize os dados usados no ensalamento.</p>
                    <Link
                        to="/admin/cadastros"
                        className="bg-green-nassau rounded-md px-4 py-2 text-sm font-semibold text-white hover:opacity-85"
                    >
                        Abrir cadastros
                    </Link>
                </CardContent>
            </Card>
        </div>
    );
}
