from dataclasses import dataclass


@dataclass
class TurmaDTO:
    id: int
    qtd_aluno: int
    ano: int
    periodo: int
