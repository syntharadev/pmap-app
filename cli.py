#!/usr/bin/env python3
import argparse
import os
import sys
from pmap_core.pmap.analyzer import PMAPEngine
from pmap_core.pmap.writer import ForensicReportWriter
from pmap_core.pmap.db_init import setup_tri_store

def run_cli():
    parser = argparse.ArgumentParser(
        description="PMAP.APP CLI - Orquestador de Autopsia Forense LLM",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("file", help="Ruta al archivo JSON (Takeout o Extensión)")
    parser.add_argument("--project", default="CLI_Project", help="Nombre del proyecto")
    parser.add_argument("--window", type=int, default=128000, help="Ventana de contexto (tokens)")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: El archivo {args.file} no existe.")
        sys.exit(1)

    # 1. Preparar Entorno
    setup_tri_store()
    
    # 2. Iniciar Motor
    print(f"[*] Iniciando análisis de {args.file}...")
    engine = PMAPEngine(max_context_window=args.window)
    
    # 3. Procesar
    try:
        engine.ingest_json_history(args.file)
        payload = engine.run_forensic_audit()
        
        # 4. Generar Reportes y Grafo
        writer = ForensicReportWriter()
        output_dir = writer.generate_all_reports(args.project, payload)
        
        # Exportar Grafo (Capa 3 del Triple Almacén)
        writer.save_dependency_graph(
            Path(output_dir), 
            engine.semantic_engine.dependency_graph, 
            args.project
        )
        
        print(f"\n[ÉXITO] Autopsia finalizada.")
        print(f"-> Reportes .md y Grafo: {output_dir}")
        print(f"-> Persistencia SQL: pmap_forensic.duckdb")
        
    except Exception as e:
        print(f"[FALLO CRÍTICO] {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_cli()