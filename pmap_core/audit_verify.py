import duckdb
import os
from pathlib import Path

def verificar_integridad_forense(db_path="pmap_forensic.duckdb", output_path="outputs"):
    print("=== AUDITORÍA DE INTEGRACIÓN PMAP.APP ===")
    
    # 1. Comprobar Base de Datos (DuckDB)
    if not os.path.exists(db_path):
        print("[FAIL] Base de Datos DuckDB no encontrada.")
        return
    
    con = duckdb.connect(db_path)
    turns = con.execute("SELECT COUNT(*) FROM canonical_route").fetchone()[0]
    vulns = con.execute("SELECT COUNT(*) FROM vulnerabilities").fetchone()[0]
    print(f"[OK] DuckDB activa: {turns} turnos y {vulns} vulnerabilidades registradas.")
    con.close()

    # 2. Comprobar Reportes .md
    out_dir = Path(output_path)
    last_run = sorted(out_dir.glob("*"))[-1] if list(out_dir.glob("*")) else None
    
    if last_run:
        files = list(last_run.glob("*.md"))
        print(f"[OK] Última autopsia: {last_run.name} ({len(files)}/9 archivos generados).")
        if len(files) < 9:
            print(f"[WARN] Faltan {9 - len(files)} archivos en el reporte.")
    else:
        print("[WARN] No se han generado archivos de salida aún.")

if __name__ == "__main__":
    verificar_integridad_forense()