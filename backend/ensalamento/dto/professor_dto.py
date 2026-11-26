from dataclasses import dataclass


@dataclass
class ProfessorDTO:
    id: int
    nome: str
    matricula: int
    usuario_id: int
