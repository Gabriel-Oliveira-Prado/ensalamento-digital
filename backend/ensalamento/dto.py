"""Contratos de dados simples, sem dependência da camada HTTP."""

from dataclasses import dataclass
from datetime import date, time


@dataclass(frozen=True, slots=True)
class RecursoDTO:
    id: int | None
    nome: str


@dataclass(frozen=True, slots=True)
class SalaDTO:
    id: int | None
    capacidade: int
    nome: str
    tipo: str


@dataclass(frozen=True, slots=True)
class PossuiDTO:
    id: int | None
    sala_id: int
    recurso_id: int


@dataclass(frozen=True, slots=True)
class DisciplinaDTO:
    id: int | None
    nome: str
    codigo: int


@dataclass(frozen=True, slots=True)
class NecessitaDeDTO:
    id: int | None
    recurso_id: int
    disciplina_id: int


@dataclass(frozen=True, slots=True)
class TurmaDTO:
    id: int | None
    qtd_aluno: int
    ano: int
    periodo: int


@dataclass(frozen=True, slots=True)
class HorarioDTO:
    id: int | None
    dia: date
    hora_inicio: time
    hora_fim: time


@dataclass(frozen=True, slots=True)
class ProfessorDTO:
    id: int | None
    email: str
    nome: str


@dataclass(frozen=True, slots=True)
class CoordenadorDTO:
    id: int | None
    nome: str
    email: str


@dataclass(frozen=True, slots=True)
class AlocacaoDTO:
    id: int | None
    horario_id: int
    professor_id: int
    sala_id: int
    turma_id: int
    disciplina_id: int
    coordenador_id: int


@dataclass(frozen=True, slots=True)
class HistoricoDTO:
    id: int | None
    data_alteracao: date
    motivo: str
    alocacao_id: int
