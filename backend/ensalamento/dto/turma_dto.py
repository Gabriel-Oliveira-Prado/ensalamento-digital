from dataclasses import dataclass


@dataclass
class TurmaDTO:
    id: int
    qtd_aluno: int
    semestre_id: int
