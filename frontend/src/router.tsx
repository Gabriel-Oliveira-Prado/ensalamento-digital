import { createBrowserRouter, Navigate } from "react-router-dom";
import { ProtectedRoute } from "./components/protected.route";
import { AuthLayout } from "./layouts/auth.layout";
import { DashboardLayout } from "./layouts/dashboard.layout";
import { RootLayout } from "./layouts/root.layout";
import { LoginPage } from "./pages/admin/auth/login.page";
import { HomePage } from "./pages/admin/home.page";
import { RegisterPage } from "./pages/admin/register.page";
import { RequestPage } from "./pages/admin/request.page";
import { HistoryPage } from "./pages/admin/history.page";
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
                        element: <ProtectedRoute />,
                        children: [
                            {
                                element: <DashboardLayout />,
                                children: [
                                    {
                                        index: true,
                                        element: <HomePage />,
                                    },
                                    {
                                        path: "cadastros",
                                        element: <RegisterPage />,
                                    },
                                    {
                                        path: "solicitacoes",
                                        element: <RequestPage />,
                                    },
                                    {
                                        path: "historico",
                                        element: <HistoryPage />,
                                    }
                                ],
                            },
                        ],
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
