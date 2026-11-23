import { Card } from "@/components/ui/card";
import { Grid } from "@/components/ui/contentgrid";
import { Input } from "@/components/ui/input";
import { usePageHeaderStore } from "@/stores/header.store";
import { cn } from "cn";
import { ChevronDown } from "lucide-react";
import { useEffect, useState } from "react";
import mockdata from "../../../mock/cadastro.json";

export function RegisterPage() {
    const setPageHeader = usePageHeaderStore((s) => s.setPageHeader);
    const resetPageHeader = usePageHeaderStore((s) => s.resetPageHeader);

    const [mockpage, setmockpage] = useState("blocos");
    const [checkboxSelections, setCheckboxSelections] = useState<Record<string, boolean[]>>({});

    useEffect(() => {
        setPageHeader({
            shortTitle: "Cadastros",
            shortDescription: "Blocos, salas, recursos, ",
            spanDescription: "cursos, disciplinas, turmas, professores e horários",
        });

        return () => {
            resetPageHeader();
        };
    }, [setPageHeader, resetPageHeader]);

    const registertable = () => {
        const model = mockdata[mockpage as keyof typeof mockdata][0];

        return (
            <div className="flex flex-col gap-3">
                {Object.entries(model).map((value, index) => {
                    const labelstyle = "text-black-nassau font-bold text-[12px] mb-3";

                    if (value[0] == "titulo") {
                        return (
                            <div key={index}>
                                <h1 className="text-[17px] font-bold">{value[1].titulo}</h1>
                                <p className="text-apoio text-[10px] font-light"> {value[1].desc}</p>
                            </div>
                        );
                    }

                    if (["text", "number"].includes(value[1].type)) {
                        return (
                            <div key={index}>
                                <h1 className={cn(labelstyle)}>{value[0]}</h1>
                                <Input
                                    type={value[1].type}
                                    placeholder={value[1].placeholder}
                                    className="border border-[#E2E8F0] bg-[#F1F5F9] p-5 text-2xl text-[#94A3B8]"
                                ></Input>
                            </div>
                        );
                    }

                    if (value[1].type == "radio") {
                        return (
                            <div key={index}>
                                <h1 className={cn(labelstyle)}>{value[0]}</h1>
                                <div className="text-black-nassau flex cursor-pointer flex-row items-center justify-between rounded-lg border border-[#E2E8F0] p-3 text-[12px] font-bold capitalize">
                                    {value[1].values[0]}
                                    <ChevronDown className="text-black-nassau" size={20}></ChevronDown>
                                </div>
                            </div>
                        );
                    }

                    if (value[1].type == "checkbox") {
                        const selectionKey = `${mockpage}:${value[0]}`;
                        const checklist = checkboxSelections[selectionKey] ?? value[1].values.map(() => false);

                        return (
                            <div key={index}>
                                <h1 className={cn(labelstyle)}>{value[0]}</h1>
                                <div className="flex flex-row gap-3">
                                    {value[1].values.map((button = "", index = 0) => {
                                        const style = checklist[index]
                                            ? "bg-green-nassau text-white border border-transparent"
                                            : "border border-paragrafo";

                                        return (
                                            <button
                                                className={cn(style + " rounded-2xl p-1 px-3 text-[12px]")}
                                                onClick={() => {
                                                    setCheckboxSelections((current) => ({
                                                        ...current,
                                                        [selectionKey]: checklist.map((selected, itemIndex) =>
                                                            itemIndex === index ? !selected : selected
                                                        ),
                                                    }));
                                                }}
                                                key={index}
                                            >
                                                {button}
                                            </button>
                                        );
                                    })}
                                </div>
                                <p className="text-apoio mt-3 text-[12px] font-light">{value[1].placeholder}</p>
                            </div>
                        );
                    }
                })}

                <div className="flex flex-row gap-3">
                    <button className="text-black-nassau border-paragrafo w-34 cursor-pointer rounded-lg border p-3.5 px-0 font-bold">
                        cancelar
                    </button>
                    <button className="bg-green-nassau flex-1 cursor-pointer rounded-lg border border-transparent p-3.5 px-0 font-bold text-white">
                        salvar {mockpage}
                    </button>
                </div>
            </div>
        );
    };

    const menu = () => {
        return (
            <div className="border-b[#3DDE3EC] flex h-10 flex-row border-b">
                {Object.keys(mockdata).map((page, index) => {
                    let style = "cursor-pointer w-23 capitalize border-b-3 text-sm";

                    if (mockpage == page) {
                        style += " font-bold border-b-green-nassau";
                    } else {
                        style += " text-[#5B6B88] border-b-transparent";
                    }

                    return (
                        <button className={cn(style)} key={index} onClick={() => setmockpage(page)}>
                            {page}
                        </button>
                    );
                })}
            </div>
        );
    };

    return (
        <div className="mb-4 w-full px-8 ring-0">
            {menu()}
            <div className="mt-8 flex flex-row gap-8">
                <Card className="flex-2 ring-0">
                    <div className="flex flex-row gap-5 px-5">
                        <Input
                            placeholder={"Buscar " + mockpage}
                            className="bg-foreground-nassau w-60 p-5 text-[#8A97AE]"
                        ></Input>
                        <button className="flex w-40 cursor-pointer flex-row items-center justify-center rounded-lg border border-[#DDE3EC] px-3 text-[12px] font-bold text-[#0F1F3D]">
                            Categoria: Todas
                            <ChevronDown className="ml-auto" size={20}></ChevronDown> {/*TODO: Codificar um filtro*/}
                        </button>
                        <button className="bg-green-nassau ml-auto cursor-pointer rounded-lg px-6 text-[13px] text-white">
                            Novo elemento {/*TODO: Modificar o conteúdo dependendo do código*/}
                        </button>
                    </div>
                    <Grid gridData={mockdata[mockpage as keyof typeof mockdata].slice(1) as never[]} />
                </Card>
                <Card className="flex-1 px-6 ring-0">{registertable()}</Card>
            </div>
        </div>
    );
}
