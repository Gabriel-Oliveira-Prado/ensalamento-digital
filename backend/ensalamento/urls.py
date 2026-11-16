from django.urls import path

from .views import (
    DisciplinaDetailView,
    DisciplinaListCreateView,
    HorarioDetailView,
    HorarioListCreateView,
    RecursoDetailView,
    RecursoListCreateView,
    SalaDetailView,
    SalaListCreateView,
    TurmaDetailView,
    TurmaListCreateView,
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
    path(
    "disciplinas/",
    DisciplinaListCreateView.as_view(),
    name="disciplina-list-create",
    ),
    path(
        "disciplinas/<int:pk>/",
        DisciplinaDetailView.as_view(),
        name="disciplina-detail",
    ),
    path(
        "turmas/",
        TurmaListCreateView.as_view(),
        name="turma-list-create",
    ),
    path(
        "turmas/<int:pk>/",
        TurmaDetailView.as_view(),
        name="turma-detail",
    ),
    path(
        "horarios/",
        HorarioListCreateView.as_view(),
        name="horario-list-create",
    ),
    path(
        "horarios/<int:pk>/",
        HorarioDetailView.as_view(),
        name="horario-detail",
    ),
]