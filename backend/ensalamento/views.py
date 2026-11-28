
from datetime import date

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Alocacao,
    Coordenador,
    Disciplina,
    Historico,
    Horario,
    NecessitaDe,
    Possui,
    Professor,
    Recurso,
    Sala,
    Semestre,
    Turma,
)

from .permissions import (
    PodeConsultarGerenciarRecursos,
    PodeConsultarGerenciarSalas,
    PodeConsultarGerenciarCadastros,
)

from .serializers import (
    DisciplinaSerializer,
    HorarioSerializer,
    NecessitaDeSerializer,
    PossuiSerializer,
    ProfessorSerializer,
    CoordenadorSerializer,
    RecursoSerializer,
    SalaSerializer,
    SemestreSerializer,
    TurmaSerializer,
    AlocacaoSerializer,
    HistoricoSerializer,
    TrocaAlocacaoSerializer,
    PainelSerializer,
)

# ============================================================
# RECURSOS
# ============================================================

@extend_schema(tags=["Recursos"])
class RecursoListCreateView(generics.ListCreateAPIView):
    queryset = Recurso.objects.all().order_by("nome")
    serializer_class = RecursoSerializer
    permission_classes = [PodeConsultarGerenciarRecursos]


@extend_schema(tags=["Recursos"])
class RecursoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recurso.objects.all()
    serializer_class = RecursoSerializer
    permission_classes = [PodeConsultarGerenciarRecursos]


# ============================================================
# SALAS
# ============================================================

@extend_schema(tags=["Salas"])
class SalaListCreateView(generics.ListCreateAPIView):
    queryset = Sala.objects.all().order_by("nome")
    serializer_class = SalaSerializer
    permission_classes = [PodeConsultarGerenciarSalas]


@extend_schema(tags=["Salas"])
class SalaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    permission_classes = [PodeConsultarGerenciarSalas]


# ============================================================
# DISCIPLINAS
# ============================================================

@extend_schema(tags=["Disciplinas"])
class DisciplinaListCreateView(generics.ListCreateAPIView):
    queryset = Disciplina.objects.all().order_by("nome")
    serializer_class = DisciplinaSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


@extend_schema(tags=["Disciplinas"])
class DisciplinaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


# ============================================================
# SEMESTRES
# ============================================================

@extend_schema(tags=["Semestres"])
class SemestreListCreateView(generics.ListCreateAPIView):
    queryset = Semestre.objects.all().order_by("ano", "periodo")
    serializer_class = SemestreSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


@extend_schema(tags=["Semestres"])
class SemestreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Semestre.objects.all()
    serializer_class = SemestreSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


# ============================================================
# TURMAS
# ============================================================

@extend_schema(tags=["Turmas"])
class TurmaListCreateView(generics.ListCreateAPIView):
    queryset = Turma.objects.select_related(
        "semestre"
    ).all().order_by(
        "semestre__ano",
        "semestre__periodo",
        "id",
    )
    serializer_class = TurmaSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


@extend_schema(tags=["Turmas"])
class TurmaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Turma.objects.select_related("semestre").all()
    serializer_class = TurmaSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


# ============================================================
# HORÁRIOS
# ============================================================

@extend_schema(tags=["Horários"])
class HorarioListCreateView(generics.ListCreateAPIView):
    queryset = Horario.objects.all().order_by(
        "dia",
        "hora_inicio",
    )
    serializer_class = HorarioSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


@extend_schema(tags=["Horários"])
class HorarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


# ============================================================
# RELACIONAMENTO: SALA POSSUI RECURSO
# ============================================================

@extend_schema(tags=["Relacionamentos"])
class PossuiListCreateView(generics.ListCreateAPIView):
    queryset = Possui.objects.select_related(
        "sala",
        "recurso",
    ).all()
    serializer_class = PossuiSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


@extend_schema(tags=["Relacionamentos"])
class PossuiDetailView(generics.RetrieveDestroyAPIView):
    queryset = Possui.objects.select_related(
        "sala",
        "recurso",
    ).all()
    serializer_class = PossuiSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


# ============================================================
# RELACIONAMENTO: DISCIPLINA NECESSITA DE RECURSO
# ============================================================

@extend_schema(tags=["Relacionamentos"])
class NecessitaDeListCreateView(generics.ListCreateAPIView):
    queryset = NecessitaDe.objects.select_related(
        "disciplina",
        "recurso",
    ).all()
    serializer_class = NecessitaDeSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


@extend_schema(tags=["Relacionamentos"])
class NecessitaDeDetailView(generics.RetrieveDestroyAPIView):
    queryset = NecessitaDe.objects.select_related(
        "disciplina",
        "recurso",
    ).all()
    serializer_class = NecessitaDeSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


# ============================================================
# ALOCAÇÕES
# ============================================================

@extend_schema_view(
    get=extend_schema(
        tags=["Alocações"],
        summary="Lista alocações",
    ),
    post=extend_schema(
        tags=["Alocações"],
        summary="Cria uma alocação",
        description=(
            "Cria uma alocação validando conflitos de sala, professor, "
            "turma e recursos necessários."
        ),
        responses={
            201: AlocacaoSerializer,
            400: OpenApiResponse(
                description="Dados inválidos ou conflito de ensalamento."
            ),
        },
        examples=[
            OpenApiExample(
                "Conflito de sala",
                value={
                    "erro": ["conflito_sala"],
                    "detalhe": [
                        "A sala já está ocupada nesse horário."
                    ],
                },
                response_only=True,
                status_codes=["400"],
            ),
        ],
    ),
)
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


@extend_schema(tags=["Alocações"])
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


# ============================================================
# TROCA ADMINISTRATIVA DE SALA E/OU HORÁRIO
# ============================================================

@extend_schema(
    tags=["Alocações"],
    summary="Troca sala e/ou horário de uma alocação",
    description=(
        "Altera a sala e/ou o horário, valida conflitos e registra "
        "o motivo no histórico."
    ),
    request=TrocaAlocacaoSerializer,
    responses={
        200: OpenApiResponse(
            description="Alocação atualizada e histórico registrado."
        ),
        400: OpenApiResponse(
            description="Dados inválidos ou conflito de ensalamento."
        ),
        404: OpenApiResponse(
            description="Alocação não encontrada."
        ),
    },
)
class AlocacaoTrocaView(APIView):
    permission_classes = [PodeConsultarGerenciarCadastros]

    def post(self, request, pk):
        with transaction.atomic():
            alocacao = get_object_or_404(
                Alocacao.objects.select_for_update().select_related(
                    "horario",
                    "professor",
                    "sala",
                    "turma",
                    "disciplina",
                    "coordenador",
                ),
                pk=pk,
            )

            serializer = TrocaAlocacaoSerializer(
                data=request.data,
                context={"alocacao": alocacao},
            )
            serializer.is_valid(raise_exception=True)

            dados = serializer.validated_data

            alocacao.sala = dados.get("sala", alocacao.sala)
            alocacao.horario = dados.get("horario", alocacao.horario)

            alocacao.save(update_fields=["sala", "horario"])

            historico = Historico.objects.create(
                alocacao=alocacao,
                motivo=dados["motivo"],
                data_alteracao=timezone.now(),
            )

        return Response(
            {
                "alocacao": AlocacaoSerializer(alocacao).data,
                "historico": HistoricoSerializer(historico).data,
            },
            status=status.HTTP_200_OK,
        )


# ============================================================
# HISTÓRICO
# ============================================================

@extend_schema(
    tags=["Histórico"],
    description="Lista o histórico. Aceita o filtro ?alocacao=<id>.",
)
class HistoricoListView(generics.ListAPIView):
    serializer_class = HistoricoSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]

    def get_queryset(self):
        queryset = Historico.objects.select_related(
            "alocacao__sala",
            "alocacao__disciplina",
            "solicitacao_troca",
        ).order_by(
            "-data_alteracao",
            "-id",
        )

        alocacao_id = self.request.query_params.get("alocacao")

        if alocacao_id is not None:
            if not alocacao_id.isdigit():
                return queryset.none()

            queryset = queryset.filter(
                alocacao_id=int(alocacao_id)
            )

        return queryset


# ============================================================
# PAINEL PÚBLICO
# ============================================================

@extend_schema(
    tags=["Painel"],
    description="Aulas do dia para o painel da TV. Público. Aceita ?data=AAAA-MM-DD.",
    responses={
        200: PainelSerializer,
        400: OpenApiResponse(
            description="Data inválida. Use o formato AAAA-MM-DD."
        ),
    },
)
class PainelView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        agora = timezone.localtime()
        data_param = request.query_params.get("data")

        if data_param:
            try:
                dia = date.fromisoformat(data_param)
            except ValueError:
                return Response(
                    {
                        "detail": (
                            "Data inválida. Use o formato AAAA-MM-DD."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            dia = agora.date()

        alocacoes = (
            Alocacao.objects.filter(horario__dia=dia)
            .select_related(
                "horario",
                "sala",
                "professor",
                "turma__semestre",
                "disciplina",
            )
            .order_by(
                "horario__hora_inicio",
                "sala__nome",
            )
        )

        aulas = []

        for alocacao in alocacoes:
            if dia < agora.date():
                situacao = "encerrada"
            elif dia > agora.date():
                situacao = "agendada"
            elif alocacao.horario.hora_fim <= agora.time():
                situacao = "encerrada"
            elif alocacao.horario.hora_inicio <= agora.time():
                situacao = "em_andamento"
            else:
                situacao = "proxima"

            aulas.append({
                "id": alocacao.id,
                "hora_inicio": alocacao.horario.hora_inicio.strftime(
                    "%H:%M"
                ),
                "hora_fim": alocacao.horario.hora_fim.strftime(
                    "%H:%M"
                ),
                "sala": alocacao.sala.nome,
                "disciplina": alocacao.disciplina.nome,
                "professor": alocacao.professor.nome,
                "turma": (
                    f"{alocacao.turma.semestre.ano}/"
                    f"{alocacao.turma.semestre.periodo}"
                ),
                "situacao": situacao,
            })

        return Response({
            "data": dia.isoformat(),
            "atualizado_em": agora.isoformat(),
            "aulas": aulas,
        })
    
# ============================================================
# PROFESSORES
# ============================================================
@extend_schema(tags=["Professores"])
class ProfessorListCreateView(generics.ListCreateAPIView):
    queryset = Professor.objects.all().order_by("nome")
    serializer_class = ProfessorSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


@extend_schema(tags=["Professores"])
class ProfessorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


# ============================================================
# COORDENADORES
# ============================================================

@extend_schema(tags=["Coordenadores"])
class CoordenadorListCreateView(generics.ListCreateAPIView):
    queryset = Coordenador.objects.all().order_by("nome")
    serializer_class = CoordenadorSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


@extend_schema(tags=["Coordenadores"])
class CoordenadorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coordenador.objects.all()
    serializer_class = CoordenadorSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]
    
