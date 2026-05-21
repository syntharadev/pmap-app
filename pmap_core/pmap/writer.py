import os
from pathlib import Path
from pmap.config import OUTPUT_DIR

class ForensicReportWriter:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)

    def _build_interrogation_prompt(self, vulns: list) -> str:
        target_vulns = [v for v in vulns if v["type"] in ["Parche Ciego Funcional", "Deuda Técnica", "Amnesia Estructural", "Evasión de Contexto"]]
        content = "# Interrogatorio Técnico (PR-CoT)\n\n"
        
        if not target_vulns:
            return content + "No se detectaron anomalías estructurales que requieran interrogatorio. Arquitectura estable."

        marker = chr(96) * 3
        content += "Copia el siguiente bloque y ejecútalo en el LLM para forzar la restitución del estado sólido:\n\n"
        content += f"{marker}text\n[SYSTEM OVERRIDE: PR-CoT INTERROGATION]\n"
        content += "Rol: Arquitecto Forense bajo auditoría estricta.\n"
        content += "Contexto: El sistema PMAP ha detectado las siguientes vulnerabilidades introducidas en la sesión:\n\n"
        
        for v in target_vulns:
            content += f"- Turno {v['turn']} | {v['type']}: {v['description']}\n"
            
        content += "\nEjecuta obligatoriamente los siguientes pasos (Chain of Thought):\n"
        content += "1. CONFESIÓN: Explica analíticamente por qué tomaste la decisión de aplicar un parche ciego o borrar entidades estructurales en lugar de refactorizar la causa raíz.\n"
        content += "2. RESTITUCIÓN: Analiza el impacto de los nodos afectados y proporciona el código completo de los módulos implicados resolviendo la deuda técnica.\n"
        content += "3. INTEGRIDAD: Queda estrictamente prohibido usar comentarios tipo `// código existente` o similares. Entrega la estructura íntegra.\n"
        content += f"{marker}\n"
        
        return content

    def _build_restoration_manifest(self, payload: dict) -> str:
        nodes = payload.get("graph_data", {}).get("nodes", [])
        
        content = "# Super-Prompt de Estado Sólido\n\n"
        content += "> **Instrucción Operativa:** Inyecta este bloque en una NUEVA sesión del LLM. Esto purgará la degradación de memoria del historial previo, forzando a la IA a retomar el trabajo basándose únicamente en las dependencias validadas.\n\n"
        
        marker = chr(96) * 3
        content += f"{marker}text\n[SYSTEM OVERRIDE: INICIALIZACIÓN DE ESTADO SÓLIDO]\n"
        content += "Rol: Arquitecto de Software Senior.\n"
        content += "Objetivo: Retomar el desarrollo de este proyecto desde un estado estable, con la ventana de contexto reseteada y purgando iteraciones fallidas previas.\n\n"
        content += "## 1. Inventario Estructural Activo (AST Canónico)\n"
        content += "El sistema cuenta actualmente con las siguientes entidades validadas en producción:\n"
        
        if nodes:
            for node in nodes:
                content += f"- {node}\n"
        else:
            content += "- (Sin dependencias estructurales detectadas en la última iteración)\n"
            
        content += "\n## 2. Leyes de Continuación Innegociables\n"
        content += "A. AMNESIA CERO: Queda estrictamente prohibido degradar, omitir o eliminar las entidades listadas en el Inventario AST.\n"
        content += "B. PROHIBICIÓN DE PARCHES: Si encuentras un error, analiza la causa raíz estructural. No apliques parches iterativos ciegos.\n"
        content += "C. CÓDIGO ÍNTEGRO: Entregarás bloques de código completos y funcionales. El uso de comentarios como `// resto del código` resultará en un fallo crítico.\n\n"
        content += "Confirma la ingesta de este estado sólido respondiendo ÚNICAMENTE con: 'ESTADO SÓLIDO ACEPTADO. Sistemas listos para la siguiente instrucción.'\n"
        content += f"{marker}\n"
        
        return content

    def generate_all_reports(self, project_name: str, payload: dict) -> str:
        base = f"[MEM_Project_]{project_name}"
        vulns = payload.get("vulnerabilities", [])
        tk = payload.get("meta", {}).get("total_tokens_consumed", 0)
        g_data = payload.get("graph_data", {})

        # 05. Mapa de Impacto
        impact_content = "# Mapa de Impacto Cruzado\n\n## Nodos Críticos Identificados\n"
        for node in g_data.get("critical_nodes", []):
            impact_content += f"- **{node}**: Alta dependencia detectada.\n"
        impact_content += "\n## Relaciones de Dependencia (Grafo)\n"
        for edge in g_data.get("edges", []):
            impact_content += f"- `{edge[0]}` depende de `{edge[1]}`\n"

        # Generación Dinámica
        interrogation_content = self._build_interrogation_prompt(vulns)
        restoration_content = self._build_restoration_manifest(payload)

        files = {
            "01_Contexto_Canonico.md": f"# Topología Canónica\nTokens Totales Consumidos: {tk}",
            "02_Degradacion_Atencional.md": "# Métricas de Caída de Memoria\n" + "\n".join([f"- Turno {p['turn']}: {p['accumulated_tokens']} tk -> {p['memory_accuracy_percent']}%" for p in payload.get("chart_data", [])]),
            "03_Inventario_AST_Dependencias.md": f"# Mapa Criptográfico AST\nEntidades detectadas: {', '.join(g_data.get('nodes', []))}",
            "04_Calidad_y_Deuda_Tecnica.md": "# Calidad Arquitectónica\n" + "\n".join([f"- Turno {v['turn']}: [{v['type']}] {v['description']}" for v in vulns if v["type"] in ["Deuda Técnica", "Parche Ciego Funcional", "Evasión de Contexto"]]),
            "05_Mapa_Impacto_Sistema.md": impact_content,
            "06_Forense_Sobrescritura.md": "# Amnesia Estructural\n" + "\n".join([f"- Turno {v['turn']}: {v['description']}" for v in vulns if v["type"] == "Amnesia Estructural"]),
            "07_Confesion_Tecnica.md": interrogation_content,
            "08_Discrepancia_Documental.md": "# Discrepancias Documentales\nComparativa automática en curso.",
            "09_Manifiesto_Restauracion.md": restoration_content
        }

        for suffix, content in files.items():
            with open(self.output_dir / f"{base}_{suffix}", "w", encoding="utf-8") as f:
                f.write(content)

        return str(self.output_dir)
