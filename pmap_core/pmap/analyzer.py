# Copyright (c) 2026 syntharadev (syntharadev@gmail.com)
# Todos los derechos reservados. Licencia: GNU AGPLv3
import gc
import math
try:
    import duckdb
    HAS_DUCKDB = True
except ImportError:
    import sqlite3
    HAS_DUCKDB = False
import ast
import re
import networkx as nx
from typing import List, Dict, Any


class PMAPEngine:
    def __init__(self, max_context_window: int = 128000):
        self.max_context = max_context_window
        self.ast_inventory = set()
        self.graph = nx.DiGraph()
        
        if HAS_DUCKDB:
            self.db_path = "pmap_forensic.duckdb"
            self.con = duckdb.connect(self.db_path)
            # [!] AJUSTE DE HARDWARE: Forzar a DuckDB a respetar el límite de memoria del NUC
            self.con.execute("SET memory_limit = '2GB';")
            self.con.execute("SET threads = 2;")
        else:
            self.db_path = ":memory:"
            self.con = sqlite3.connect(self.db_path)
            
        self._init_db()

    def __del__(self):
        try:
            self.con.close()
        except Exception:
            pass

    def _init_db(self):
        self.con.execute("CREATE TABLE IF NOT EXISTS history (idx INTEGER PRIMARY KEY, role VARCHAR, content TEXT, tk INTEGER)")
        self.con.execute("CREATE TABLE IF NOT EXISTS vulns (idx INTEGER, severity VARCHAR, type VARCHAR, description TEXT)")

    def ingest_structured_data(self, turns: List[Dict[str, Any]]):
        self.con.execute("DELETE FROM history")
        for i, t in enumerate(turns):
            tk = len(t['content']) // 4
            if HAS_DUCKDB:
                self.con.execute("""
                    INSERT INTO history VALUES (?, ?, ?, ?) 
                    ON CONFLICT (idx) DO UPDATE SET role=EXCLUDED.role, content=EXCLUDED.content, tk=EXCLUDED.tk
                """, [i, t['role'], t['content'], tk])
            else:
                self.con.execute("""
                    INSERT INTO history VALUES (?, ?, ?, ?) 
                    ON CONFLICT (idx) DO UPDATE SET role=excluded.role, content=excluded.content, tk=excluded.tk
                """, [i, t['role'], t['content'], tk])

    def ingest_json_history(self, file_path: str):
        """Ingesta directa desde archivo JSON para el CLI."""
        import json
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Soportar tanto formato plano como formato con clave 'turns'
        if isinstance(data, dict) and "turns" in data:
            data = data["turns"]
        self.ingest_structured_data(data)

    def _analyze_ast_and_graph(self, content: str) -> Dict[str, Any]:
        """
        [FIX] Método unificado que extrae el inventario AST y construye
        el grafo de dependencias simultáneamente.
        Antes existía como _analyze_ast() sin integración de grafo.
        """
        # Patrón hexadecimal: \x60 es la comilla invertida. Evita la corrupción al copiar.
        pattern = r'\x60{3}(?:[a-zA-Z]*)\n?(.*?)\x60{3}'
        blocks = re.findall(pattern, content, re.DOTALL)
        code = "\n".join(blocks)
        inventory = set()
        complexity = 1
        
        if not code: 
            return {"inventory": inventory, "complexity": complexity}
        
        try:
            tree = ast.parse(code)
            current_scope = None
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    inventory.add(node.name)
                    self.graph.add_node(node.name, type="class")
                    current_scope = node.name
                    # Registrar dependencias de herencia
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            self.graph.add_edge(node.name, base.id)
                            
                elif isinstance(node, ast.FunctionDef):
                    inventory.add(node.name)
                    self.graph.add_node(node.name, type="function")
                    # Si la función está dentro de una clase, registrar dependencia
                    if current_scope:
                        self.graph.add_edge(current_scope, node.name)
                        
                elif isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                    complexity += 1
                    
                # Detectar llamadas a funciones para construir el grafo de dependencias
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in inventory:
                        # Función conocida llamada desde el contexto actual
                        self.graph.add_edge("__caller__", node.func.id)
                    elif isinstance(node.func, ast.Attribute):
                        if isinstance(node.func.value, ast.Name):
                            target = f"{node.func.value.id}.{node.func.attr}"
                            self.graph.add_node(target, type="method_call")
                            
        except SyntaxError:
            pass
            
        return {"inventory": inventory, "complexity": complexity}

    def run_forensic_audit(self) -> Dict[str, Any]:
        vulnerabilities = []
        chart = []
        total_tk = 0
        self.ast_inventory.clear()
        self.graph.clear()

        # Diccionarios de heurística
        fallos_cognitivos = ["lo siento", "mis disculpas", "caí en la trampa", "tienes razón", "me equivoqué", "disculpa"]
        alarmas_tecnicas = ["error", "timeout", "fallo", "corrupción", "no funciona", "incidencia", "crítico"]
        
        # Detección de pereza del modelo y resúmenes ilegales
        patrones_pereza = [
            "generado en iteraciones previas", "resto del código", "código omitido", 
            "código anterior", "generado anteriormente", "sin cambios", "resto de la clase",
            "..."  # Elipsis sueltas en código
        ]

        con = self.con
        if True:
            con.execute("DELETE FROM vulns")
            rows = con.execute("SELECT * FROM history ORDER BY idx").fetchall()
            estado_error_previo = False

            for row in rows:
                idx, role, content, tk = row
                total_tk += tk
                
                # Métrica de degradación atencional (más estricta)
                decay = max(0, (total_tk - (self.max_context * 0.15))) / (self.max_context * 0.85)
                acc = max(10.0, 100 - (math.pow(decay, 1.8) * 70)) if total_tk > (self.max_context * 0.15) else 99.9
                chart.append({"turn": idx, "accumulated_tokens": total_tk, "memory_accuracy_percent": round(acc, 2)})
                
                content_lower = content.lower()

                if role == "user":
                    if any(alarma in content_lower for alarma in alarmas_tecnicas):
                        estado_error_previo = True
                
                elif role in ["model", "assistant"]:
                    ast_data = self._analyze_ast_and_graph(content)
                    
                    # 1. Detección de Pereza Algorítmica (Model Laziness)
                    if any(patron in content_lower for patron in patrones_pereza):
                        desc = "El modelo ha resumido u omitido código mediante elipsis o marcadores descriptivos. Ruptura de integridad."
                        vulnerabilities.append({"turn": idx, "severity": "CRITICAL", "type": "Evasión de Contexto", "description": desc})

                    # 2. Impacto de Grafo
                    for node in ast_data["inventory"]:
                        if self.graph.has_node(node):
                            impacto = self.graph.in_degree(node)
                            if impacto > 3:
                                desc = f"Nodo crítico '{node}' modificado. Impacto potencial en {impacto} dependencias."
                                vulnerabilities.append({"turn": idx, "severity": "HIGH", "type": "Riesgo de Impacto", "description": desc})

                    # 3. Deuda Técnica
                    if ast_data["complexity"] > 10:
                        vulnerabilities.append({"turn": idx, "severity": "HIGH", "type": "Deuda Técnica", "description": f"Complejidad Ciclomática ({ast_data['complexity']}). Posible Parche Ciego."})
                    
                    # 4. Amnesia Estructural
                    if ast_data["inventory"]:
                        lost = self.ast_inventory - ast_data["inventory"]
                        if lost and len(ast_data["inventory"]) > 0:
                            vulnerabilities.append({"turn": idx, "severity": "CRITICAL", "type": "Amnesia Estructural", "description": f"Entidades AST desaparecidas: {', '.join(lost)}"})
                        self.ast_inventory.update(ast_data["inventory"])

                    # 5. Colapso Cognitivo
                    if any(patron in content_lower for patron in fallos_cognitivos):
                        vulnerabilities.append({"turn": idx, "severity": "MEDIUM", "type": "Colapso Cognitivo", "description": "Patrón de complacencia detectado."})

                    # 6. Parche Ciego
                    if estado_error_previo:
                        vulnerabilities.append({"turn": idx, "severity": "HIGH", "type": "Parche Ciego Funcional", "description": "Bucle de error continuo. Implementación reactiva detectada."})
                        
                    estado_error_previo = False

            # Persistir vulnerabilidades
            for i, v in enumerate(vulnerabilities):
                con.execute(
                    "INSERT INTO vulns VALUES (?, ?, ?, ?)",
                    [v["turn"], v["severity"], v["type"], v["description"]]
                )

            graph_summary = {
                "nodes": list(self.graph.nodes()),
                "edges": list(self.graph.edges()),
                "critical_nodes": [n for n, d in self.graph.in_degree() if d > 2]
            }

            # Liberación activa de memoria RAM
            gc.collect()

            return {
                "meta": {"new_turns_audited": len(rows), "total_tokens_consumed": total_tk},
                "vulnerabilities": vulnerabilities,
                "chart_data": chart,
                "graph_data": graph_summary
            }


def run_forensic_analysis(chat_text: str) -> str:
    """
    Función de entrada global limpia adaptada para Pyodide (Wasm) en el navegador.
    Acepta un string (ya sea JSON o texto crudo) y devuelve los resultados formateados en JSON.
    """
    import json
    
    # 1. Intentar parsear como JSON
    try:
        data = json.loads(chat_text)
        if isinstance(data, dict) and "turns" in data:
            turns = data["turns"]
        elif isinstance(data, list):
            turns = data
        else:
            turns = [{"role": "user", "content": chat_text}]
    except Exception:
        # Fallback a parseo heurístico si es texto plano crudo
        turns = []
        lines = chat_text.split("\n")
        current_role = "user"
        current_content = []
        for line in lines:
            line_stripped = line.strip()
            line_lower = line_stripped.lower()
            if line_lower.startswith("user:") or line_lower.startswith("tú:") or line_lower.startswith("usuario:") or line_lower.startswith("**tú**:") or line_lower.startswith("**usuario**:") or line_lower.startswith("**user**:"):
                if current_content:
                    turns.append({"role": current_role, "content": "\n".join(current_content).strip()})
                current_role = "user"
                # Extraer texto tras el delimitador de rol
                parts = line.split(":", 1)
                current_content = [parts[1]] if len(parts) > 1 else []
            elif line_lower.startswith("model:") or line_lower.startswith("assistant:") or line_lower.startswith("gemini:") or line_lower.startswith("modelo:") or line_lower.startswith("**modelo**:") or line_lower.startswith("**gemini**:") or line_lower.startswith("**assistant**:"):
                if current_content:
                    turns.append({"role": current_role, "content": "\n".join(current_content).strip()})
                current_role = "model"
                # Extraer texto tras el delimitador de rol
                parts = line.split(":", 1)
                current_content = [parts[1]] if len(parts) > 1 else []
            else:
                current_content.append(line)
        if current_content:
            turns.append({"role": current_role, "content": "\n".join(current_content).strip()})
        if not turns:
            turns = [{"role": "user", "content": chat_text}]

    # 2. Purificar la estructura
    flat_turns = []
    for i, t in enumerate(turns):
        role = t.get("role", "user")
        if "parts" in t:
            content = "".join([p.get("text", "") for p in t["parts"]])
        else:
            content = t.get("content", "")
        
        # Mapear rol a 'user' o 'model'
        clean_role = "model" if any(x in str(role).lower() for x in ["model", "assistant", "modelo", "asistente"]) else "user"
        flat_turns.append({
            "role": clean_role,
            "content": content
        })

    # 3. Inicializar el motor (SQLite en memoria automático bajo Pyodide)
    engine = PMAPEngine()
    engine.ingest_structured_data(flat_turns)
    results = engine.run_forensic_audit()

    # 4. Derivar indicadores de alerta temprana (early warning)
    critical_vulns = [v for v in results.get("vulnerabilities", []) if v.get("severity") == "CRITICAL"]
    total_tokens = results.get("meta", {}).get("total_tokens_consumed", 0)

    if len(critical_vulns) > 0 or total_tokens > (0.8 * 128000):
        index = "CRITICAL"
        is_critical = True
        reason = "Se detectaron patrones de amnesia estructural o un volumen de tokens crítico que amenaza la retención del contexto."
    else:
        index = "OPTIMAL"
        is_critical = False
        reason = "Integridad estructural y retención cognitiva dentro de parámetros saludables."

    results["early_warning"] = {
        "index": index,
        "is_critical": is_critical,
        "reason": reason
    }

    return json.dumps(results, ensure_ascii=False)
