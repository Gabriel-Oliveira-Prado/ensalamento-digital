from rest_framework import generics

from .models import Recurso, Sala
from .permissions import (
    PodeConsultarGerenciarRecursos,
    PodeConsultarGerenciarSalas,
)
from .serializers import RecursoSerializer, SalaSerializer


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