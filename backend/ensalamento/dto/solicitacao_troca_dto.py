from dataclasses import dataclass


@dataclass
class SolicitacaoTrocaDTO:
    id: int
    motivo: str
    status: str
    tipo_troca: str
    alocacao_origem_id: int
    alocacao_destino_id: int
    professor_solicitante_id: int
