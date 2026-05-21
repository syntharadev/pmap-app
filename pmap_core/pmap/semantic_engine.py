import ast
import os
import json
import networkx as nx
from typing import List, Dict, Any

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    raise ImportError("Falta instalar scikit-learn. Ejecuta: pip install scikit-learn")

class SemanticGraphEngine:
    """
    Motor Semántico y de Grafos para PMAP.APP (Versión Hardware-Safe).
    """
    def __init__(self):
        # 1. Almacén Ligero (Reemplazo de LanceDB)
        from pmap.config import SEMANTIC_DB_PATH
        self.db_path = SEMANTIC_DB_PATH
        
        # 2. Motor Vectorial Clásico (Scikit-Learn AVX-Free)
        self.vectorizer = TfidfVectorizer()
        
        # 3. Inicializar Grafo en RAM
        self.dependency_graph = nx.DiGraph()
        
        self.business_rules = []
        self.rules_vectors = None
        self.complexity_trend = []

    # ==========================================
    # MOTOR 1: COMPLEJIDAD Y PARCHES CIEGOS
    # ==========================================
    
    def calculate_cyclomatic_complexity(self, code_block: str) -> int:
        if not code_block.strip():
            return 0
        try:
            tree = ast.parse(code_block)
        except SyntaxError:
            return -1 
            
        complexity = 1
        branching_nodes = (ast.If, ast.For, ast.While, ast.Try, ast.ExceptHandler, ast.With)
        
        for node in ast.walk(tree):
            if isinstance(node, branching_nodes):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        return complexity

    def detect_blind_patch(self, current_turn: int, code_block: str) -> Dict[str, Any]:
        current_cc = self.calculate_cyclomatic_complexity(code_block)
        if current_cc == -1:
            return {"is_blind_patch": False, "reason": "Syntax Error"}
            
        self.complexity_trend.append((current_turn, current_cc))
        
        if len(self.complexity_trend) < 3:
            return {"is_blind_patch": False, "cc_score": current_cc}
            
        _, cc_1 = self.complexity_trend[-3]
        _, cc_2 = self.complexity_trend[-2]
        
        delta = current_cc - cc_1
        if delta >= 5 and current_cc >= 10:
            return {
                "is_blind_patch": True,
                "cc_score": current_cc,
                "delta": delta,
                "description": f"Incremento drástico de complejidad ciclomática (+{delta} ramas). Riesgo crítico de Código Espagueti."
            }
        return {"is_blind_patch": False, "cc_score": current_cc}

    # ==========================================
    # MOTOR 2: AMNESIA ALGEBRAICA (SCIKIT-LEARN)
    # ==========================================

    def extract_and_vectorize_rules(self, turn_0_text: str):
        sentences = [s.strip() for s in turn_0_text.split('.') if len(s.strip()) > 10]
        rule_keywords = ["debe", "siempre", "nunca", "obligatorio", "restricción", "no uses", "requiere"]
        extracted_rules = [s for s in sentences if any(kw in s.lower() for kw in rule_keywords)]
        
        if not extracted_rules and sentences:
            extracted_rules = [sentences[0]]

        if not extracted_rules:
            return
            
        self.business_rules = extracted_rules
        
        # Ajustamos (fit) el modelo vectorial al corpus de reglas
        self.rules_vectors = self.vectorizer.fit_transform(self.business_rules)
        
        # Persistencia ligera
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump({"rules": self.business_rules}, f)
            
        print(f"[*] {len(self.business_rules)} reglas indexadas matemáticamente (Modo AVX-Free).")

    def check_semantic_amnesia(self, current_text: str, current_accuracy_percent: float) -> List[Dict[str, Any]]:
        if not self.business_rules or self.rules_vectors is None:
            return []

        if current_accuracy_percent > 80.0:
            return []

        # Vectorizamos el texto actual usando el vocabulario de las reglas
        current_vector = self.vectorizer.transform([current_text])
        
        # Calculamos la similitud coseno
        similarities = cosine_similarity(current_vector, self.rules_vectors)[0]
        
        amnesia_alerts = []
        for idx, similarity_score in enumerate(similarities):
            # Si la similitud cae cerca de 0 en la zona de peligro de atención
            if similarity_score < 0.05 and current_accuracy_percent < 50.0:
                rule = self.business_rules[idx]
                amnesia_alerts.append({
                    "rule_broken": rule,
                    "distance": round(1.0 - similarity_score, 2),
                    "description": f"Deriva semántica detectada. La IA probablemente ha olvidado la regla: '{rule[:50]}...'"
                })
                
        return amnesia_alerts