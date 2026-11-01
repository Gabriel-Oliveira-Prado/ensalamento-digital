import { createBrowserRouter, Navigate } from "react-router-dom";
import { AuthLayout } from "./layouts/auth.layout";
import { RootLayout } from "./layouts/root.layout";
import { RegisterPage } from "./pages/admin/auth/register.page";
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
                                path: "register",
                                element: <RegisterPage />,
                            },
                            {
                                path: "login",
                                element: <div>Login</div>,
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
