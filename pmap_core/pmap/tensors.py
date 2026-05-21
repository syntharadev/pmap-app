import re
from typing import Dict, Any

class EmotionalTensorEngine:
    """
    Motor de Tensores de Intención para PMAP.APP.
    Mide la fluidez contextual y detecta el "Colapso por Complacencia" (Apology Loops).
    Optimizado para CPU (AVX-Safe) usando mapas de densidad léxica.
    """
    def __init__(self):
        # Pesos sinápticos heurísticos para la Fricción del Usuario
        self.friction_markers = {
            r"\b(no funciona|falla|error|rompe)\b": 1.5,
            r"\b(otra vez|sigues|vuelves a)\b": 2.0,
            r"\b(no entiendes|te dije que|olvidaste)\b": 2.5,
            r"\b(mal|incorrecto|pésimo)\b": 2.0
        }
        
        # Pesos sinápticos heurísticos para la Sumisión del LLM (Complacencia)
        self.submission_markers = {
            r"\b(lo siento|disculpa|perdón|mis disculpas)\b": 2.5,
            r"\b(tienes razón|mi error|me equivoqué)\b": 2.0,
            r"\b(aquí tienes la corrección|corregido|ahora sí)\b": 1.0,
            r"\b(omisión|pasé por alto)\b": 1.5
        }
        
        self.tensor_history = []

    def _calculate_tensor_weight(self, text: str, markers: Dict[str, float]) -> float:
        """Calcula el peso tensorial basado en la densidad de marcadores."""
        if not text:
            return 0.0
            
        text_lower = text.lower()
        weight = 0.0
        
        for pattern, score in markers.items():
            matches = len(re.findall(pattern, text_lower))
            weight += (matches * score)
            
        return weight

    def evaluate_conversational_node(self, turn_index: int, user_text: str, model_text: str) -> Dict[str, Any]:
        """
        Evalúa un par de interacción (Usuario -> Modelo) para calcular
        el gradiente de tensión emocional/técnica.
        """
        friction_score = self._calculate_tensor_weight(user_text, self.friction_markers)
        submission_score = self._calculate_tensor_weight(model_text, self.submission_markers)
        
        self.tensor_history.append({
            "turn": turn_index,
            "friction": friction_score,
            "submission": submission_score
        })
        
        is_cognitive_collapse = friction_score >= 2.0 and submission_score >= 2.5
        
        alert = None
        if is_cognitive_collapse:
            alert = {
                "turn": turn_index,
                "severity": "HIGH",
                "type": "Colapso Cognitivo (Bucle de Disculpas)",
                "description": f"El LLM abandonó el rigor técnico (Tensor de Sumisión: {submission_score}). Riesgo inminente de generación de 'Código Espagueti' para complacer al usuario."
            }
            
        return {
            "friction_score": friction_score,
            "submission_score": submission_score,
            "is_collapse": is_cognitive_collapse,
            "alert": alert
        }