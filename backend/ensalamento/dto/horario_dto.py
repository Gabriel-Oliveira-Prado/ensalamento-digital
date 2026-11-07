from dataclasses import dataclass
from datetime import date, time

class HorarioDTO:
    id: int
    dia: date
    hora_inicio: time
    hora_fim: time
