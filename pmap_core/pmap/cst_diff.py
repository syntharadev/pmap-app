import re
import tree_sitter_python as tspython
from tree_sitter import Language, Parser
from typing import Dict, Set, Any

class CSTForensicAnalyzer:
    """
    Analizador de Árboles de Sintaxis Concreta (CST) para PMAP.APP.
    Detecta la amnesia estructural en LLMs mediante disección a nivel de compilador.
    """
    def __init__(self):
        # Inicializamos el compilador para Python usando los bindings v0.21+
        self.PY_LANGUAGE = Language(tspython.language())
        self.parser = Parser()
        self.parser.language = self.PY_LANGUAGE

    def extract_code_blocks(self, markdown_text: str) -> str:
        """
        Extrae código encapsulado en bloques de markdown (```python ... ```).
        Ignora el texto conversacional para evitar ruido en el AST.
        """
        if not markdown_text:
            return ""
            
        # Regex para capturar todo el contenido dentro de ```python y ```
        pattern = re.compile(r"```python\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)
        matches = pattern.findall(markdown_text)
        
        # Unimos todos los bloques de código generados en ese turno
        return "\n\n".join(matches)

    def _extract_entities_from_cst(self, code: str) -> Set[str]:
        """
        Recorre el Árbol de Sintaxis Concreta y extrae firmas únicas
        (nombres de funciones y clases).
        """
        if not code.strip():
            return set()

        tree = self.parser.parse(bytes(code, "utf8"))
        root_node = tree.root_node
        entities = set()

        # Query S-expression nativa de tree-sitter para aislar definiciones
        # Capturamos funciones y clases por su identificador (nombre)
        query = self.PY_LANGUAGE.query("""
            (function_definition name: (identifier) @function.def)
            (class_definition name: (identifier) @class.def)
        """)

        captures = query.captures(root_node)
        
        for node, capture_name in captures:
            # Extraemos el texto exacto del nodo (el nombre de la función/clase)
            entity_name = code[node.start_byte:node.end_byte]
            entities.add(f"{capture_name}::{entity_name}")

        return entities

    def compute_memory_diff(self, old_code: str, new_code: str) -> Dict[str, Any]:
        """
        Compara dos estados de código a nivel CST.
        Retorna un dict con las entidades borradas por error y las alucinadas.
        """
        old_entities = self._extract_entities_from_cst(old_code)
        new_entities = self._extract_entities_from_cst(new_code)

        # Entidades que estaban en el turno anterior y desaparecieron (Amnesia)
        forgotten = old_entities - new_entities
        
        # Entidades que aparecieron de la nada (Posible alucinación o feature nueva)
        hallucinated = new_entities - old_entities

        return {
            "is_degraded": len(forgotten) > 0,
            "forgotten": list(forgotten),
            "hallucinated": list(hallucinated),
            "total_entities_now": len(new_entities)
        }

if __name__ == "__main__":
    # Test rápido de integridad estructural
    analyzer = CSTForensicAnalyzer()
    
    code_v1 = """
class MotorBase:
    pass
def inicializar():
    pass
def guardar_datos():
    pass
"""
    # En la V2, el LLM olvidó "guardar_datos" y alucinó "limpiar_cache"
    code_v2 = """
class MotorBase:
    pass
def inicializar():
    pass
def limpiar_cache():
    pass
"""
    
    diff = analyzer.compute_memory_diff(code_v1, code_v2)
    print("Test CST Forensic Diff:")
    print(diff)