from dataclasses import dataclass
from datetime import datetime


@dataclass
class HistoricoDTO:
    id: int
    data_alteracao: datetime
    motivo: str
    alocacao_id: int
