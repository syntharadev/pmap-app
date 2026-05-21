import duckdb
import os
from pmap.config import DB_PATH

def setup_tri_store(db_path=DB_PATH):
    """
    Inicializa el Almacén Documental con tipología estricta.
    El Triple Almacén se completa con el Almacén Semántico (JSON/Vector)
    y el Almacén de Grafos (GraphML).
    """
    print(f"[*] Configurando Triple Almacén en: {db_path}")
    con = duckdb.connect(db_path)
    
    # Tabla de Ruta Canónica (Persistencia de la disección de grafos)
    con.execute("""
        CREATE TABLE IF NOT EXISTS canonical_route (
            turn_index INTEGER PRIMARY KEY,
            role VARCHAR CHECK (role IN ('user', 'model', 'assistant')),
            content TEXT NOT NULL,
            token_count INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabla de Vulnerabilidades (Autopsia Forense)
    con.execute("""
        CREATE TABLE IF NOT EXISTS vulnerabilities (
            vuln_id INTEGER PRIMARY KEY,
            turn_index INTEGER,
            severity VARCHAR CHECK (severity IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW')),
            type VARCHAR,
            description TEXT,
            FOREIGN KEY (turn_index) REFERENCES canonical_route(turn_index)
        )
    """)
    
    # Tabla de Entidades CST (Inventario Tree-sitter)
    con.execute("""
        CREATE TABLE IF NOT EXISTS cst_entities (
            entity_id VARCHAR PRIMARY KEY,
            name VARCHAR,
            type VARCHAR,
            hash_cst VARCHAR,
            last_turn INTEGER
        )
    """)
    
    con.close()
    print("[OK] Esquemas de base de datos creados exitosamente.")

if __name__ == "__main__":
    setup_tri_store()
