import json
import pytest
import duckdb
from pathlib import Path

# Constantes de entorno de prueba
JSON_TARGET = "TDD_Motor_Compresion_Neuronal.json"

class TestVeraIntegrity:
    """
    Suite de pruebas forenses de Antigravity.
    Inyecta la Ley de Vera sobre los artefactos JSON extraídos.
    """

    @pytest.fixture(scope="class")
    def raw_data(self):
        """Carga el JSON y verifica su existencia física (Reality Check)"""
        file_path = Path(JSON_TARGET)
        assert file_path.exists(), f"[Vera Halt] El archivo {JSON_TARGET} no existe en la ruta de ejecución."
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        assert isinstance(data, list), "[Vera Halt] Violación Estructural: El JSON raíz debe ser un Array puro."
        assert len(data) > 0, "[Vera Halt] El historial JSON está vacío."
        return data

    def test_json_schema_compliance(self, raw_data):
        """Verifica que cada nodo cumple estrictamente el esquema Pydantic"""
        for index, turn in enumerate(raw_data):
            # Comprobación de claves obligatorias
            assert "role" in turn, f"[Vera Halt] Turno {index} carece de la clave 'role'."
            assert "content" in turn, f"[Vera Halt] Turno {index} carece de la clave 'content'."
            
            # Validación de tipos y valores permitidos
            assert isinstance(turn["role"], str), f"[Vera Halt] Turno {index} 'role' no es String."
            assert isinstance(turn["content"], str), f"[Vera Halt] Turno {index} 'content' no es String."
            assert turn["role"] in ["user", "model"], f"[Vera Halt] Turno {index} posee un rol ilegal: {turn['role']}"

    def test_code_block_preservation(self, raw_data):
        """Audita que los bloques de código y las directivas PMAP no hayan sido truncados"""
        model_turns = [t for t in raw_data if t["role"] == "model"]
        
        # En una exportación de PMAP de este nivel, siempre debe haber bloques de código C++
        has_cpp_code = any("```cpp" in turn["content"] for turn in model_turns)
        assert has_cpp_code, "[Vera Halt] Amnesia detectada: No se encontraron bloques de código C++ escapados en el JSON."

        # Verificación de que no existen caracteres invisibles de truncamiento
        for turn in raw_data:
            assert "\u200b" not in turn["content"], "[Vera Halt] Carácter parasitario de Zero-Width Space detectado."

    def test_duckdb_serialization_integrity(self, raw_data):
        """Prueba de estrés: Ingesta en BD relacional efímera para verificar coherencia de tipos"""
        # Levanta DuckDB en memoria RAM exclusiva para el test (Seguro para el NUC)
        con = duckdb.connect(database=':memory:')
        
        # Esquema tabla de test
        con.execute("""
            CREATE TABLE pmap_audit_test (
                turn_id INTEGER,
                role VARCHAR,
                content_length INTEGER,
                has_code BOOLEAN
            )
        """)

        # Serialización e inyección transaccional
        con.execute("BEGIN TRANSACTION")
        for idx, turn in enumerate(raw_data):
            con.execute(
                "INSERT INTO pmap_audit_test VALUES (?, ?, ?, ?)", 
                (idx, turn["role"], len(turn["content"]), "```" in turn["content"])
            )
        con.execute("COMMIT")

        # Comprobación matemática de filas vs nodos JSON
        db_count = con.execute("SELECT COUNT(*) FROM pmap_audit_test").fetchone()[0]
        assert db_count == len(raw_data), f"[Vera Halt] Discrepancia de inyección: JSON {len(raw_data)} turnos vs BD {db_count} registros."
        
        con.close()
