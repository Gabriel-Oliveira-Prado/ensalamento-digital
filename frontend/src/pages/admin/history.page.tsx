import { usePageHeaderStore } from "@/stores/header.store";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { ArrowRight, ChevronDown } from "lucide-react";
import "../../assets/styles/history.css"; //<<< css está aqui!!!

export function HistoryPage() {
    const setPageHeader = usePageHeaderStore((s) => s.setPageHeader);
    const resetPageHeader = usePageHeaderStore((s) => s.resetPageHeader);
    const { control } = useForm();

    useEffect(() => {
        setPageHeader({
            shortTitle: "Histórico",
<<<<<<< HEAD
            shortDescription: "Quem trocou, quando, e porquê.",
=======
            shortDescription: "Consulte o histórico de alterações.",
            spanDescription: "Acompanhe as alterações realizadas nas salas, horários e alocações",
>>>>>>> 462ba35b0461be9e7d1edfa60eccd6c0246ea7fd
        });

        return () => {
            resetPageHeader();
        };
    }, [setPageHeader, resetPageHeader]);
    return (
        <div class="historyMain">
            <div class="filtering">
                <input
                    name="search"
                    control={control}
                    placeholder="Busque por turma, professor, ou sala."
                    type="text"
                    id="busca"
                />

<<<<<<< HEAD
                <div class="filter">
                    Período: 30 dias <ChevronDown class="chevron" />
                </div>
                <div class="filter">
                    Alterado por: todos <ChevronDown class="chevron" />
                </div>
                <div class="export">Exportar CSV</div>
            </div>

            <table class="historyTable">
                <tr>
                    <th>Data e hora</th>
                    <th>Turma</th>
                    <th>Troca</th>
                    <th>Professor</th>
                    <th>Alteração</th>
                    <th>Motivo</th>
                    <th>Aviso</th>
                </tr>
                <tr>
                    <td>
                        <b>10/10 | 20:20</b>
                    </td>
                    <td>Cadeira, Curso</td>
                    <td>
                        <div class="salas">
                            <div class="sala1">sala1</div>
                            <ArrowRight />
                            <div class="sala2">sala2</div>
                        </div>
                    </td>
                    <td>Fulano</td>
                    <td>Ciclano</td>
                    <td>isso e aquilo</td>
                    <td>enviado/não enviado</td>
                </tr>
                <tr>
                    <td>
                        <b>10/10 | 20:20</b>
                    </td>
                    <td>Cadeira, Curso</td>
                    <td>
                        <div class="salas">
                            <div class="sala1">sala1</div>
                            <ArrowRight class="icon" />
                            <div class="sala2">sala2</div>
                        </div>
                    </td>
                    <td>Fulano</td>
                    <td>Ciclano</td>
                    <td>isso e aquilo</td>
                    <td>enviado/não enviado</td>
                </tr>
                <tr>
                    <td>
                        <b>10/10 | 20:20</b>
                    </td>
                    <td>Cadeira, Curso</td>
                    <td>
                        <div class="salas">
                            <div class="sala1">sala1</div>
                            <ArrowRight />
                            <div class="sala2">sala2</div>
                        </div>
                    </td>
                    <td>Fulano</td>
                    <td>Ciclano</td>
                    <td>isso e aquilo</td>
                    <td>enviado/não enviado</td>
                </tr>
            </table>

            <div class="pageChange">
                <button>Anterior</button>
                <button>Próximo</button>
            </div>

            <p class="count"> Mostrando 3 de 12 </p>
        </div>
    );
=======
    return <h1>Histórico de alterações</h1>;
>>>>>>> 462ba35b0461be9e7d1edfa60eccd6c0246ea7fd
}
