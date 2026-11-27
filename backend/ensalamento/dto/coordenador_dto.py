from dataclasses import dataclass


@dataclass
class CoordenadorDTO:
    id: int
    nome: str
    usuario_id: int
