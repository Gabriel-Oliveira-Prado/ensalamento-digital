from dataclasses import dataclass


@dataclass
class CoordenadorDTO:
    id: int
    nome: str
    email: str
    senha: str
