import sys

def trace_execution():
    try:
        print("[1] Importando FastAPI...")
        import fastapi
        
        print("[2] Importando Uvicorn...")
        import uvicorn
        
        print("[3] Testeando extensiones C/Rust de Uvicorn (httptools / watchfiles)...")
        try:
            import httptools
            print("    -> httptools OK")
        except ImportError:
            print("    -> httptools no instalado (ignorado)")
            
        try:
            import watchfiles
            print("    -> watchfiles OK")
        except ImportError:
            print("    -> watchfiles no instalado (ignorado)")
            
        print("[4] Instanciando gramática C de Tree-sitter...")
        from tree_sitter import Language
        import tree_sitter_python
        Language(tree_sitter_python.language())
        
        print("[5] Importando el orquestador PMAP completo...")
        from pmap_core.pmap.analyzer import PMAPEngine
        
        print("[6] Instanciando el motor...")
        engine = PMAPEngine()
        
        print("\n[ÉXITO] Toda la arquitectura ha sido cargada en RAM sin colapsar el procesador.")
        
    except Exception as e:
        print(f"\n[ERROR CONTROLADO] Falló con: {e}")

if __name__ == "__main__":
    trace_execution()