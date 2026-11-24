from dataclasses import dataclass


@dataclass
class SalaDTO:
    id: int
    capacidade: int
    nome: str
    tipo: str
