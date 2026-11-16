from django.urls import path

from .views import (
    RecursoDetailView,
    RecursoListCreateView,
    SalaDetailView,
    SalaListCreateView,
)


urlpatterns = [
    path(
        "recursos/",
        RecursoListCreateView.as_view(),
        name="recurso-list-create",
    ),
    path(
        "recursos/<int:pk>/",
        RecursoDetailView.as_view(),
        name="recurso-detail",
    ),
    path(
        "salas/",
        SalaListCreateView.as_view(),
        name="sala-list-create",
    ),
    path(
        "salas/<int:pk>/",
        SalaDetailView.as_view(),
        name="sala-detail",
    ),
]