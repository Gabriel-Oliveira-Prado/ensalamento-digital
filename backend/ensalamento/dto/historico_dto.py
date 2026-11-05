from dataclasses import dataclass
from datetime import date

class HistoricoDTO:
    id: int
    data_alteracao: date
    motivo: str
    alocacao_id: int
