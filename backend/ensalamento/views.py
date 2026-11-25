from datetime import date

from django.db import transaction
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
    Disciplina,
    Historico,
    Horario,
    NecessitaDe,
    Possui,
    Recurso,
    Sala,
    Semestre,
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
    SemestreSerializer,
    TurmaSerializer,
    AlocacaoSerializer,
    HistoricoSerializer,
    TrocaAlocacaoSerializer,
)


@extend_schema(tags=["Recursos"], description="Consulta e cadastra recursos das salas.")
class RecursoListCreateView(generics.ListCreateAPIView):
    queryset = Recurso.objects.all().order_by("nome")
    serializer_class = RecursoSerializer
    permission_classes = [PodeConsultarGerenciarRecursos]


@extend_schema(tags=["Recursos"], description="Consulta, atualiza ou exclui um recurso.")
class RecursoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recurso.objects.all()
    serializer_class = RecursoSerializer
    permission_classes = [PodeConsultarGerenciarRecursos]

@extend_schema(tags=["Salas"], description="Consulta e cadastra salas disponíveis para ensalamento.")
class SalaListCreateView(generics.ListCreateAPIView):
    queryset = Sala.objects.all().order_by("nome")
    serializer_class = SalaSerializer
    permission_classes = [PodeConsultarGerenciarSalas]


@extend_schema(tags=["Salas"], description="Consulta, atualiza ou exclui uma sala.")
class SalaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    permission_classes = [PodeConsultarGerenciarSalas]

@extend_schema(tags=["Disciplinas"], description="Consulta e cadastra disciplinas.")
class DisciplinaListCreateView(generics.ListCreateAPIView):
    queryset = Disciplina.objects.all().order_by("nome")
    serializer_class = DisciplinaSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


@extend_schema(tags=["Disciplinas"], description="Consulta, atualiza ou exclui uma disciplina.")
class DisciplinaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]

@extend_schema(tags=["Semestres"], description="Consulta e cadastra semestres letivos.")
class SemestreListCreateView(generics.ListCreateAPIView):
    queryset = Semestre.objects.all().order_by("ano", "periodo")
    serializer_class = SemestreSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


@extend_schema(tags=["Semestres"], description="Consulta, atualiza ou exclui um semestre letivo.")
class SemestreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Semestre.objects.all()
    serializer_class = SemestreSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


@extend_schema(tags=["Turmas"], description="Consulta e cadastra turmas.")
class TurmaListCreateView(generics.ListCreateAPIView):
    queryset = Turma.objects.select_related("semestre").all().order_by(
        "semestre__ano", "semestre__periodo", "id"
    )
    serializer_class = TurmaSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


@extend_schema(tags=["Turmas"], description="Consulta, atualiza ou exclui uma turma.")
class TurmaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


@extend_schema(tags=["Horários"], description="Consulta e cadastra horários de aula.")
class HorarioListCreateView(generics.ListCreateAPIView):
    queryset = Horario.objects.all().order_by(
        "dia",
        "hora_inicio",
    )
    serializer_class = HorarioSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


@extend_schema(tags=["Horários"], description="Consulta, atualiza ou exclui um horário.")
class HorarioDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]

@extend_schema(tags=["Relacionamentos"], description="Vincula recursos às salas.")
class PossuiListCreateView(generics.ListCreateAPIView):
    queryset = Possui.objects.select_related(
        "sala",
        "recurso",
    ).all()
    serializer_class = PossuiSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


@extend_schema(tags=["Relacionamentos"], description="Consulta ou remove um vínculo entre sala e recurso.")
class PossuiDetailView(generics.RetrieveDestroyAPIView):
    queryset = Possui.objects.select_related(
        "sala",
        "recurso",
    ).all()
    serializer_class = PossuiSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]

@extend_schema(tags=["Relacionamentos"], description="Vincula os recursos exigidos por uma disciplina.")
class NecessitaDeListCreateView(generics.ListCreateAPIView):
    queryset = NecessitaDe.objects.select_related(
        "disciplina",
        "recurso",
    ).all()
    serializer_class = NecessitaDeSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]


@extend_schema(tags=["Relacionamentos"], description="Consulta ou remove um recurso exigido por disciplina.")
class NecessitaDeDetailView(generics.RetrieveDestroyAPIView):
    queryset = NecessitaDe.objects.select_related(
        "disciplina",
        "recurso",
    ).all()
    serializer_class = NecessitaDeSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]

@extend_schema_view(
    get=extend_schema(
        tags=["Alocações"],
        summary="Lista alocações",
        description="Retorna as alocações de turma, sala, professor e horário.",
    ),
    post=extend_schema(
        tags=["Alocações"],
        summary="Cria uma alocação",
        description=(
            "Cria uma alocação e bloqueia conflitos de sala, professor ou turma."
        ),
        responses={
            201: AlocacaoSerializer,
            400: OpenApiResponse(description="Dados inválidos ou conflito de ensalamento."),
        },
        examples=[
            OpenApiExample(
                "Conflito de sala",
                value={"erro": "conflito_sala", "detalhe": "A sala já está ocupada nesse horário."},
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                "Conflito de professor",
                value={"erro": "conflito_professor", "detalhe": "O professor já possui uma aula nesse horário."},
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                "Conflito de turma",
                value={"erro": "conflito_turma", "detalhe": "A turma já possui uma aula nesse horário."},
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


@extend_schema(
    tags=["Alocações"],
    description="Consulta, atualiza ou exclui uma alocação. Atualizações também validam conflitos.",
)
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


@extend_schema(
    tags=["Alocações"],
    summary="Troca sala e/ou horário de uma alocação",
    description="Troca a sala e/ou o horário, valida conflitos e registra o motivo no histórico.",
    request=TrocaAlocacaoSerializer,
    responses={
        200: OpenApiResponse(description="Alocação atualizada e registro de histórico."),
        400: OpenApiResponse(description="Dados inválidos ou conflito de ensalamento."),
    },
)
class AlocacaoTrocaView(APIView):
    """Troca a sala e/ou o horário de uma alocação e registra o histórico."""

    permission_classes = [PodeConsultarGerenciarCadastros]

    def post(self, request, pk):
        with transaction.atomic():
            alocacao = generics.get_object_or_404(
                Alocacao.objects.select_for_update().select_related(
                    "horario", "sala"
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


@extend_schema(
    tags=["Histórico"],
    description="Lista as trocas de alocação. Aceita ?alocacao=<id>.",
)
class HistoricoListView(generics.ListAPIView):
    serializer_class = HistoricoSerializer
    permission_classes = [PodeConsultarGerenciarCadastros]

    def get_queryset(self):
        queryset = Historico.objects.select_related(
            "alocacao__sala", "alocacao__disciplina"
        ).order_by("-data_alteracao", "-id")

        alocacao = self.request.query_params.get("alocacao")
        if alocacao is not None:
            if not alocacao.isdigit():
                return queryset.none()
            queryset = queryset.filter(alocacao_id=int(alocacao))

        return queryset


@extend_schema(
    tags=["Painel"],
    description="Aulas do dia para o painel da TV. Público. Aceita ?data=AAAA-MM-DD.",
    responses={200: OpenApiResponse(description="Aulas do dia.")},
)
class PainelView(APIView):
    """Aulas do dia para o painel da TV. Público e somente leitura.

    Parâmetro opcional: ?data=AAAA-MM-DD (padrão: hoje).
    """

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
                    {"detail": "Data inválida. Use o formato AAAA-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            dia = agora.date()

        alocacoes = (
            Alocacao.objects.filter(horario__dia=dia)
            .select_related("horario", "sala", "professor", "turma__semestre", "disciplina")
            .order_by("horario__hora_inicio", "sala__nome")
        )

        aulas = []
        for a in alocacoes:
            if dia != agora.date():
                situacao = "agendada" if dia > agora.date() else "encerrada"
            elif a.horario.hora_fim <= agora.time():
                situacao = "encerrada"
            elif a.horario.hora_inicio <= agora.time():
                situacao = "em_andamento"
            else:
                situacao = "proxima"

            aulas.append(
                {
                    "id": a.id,
                    "hora_inicio": a.horario.hora_inicio.strftime("%H:%M"),
                    "hora_fim": a.horario.hora_fim.strftime("%H:%M"),
                    "sala": a.sala.nome,
                    "disciplina": a.disciplina.nome,
                    "professor": a.professor.nome,
                    "turma": f"{a.turma.semestre.ano}/{a.turma.semestre.periodo}",
                    "situacao": situacao,
                }
            )

        return Response(
            {
                "data": dia.isoformat(),
                "atualizado_em": agora.isoformat(),
                "aulas": aulas,
            }
        )