import { usePageHeaderStore } from "@/stores/header.store";
import { ArrowRight, ChevronDown } from "lucide-react";
import { useEffect } from "react";
import "../../assets/styles/history.css"; //<<< css está aqui!!!

export function HistoryPage() {
    const setPageHeader = usePageHeaderStore((s) => s.setPageHeader);
    const resetPageHeader = usePageHeaderStore((s) => s.resetPageHeader);

    useEffect(() => {
        setPageHeader({
            shortTitle: "Histórico",
            shortDescription: "Consulte o histórico de alterações.",
            spanDescription: "Acompanhe as alterações realizadas nas salas, horários e alocações",
        });

        return () => {
            resetPageHeader();
        };
    }, [setPageHeader, resetPageHeader]);
    return (
        <div className="historyMain">
            <div className="filtering">
                <input name="search" placeholder="Busque por turma, professor, ou sala." type="text" id="busca" />

                <div className="filter">
                    Período: 30 dias <ChevronDown className="chevron" />
                </div>
                <div className="filter">
                    Alterado por: todos <ChevronDown className="chevron" />
                </div>
                <div className="export">Exportar CSV</div>
            </div>

            <table className="historyTable">
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
                        <div className="salas">
                            <div className="sala1">sala1</div>
                            <ArrowRight />
                            <div className="sala2">sala2</div>
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
                        <div className="salas">
                            <div className="sala1">sala1</div>
                            <ArrowRight className="icon" />
                            <div className="sala2">sala2</div>
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
                        <div className="salas">
                            <div className="sala1">sala1</div>
                            <ArrowRight />
                            <div className="sala2">sala2</div>
                        </div>
                    </td>
                    <td>Fulano</td>
                    <td>Ciclano</td>
                    <td>isso e aquilo</td>
                    <td>enviado/não enviado</td>
                </tr>
            </table>

            <div className="pageChange">
                <button>Anterior</button>
                <button>Próximo</button>
            </div>

            <p className="count"> Mostrando 3 de 12 </p>
        </div>
    );
}
