from dataclasses import dataclass
from datetime import date


@dataclass
class SemestreDTO:
    id: int
    ano: int
    periodo: int
    data_inicio: date
    data_fim: date
