from rest_framework import generics

from .models import (
    Disciplina,
    Horario,
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
    RecursoSerializer,
    SalaSerializer,
    TurmaSerializer,
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