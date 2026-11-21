from rest_framework import generics

from .models import (
    Alocacao,
    Disciplina,
    Horario,
    NecessitaDe,
    Possui,
    Recurso,
    Sala,
    Turma,
)

from .permissions import (
    PodeConsultarGerenciarRecursos,
    PodeConsultarGerenciarSalas,
    PodeConsultarGerenciarCadastros
)
from .serializers import (
    DisciplinaSerializer,
    HorarioSerializer,
    NecessitaDeSerializer,
    PossuiSerializer,
    RecursoSerializer,
    SalaSerializer,
    TurmaSerializer,
    AlocacaoSerializer,
)


class RecursoListCreateView(generics.ListCreateAPIView):
    queryset = Recurso.objects.all().order_by("nome")
    serializer_class = RecursoSerializer
    permission_classes = [PodeConsultarGerenciarRecursos]


class RecursoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recurso.objects.all()
    serializer_class = RecursoSerializer
    permission_classes = [PodeConsultarGerenciarRecursos]

class SalaListCreateView(generics.ListCreateAPIView):
    queryset = Sala.objects.all().order_by("nome")
    serializer_class = SalaSerializer
    permission_classes = [PodeConsultarGerenciarSalas]


class SalaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    permission_classes = [PodeConsultarGerenciarSalas]

class DisciplinaListCreateView(generics.ListCreateAPIView):
    queryset = Disciplina.objects.all().order_by("nome")
    serializer_class = DisciplinaSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


class DisciplinaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]

class TurmaListCreateView(generics.ListCreateAPIView):
    queryset = Turma.objects.all().order_by("ano", "periodo", "id")
    serializer_class = TurmaSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


class TurmaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


class HorarioListCreateView(generics.ListCreateAPIView):
    queryset = Horario.objects.all().order_by(
        "dia",
        "hora_inicio",
    )
    serializer_class = HorarioSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


class HorarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]

class PossuiListCreateView(generics.ListCreateAPIView):
    queryset = Possui.objects.select_related(
        "sala",
        "recurso",
    ).all()
    serializer_class = PossuiSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


class PossuiDetailView(generics.RetrieveDestroyAPIView):
    queryset = Possui.objects.select_related(
        "sala",
        "recurso",
    ).all()
    serializer_class = PossuiSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]

class NecessitaDeListCreateView(generics.ListCreateAPIView):
    queryset = NecessitaDe.objects.select_related(
        "disciplina",
        "recurso",
    ).all()
    serializer_class = NecessitaDeSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


class NecessitaDeDetailView(generics.RetrieveDestroyAPIView):
    queryset = NecessitaDe.objects.select_related(
        "disciplina",
        "recurso",
    ).all()
    serializer_class = NecessitaDeSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]

class AlocacaoListCreateView(generics.ListCreateAPIView):
    queryset = Alocacao.objects.select_related(
        "horario",
        "professor",
        "sala",
        "turma",
        "disciplina",
        "coordenador",
    ).all()

    serializer_class = AlocacaoSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


class AlocacaoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alocacao.objects.select_related(
        "horario",
        "professor",
        "sala",
        "turma",
        "disciplina",
        "coordenador",
    ).all()

    serializer_class = AlocacaoSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]