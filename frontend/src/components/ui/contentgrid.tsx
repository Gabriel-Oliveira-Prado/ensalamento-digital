import { Ellipsis } from "lucide-react";
import "../../assets/styles/grid.css"; // TODO: Adaptar o documento para Tailwind CSS

interface GridProps {
    gridData?: GridRow[];
}

interface GridRow {
    [key: string]: GridCell;
}

type GridCellArray = string[];

type GridCell = string | number | boolean | GridCellArray;

function Grid({ gridData = [] }: GridProps) {
    const borderColors: string[] = ["#0F7B7B", "#7C5CF0", "#E8603C", "#3B6FE0"]; // é loopado para dar as cores da borda no primeio elemento das linhas
    let i: number = 0; // contador

    const rows: GridCell[][] = [];

    gridData.forEach((v) => {
        // cria listas com os elementos de cada linha na grid. Deduz que os dados retirados tem colunas uniformes
        const col = [];
        for (const [, value] of Object.entries(v)) {
            col.push(value);
        }
        col.push("doticon"); // símbolo obrigatório adicionado sempre no final
        rows.push(col);
    });

    return (
        <table>
            <tr>
                {Object.keys(gridData[0] ?? {}).map((header, index) => {
                    // Lê gridData para criar colunas baseado nos atributos do json. Deduz que é uniforme
                    return <th key={index}>{header}</th>;
                })}
                <th></th>
            </tr>
            {rows.map((row, index) => {
                // Criação das linhas

                return (
                    <tr key={index}>
                        {row.map((col = "", index = 0) => {
                            // Preenchimento das linhas

                            const bColor = borderColors[i];

                            if (index == 0) {
                                // Movimenta 1 passo da lista e volta ao começo
                                if (i == 3) {
                                    i = 0;
                                }
                                i++;
                            }

                            if (col == "doticon") {
                                // substituição pelo símbolo
                                return (
                                    <td key={index}>
                                        <Ellipsis
                                            key={index}
                                            style={{ color: "#3A4A66", cursor: "pointer" }}
                                            onClick={() => {
                                                //TODO: Adicionar lista de ações para modificar o valor da linha no banco.
                                            }}
                                        ></Ellipsis>
                                    </td>
                                );
                            }

                            if (Array.isArray(col)) {
                                // Caso o conteúdo for tags, como categoria de status ou recursos (precisa vir como array)
                                return (
                                    <td key={index}>
                                        <div style={{ borderLeftColor: bColor }}>
                                            {col.map((value, index) => {
                                                const [divColor, textColor] = [
                                                    "ativo",
                                                    "confirmado",
                                                    "diurno",
                                                ].includes(value)
                                                    ? ["#D9F1EE", "#0F7B7B"]
                                                    : ["computadores", "laboratório", "noturno"].includes(value)
                                                      ? ["#EDE9FE", "#5B3FD6"]
                                                      : ["ar-cond.", "sáb"].includes(value)
                                                        ? ["rgba(59, 130, 246, .3)", "#2346A9"]
                                                        : ["inativo", "som"].includes(value)
                                                          ? ["#E8ECF2", "#4A5873"]
                                                          : ["em obra", "pendente", "conflito"].includes(value)
                                                            ? ["#FCE3DA", "#C2410C"]
                                                            : ["rgba(242, 183, 5,.2)", "#F5B800"];

                                                return (
                                                    <div
                                                        key={index}
                                                        style={{
                                                            backgroundColor: divColor,
                                                            color: textColor,
                                                        }}
                                                    >
                                                        {value}
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    </td>
                                );
                            }
                            // resultado padrão
                            return (
                                <td key={index}>
                                    <div style={{ borderLeftColor: bColor }}>{col}</div>
                                </td>
                            );
                        })}
                    </tr>
                );
            })}
        </table>
    );
}

export { Grid };
