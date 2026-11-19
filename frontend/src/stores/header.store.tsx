import type { RouteHandleMetada } from "@/types/route.handles";
import { create } from "zustand";

// essa store permite criar páginas padronizadas mantendo o progresso no header 
// de navegação a esquerda da tela baseado na rota. 
// A rota chamará um arquivo que definirá os dados a serem inseridos no modelo
// para os componentes padronizados em adição a permitir preenchimento customizado adicional.

interface HeaderStore { 
    metadata: RouteHandleMetada;
    setPageHeader: (data: RouteHandleMetada) => void;
    resetPageHeader: () => void;
}

export const usePageHeaderStore = create<HeaderStore>((set) => ({
    metadata: { // Preenchimento padrão, para endereço "/"
        shortTitle: "Ensalamento",
        spanTitle: "semanal",
        shortDescription: "Semestre 2026.2",
        spanDescription: "· alocação de turmas por dia e horário",
    },

// As funções são chamadas em união para obter os dados (setPageHeader) do arquivo e resetar a página
// para preparar para a adesão dos valores novos.

    setPageHeader: (data) => set((state) => ({ ...state, metadata: { ...data } })), 
    resetPageHeader: () => set({ metadata: { shortTitle: "Dashboard", shortDescription: "" } }),
}));
