import { createBrowserRouter, Navigate } from "react-router-dom";
import { RootLayout } from "./layouts/root.layout";
import { PainelTvPage } from "./pages/tv/painel.page";

export const router = createBrowserRouter([
    {
        element: <RootLayout />,
        children: [
            {
                path: "/painel",
                element: <PainelTvPage />,
            },

            {
                path: "/admin",
            },

            // fallback
            {
                path: "*",
                element: <Navigate to={"/painel"} replace />,
            },
        ],
    },
]);
