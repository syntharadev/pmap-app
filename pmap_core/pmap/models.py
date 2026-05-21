from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class EntityNode(BaseModel):
    """Representa una clase o función detectada por Tree-sitter."""
    name: str
    type: str  # 'function' o 'class'
    hash_cst: str
    turn_index: int

class VulnerabilityReport(BaseModel):
    """Estructura de una falla detectada."""
    turn: int
    severity: str # 'CRITICAL', 'HIGH', 'MEDIUM'
    type: str
    description: str

class ForensicPayload(BaseModel):
    """Objeto final para el Dashboard y los .md."""
    project_name: str
    total_tokens: int
    final_accuracy: float
    vulnerabilities: List[VulnerabilityReport]
    chart_data: List[Dict]