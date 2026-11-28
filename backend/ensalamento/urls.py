
from django.urls import path

from .views import (
    AlocacaoDetailView,
    AlocacaoListCreateView,
    AlocacaoTrocaView,
    CoordenadorDetailView,
    CoordenadorListCreateView,
    DisciplinaDetailView,
    DisciplinaListCreateView,
    HistoricoListView,
    HorarioDetailView,
    HorarioListCreateView,
    NecessitaDeDetailView,
    NecessitaDeListCreateView,
    PainelView,
    PossuiDetailView,
    PossuiListCreateView,
    ProfessorDetailView,
    ProfessorListCreateView,
    RecursoDetailView,
    RecursoListCreateView,
    SalaDetailView,
    SalaListCreateView,
    SemestreDetailView,
    SemestreListCreateView,
    TurmaDetailView,
    TurmaListCreateView,
)


urlpatterns = [
    # Recursos
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

    # Salas
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

    # Disciplinas
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

    # Semestres
    path(
        "semestres/",
        SemestreListCreateView.as_view(),
        name="semestre-list-create",
    ),
    path(
        "semestres/<int:pk>/",
        SemestreDetailView.as_view(),
        name="semestre-detail",
    ),

    # Turmas
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

    # Horários
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

    # Relacionamento sala/recurso
    path(
        "possui/",
        PossuiListCreateView.as_view(),
        name="possui-list-create",
    ),
    path(
        "possui/<int:pk>/",
        PossuiDetailView.as_view(),
        name="possui-detail",
    ),

    # Relacionamento disciplina/recurso
    path(
        "necessita-de/",
        NecessitaDeListCreateView.as_view(),
        name="necessita-de-list-create",
    ),
    path(
        "necessita-de/<int:pk>/",
        NecessitaDeDetailView.as_view(),
        name="necessita-de-detail",
    ),

    # Alocações
    path(
        "alocacoes/",
        AlocacaoListCreateView.as_view(),
        name="alocacao-list-create",
    ),
    path(
        "alocacoes/<int:pk>/",
        AlocacaoDetailView.as_view(),
        name="alocacao-detail",
    ),
    path(
        "alocacoes/<int:pk>/trocar/",
        AlocacaoTrocaView.as_view(),
        name="alocacao-trocar",
    ),

    # Histórico
    path(
        "historico/",
        HistoricoListView.as_view(),
        name="historico-list",
    ),
        # Professores
    path(
        "professores/",
        ProfessorListCreateView.as_view(),
        name="professor-list-create",
    ),
    path(
        "professores/<int:pk>/",
        ProfessorDetailView.as_view(),
        name="professor-detail",
    ),

    # Coordenadores
    path(
        "coordenadores/",
        CoordenadorListCreateView.as_view(),
        name="coordenador-list-create",
    ),
    path(
        "coordenadores/<int:pk>/",
        CoordenadorDetailView.as_view(),
        name="coordenador-detail",
    ),

    # Painel público
    path(
        "painel/",
        PainelView.as_view(),
        name="painel",
    ),
]
