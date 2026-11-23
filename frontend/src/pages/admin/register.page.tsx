import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { api } from "@/services/api";
import { usePageHeaderStore } from "@/stores/header.store";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";
import { Pencil, Plus, Trash2, X } from "lucide-react";
import { useEffect, useMemo, useState, type FormEvent } from "react";

type ApiRecord = { id: number } & Record<string, string | number>;

type FieldConfig = {
    name: string;
    label: string;
    type?: "text" | "number" | "date" | "time";
};

type EntityConfig = {
    key: string;
    label: string;
    endpoint: string;
    fields: FieldConfig[];
};

const entities: EntityConfig[] = [
    {
        key: "recursos",
        label: "Recursos",
        endpoint: "/ensalamento/recursos/",
        fields: [{ name: "nome", label: "Nome" }],
    },
    {
        key: "salas",
        label: "Salas",
        endpoint: "/ensalamento/salas/",
        fields: [
            { name: "nome", label: "Nome" },
            { name: "capacidade", label: "Capacidade", type: "number" },
            { name: "tipo", label: "Tipo" },
        ],
    },
    {
        key: "disciplinas",
        label: "Disciplinas",
        endpoint: "/ensalamento/disciplinas/",
        fields: [{ name: "nome", label: "Nome" }],
    },
    {
        key: "turmas",
        label: "Turmas",
        endpoint: "/ensalamento/turmas/",
        fields: [
            { name: "qtd_aluno", label: "Quantidade de alunos", type: "number" },
            { name: "ano", label: "Ano", type: "number" },
            { name: "periodo", label: "Período", type: "number" },
        ],
    },
    {
        key: "horarios",
        label: "Horários",
        endpoint: "/ensalamento/horarios/",
        fields: [
            { name: "dia", label: "Dia", type: "date" },
            { name: "hora_inicio", label: "Início", type: "time" },
            { name: "hora_fim", label: "Fim", type: "time" },
        ],
    },
];

function emptyForm(config: EntityConfig) {
    return Object.fromEntries(config.fields.map((field) => [field.name, ""]));
}

export function RegisterPage() {
    const setPageHeader = usePageHeaderStore((state) => state.setPageHeader);
    const resetPageHeader = usePageHeaderStore((state) => state.resetPageHeader);
    const [selectedKey, setSelectedKey] = useState(entities[0].key);
    const [form, setForm] = useState<Record<string, string>>(() => emptyForm(entities[0]));
    const [editingId, setEditingId] = useState<number | null>(null);
    const [saving, setSaving] = useState(false);
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");

    const config = useMemo(() => entities.find((entity) => entity.key === selectedKey) ?? entities[0], [selectedKey]);
    const {
        data: records = [],
        isLoading: loading,
        isError: queryFailed,
        refetch,
    } = useQuery({
        queryKey: ["cadastros", config.endpoint],
        queryFn: async () => (await api.get<ApiRecord[]>(config.endpoint)).data,
    });

    const [mockpage, setmockpage] = useState("blocos");
    const [checkboxSelections, setCheckboxSelections] = useState<Record<string, boolean[]>>({});

    useEffect(() => {
        setPageHeader({
            shortTitle: "Cadastros",
            shortDescription: "Registre e edite informações",
            spanDescription: " diretamente na API",
        });

        return () => resetPageHeader();
    }, [setPageHeader, resetPageHeader]);

    function changeEntity(entity: EntityConfig) {
        setSelectedKey(entity.key);
        setForm(emptyForm(entity));
        setEditingId(null);
        setMessage("");
        setError("");
    }

    function cancelEditing() {
        setEditingId(null);
        setForm(emptyForm(config));
        setError("");
    }

    function startEditing(record: ApiRecord) {
        const values = Object.fromEntries(config.fields.map((field) => [field.name, String(record[field.name] ?? "")]));
        setForm(values);
        setEditingId(record.id);
        setMessage("");
        setError("");
    }

    async function submit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault();
        setSaving(true);
        setError("");
        setMessage("");

        const payload = Object.fromEntries(
            config.fields.map((field) => [
                field.name,
                field.type === "number" ? Number(form[field.name]) : form[field.name],
            ])
        );

        try {
            if (editingId) {
                await api.patch(`${config.endpoint}${editingId}/`, payload);
                setMessage("Registro atualizado com sucesso.");
            } else {
                await api.post(config.endpoint, payload);
                setMessage("Registro criado com sucesso.");
            }

            setEditingId(null);
            setForm(emptyForm(config));
            await refetch();
        } catch (requestError) {
            const responseData = axios.isAxiosError(requestError) ? requestError.response?.data : null;
            setError(responseData ? JSON.stringify(responseData) : "Não foi possível salvar o registro.");
        } finally {
            setSaving(false);
        }
    }

    async function remove(record: ApiRecord) {
        if (!window.confirm(`Excluir o registro ${record.id}?`)) return;

        setError("");
        setMessage("");

        try {
            await api.delete(`${config.endpoint}${record.id}/`);
            setMessage("Registro excluído com sucesso.");
            await refetch();
        } catch {
            setError("Não foi possível excluir. O registro pode estar sendo usado em outro cadastro.");
        }
    }

    return (
        <div className="space-y-5">
            <div className="flex flex-wrap gap-2">
                {entities.map((entity) => (
                    <Button
                        key={entity.key}
                        type="button"
                        variant={entity.key === selectedKey ? "default" : "outline"}
                        className={entity.key === selectedKey ? "bg-green-nassau hover:bg-green-nassau/85" : ""}
                        onClick={() => changeEntity(entity)}
                    >
                        {entity.label}
                    </Button>
                ))}
            </div>

            <div className="grid gap-5 xl:grid-cols-[360px_1fr]">
                <Card className="h-fit border-slate-200 bg-white shadow-sm">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2 text-lg">
                            {editingId ? <Pencil className="size-5" /> : <Plus className="size-5" />}
                            {editingId ? "Editar" : "Novo"} {config.label.toLowerCase()}
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <form className="space-y-4" onSubmit={submit}>
                            {config.fields.map((field) => (
                                <label
                                    key={field.name}
                                    className="block space-y-1.5 text-sm font-medium text-slate-700"
                                >
                                    <span>{field.label}</span>
                                    <Input
                                        required
                                        min={field.type === "number" ? 0 : undefined}
                                        type={field.type ?? "text"}
                                        value={form[field.name] ?? ""}
                                        onChange={(event) =>
                                            setForm((current) => ({
                                                ...current,
                                                [field.name]: event.target.value,
                                            }))
                                        }
                                    />
                                </label>
                            ))}

                            <div className="flex gap-2 pt-2">
                                <Button
                                    disabled={saving}
                                    type="submit"
                                    className="bg-green-nassau hover:bg-green-nassau/85 flex-1"
                                >
                                    {saving ? "Salvando..." : "Salvar"}
                                </Button>
                                {editingId && (
                                    <Button type="button" variant="outline" onClick={cancelEditing}>
                                        <X className="size-4" />
                                    </Button>
                                )}
                            </div>
                        </form>
                    </CardContent>
                </Card>

                <Card className="border-slate-200 bg-white shadow-sm">
                    <CardHeader>
                        <CardTitle className="text-lg">{config.label} cadastrados</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                        {message && <p className="rounded-md bg-emerald-50 p-3 text-sm text-emerald-700">{message}</p>}
                        {(error || queryFailed) && (
                            <p className="rounded-md bg-red-50 p-3 text-sm text-red-700">
                                {error || "Não foi possível carregar os registros."}
                            </p>
                        )}

                        {loading ? (
                            <p className="py-8 text-center text-sm text-slate-500">Carregando...</p>
                        ) : records.length === 0 ? (
                            <p className="py-8 text-center text-sm text-slate-500">Nenhum registro cadastrado.</p>
                        ) : (
                            <div className="overflow-x-auto rounded-lg border border-slate-200">
                                <table className="w-full text-left text-sm">
                                    <thead className="bg-slate-50 text-slate-600">
                                        <tr>
                                            <th className="px-4 py-3 font-semibold">ID</th>
                                            {config.fields.map((field) => (
                                                <th key={field.name} className="px-4 py-3 font-semibold">
                                                    {field.label}
                                                </th>
                                            ))}
                                            <th className="px-4 py-3 text-right font-semibold">Ações</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-slate-100">
                                        {records.map((record) => (
                                            <tr key={record.id} className="hover:bg-slate-50">
                                                <td className="px-4 py-3 text-slate-500">{record.id}</td>
                                                {config.fields.map((field) => (
                                                    <td key={field.name} className="px-4 py-3 text-slate-800">
                                                        {String(record[field.name] ?? "—")}
                                                    </td>
                                                ))}
                                                <td className="px-4 py-3">
                                                    <div className="flex justify-end gap-1">
                                                        <Button
                                                            size="icon-sm"
                                                            variant="ghost"
                                                            onClick={() => startEditing(record)}
                                                        >
                                                            <Pencil className="size-4" />
                                                        </Button>
                                                        <Button
                                                            size="icon-sm"
                                                            variant="ghost"
                                                            className="text-red-600 hover:text-red-700"
                                                            onClick={() => void remove(record)}
                                                        >
                                                            <Trash2 className="size-4" />
                                                        </Button>
                                                    </div>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
