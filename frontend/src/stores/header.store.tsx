import type { RouteHandleMetada } from "@/types/route.handles";
import { create } from "zustand";

interface HeaderStore {
    metadata: RouteHandleMetada;
    setPageHeader: (data: RouteHandleMetada) => void;
    resetPageHeader: () => void;
}

export const usePageHeaderStore = create<HeaderStore>((set) => ({
    metadata: {
        shortTitle: "Ensalamento",
        spanTitle: "semanal",
        shortDescription: "Semestre 2026.2",
        spanDescription: "· alocação de turmas por dia e horário",
    },
    setPageHeader: (data) => set((state) => ({ ...state, metadata: { ...data } })),
    resetPageHeader: () => set({ metadata: { shortTitle: "Dashboard", shortDescription: "" } }),
}));
