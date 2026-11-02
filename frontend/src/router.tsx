import { createBrowserRouter, Navigate } from "react-router-dom";
import { AuthLayout } from "./layouts/auth.layout";
import { RootLayout } from "./layouts/root.layout";
import { LoginPage } from "./pages/admin/auth/login.page";
import { HomePage } from "./pages/admin/home.page";
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
                children: [
                    {
                        index: true,
                        element: <HomePage />,
                    },
                    {
                        element: <AuthLayout />,
                        children: [
                            {
                                path: "auth",
                                element: <LoginPage />,
                            },
                        ],
                    },
                ],
            },

            // fallback
            {
                path: "/",
                element: <Navigate to={"/painel"} replace />,
            },
        ],
    },
]);
