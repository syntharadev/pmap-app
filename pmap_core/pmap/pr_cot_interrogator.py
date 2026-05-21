import json
from typing import Dict, Any, List
from pydantic import BaseModel, Field

# ==========================================
# ESQUEMA DE SALIDA ESTRUCTURADA (JSON SCHEMA)
# ==========================================
# Obliga al LLM a devolver la autopsia en un formato estricto y predecible.

class AutopsiaForense(BaseModel):
    locus_of_failure_node: str = Field(
        ..., description="Identificador preciso de la función, clase o bloque donde se fracturó la integridad."
    )
    logical_consistency_assessment: str = Field(
        ..., description="Explicación del salto lógico, supresión no intencionada o conflicto de variables."
    )
    information_completeness_deficit: str = Field(
        ..., description="Reconocimiento explícito de los límites de contexto o reglas olvidadas que causaron el fallo."
    )
    algorithmic_correction_ast: str = Field(
        ..., description="Restitución en formato plano del CST reparado y purgado de la deuda técnica. Solo código."
    )

class PRCoTInterrogator:
    """
    Agente Evaluador de Cadena de Pensamiento Poli-Reflectiva.
    Aísla vulnerabilidades críticas y genera el Error Reflection Prompting (ERP).
    Preparado para conectar con IAs Locales (Ollama / Llama.cpp) para Soberanía de Datos.
    """
    def __init__(self, local_endpoint="http://localhost:11434/api/generate"):
        # Apunta por defecto a un puerto de Ollama corriendo en el NUC
        self.local_endpoint = local_endpoint

    def build_reflection_prompt(self, project_name: str, vulnerability: Dict) -> str:
        """
        Ensambla el bloque de provocación con las pruebas irrefutables del fallo.
        """
        turn = vulnerability.get("turn")
        vuln_type = vulnerability.get("type")
        desc = vulnerability.get("description")

        erp = f"""
ACTÚA COMO ARQUITECTO FORENSE Y AUDITOR DE CÓDIGO.

Se ha detectado una fractura lógica severa en el turno {turn} del proyecto '{project_name}'.
Tipo de Vulnerabilidad: {vuln_type}
Diagnóstico del Orquestador (Irrefutable): {desc}

INSTRUCCIONES DE INTERROGATORIO:
Estás obligado a evaluar este rastro de razonamiento defectuoso. No justifiques el error.
Debes identificar el punto exacto de la fractura y proporcionar la restitución íntegra de la lógica omitida.
Responde estrictamente en formato JSON siguiendo el esquema solicitado.
"""
        return erp.strip()

    def simulate_interrogation(self, erp_prompt: str) -> Dict[str, Any]:
        """
        Simulador de extracción para pruebas locales.
        En producción, aquí se hace el POST request a self.local_endpoint.
        """
        print("[!] Ejecutando interrogatorio PR-CoT (Modo Simulación)...")
        
        # Simulamos la confesión técnica que devolvería el LLM
        mock_response = {
            "locus_of_failure_node": "Función o bloque omitido durante la regeneración",
            "logical_consistency_assessment": "Asunción errónea del estado global. Sustitución de dependencias por código espagueti.",
            "information_completeness_deficit": "Evicción de contexto: olvido de reglas de negocio por degradación de memoria (>32k tokens).",
            "algorithmic_correction_ast": "# Código purificado y restituido iría aquí"
        }
        return mock_response

    def interrogate_critical_failures(self, project_name: str, vulnerabilities: List[Dict]) -> List[Dict]:
        """
        Filtra las alertas CRÍTICAS y genera una autopsia por cada una.
        """
        # Filtramos solo las vulnerabilidades que requieren restitución de código
        critical_vulns = [v for v in vulnerabilities if v.get("severity") == "CRITICAL" or v.get("type") == "Amnesia Estructural"]
        confessions = []

        for vuln in critical_vulns:
            erp = self.build_reflection_prompt(project_name, vuln)
            
            # Aquí cambiamos a ejecución real cuando tengas un modelo local corriendo
            confession = self.simulate_interrogation(erp)
            confession["turn_associated"] = vuln.get("turn")
            confession["original_alert"] = vuln.get("description")
            confessions.append(confession)

        return confessions

if __name__ == "__main__":
    # Prueba aislada
    agent = PRCoTInterrogator()
    sample_vuln = {"turn": 42, "type": "Amnesia Estructural", "severity": "CRITICAL", "description": "Se borró la función guardar_db()"}
    prompt = agent.build_reflection_prompt("PMAP_Core", sample_vuln)
    print("PROMPT ERP GENERADO:\\n", prompt)
    print("\\nCONFESIÓN EXTRAÍDA:\\n", json.dumps(agent.simulate_interrogation(prompt), indent=2))