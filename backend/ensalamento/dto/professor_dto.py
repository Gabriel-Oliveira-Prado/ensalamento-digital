from dataclasses import dataclass


@dataclass
class ProfessorDTO:
    id: int
    email: str
    nome: str
    matricula: int
    senha: str
