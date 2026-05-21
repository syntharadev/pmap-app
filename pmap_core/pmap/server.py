import os
import gc
import json
import hmac
import hashlib
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, Request, Header, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from google import genai
from google.genai import types

# Importaciones de tu motor analítico existente
from pmap.analyzer import PMAPEngine
from pmap.parser import ForensicJSONParser
from pmap.writer import ForensicReportWriter
from pmap.license_manager import LicenseManager

# --- SINGLETON: Cliente Gemini reutilizable (evita reconexiones por cada petición) ---
_gemini_client = None

def _get_gemini_client():
    """Inicializa el cliente Gemini una sola vez y lo reutiliza."""
    global _gemini_client
    if _gemini_client is None:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="Falta la configuración de GOOGLE_API_KEY en el servidor.")
        _gemini_client = genai.Client(api_key=api_key)
    return _gemini_client

app = FastAPI(title="PMAP.APP Sovereign Node", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import sys
# Resolver ruta base para servir frontend (PyInstaller extrae en sys._MEIPASS)
if getattr(sys, 'frozen', False):
    frontend_dir = sys._MEIPASS
else:
    # Si se corre en local, ir al root del proyecto
    frontend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/{filename}")
def serve_static(filename: str):
    allowed_files = ["favicon.svg", "Logo_pmap_app.svg", "Instrucciones_PMAP_APP.html"]
    if filename in allowed_files:
        path = os.path.join(frontend_dir, filename)
        if os.path.exists(path):
            return FileResponse(path)
    raise HTTPException(status_code=404, detail="File not found")

# Estado global de la aplicación (100% libre y registrado)
APP_STATE = {
    "is_pro": True
}

# --- ESQUEMAS ESTRICTOS PARA EL PIPELINE DE GEMINI ---
class ChatTurn(BaseModel):
    role: str = Field(description="El rol del emisor: 'user' o 'model'")
    content: str = Field(description="El texto literal, comandos o bloques de código íntegros de ese turno")

class ChatHistory(BaseModel):
    turns: List[ChatTurn] = Field(description="Lista completa y ordenada cronológicamente de las intervenciones")

class LicenseRequest(BaseModel):
    license_key: str

# --- MIDDLEWARE ZERO-KNOWLEDGE: Verificación (Mantenido por compatibilidad de tipos) ---
def verify_pro_access():
    """Bypass total. La herramienta es 100% gratuita y abierta una vez iniciado el nodo."""
    return True

# --- UTILIDAD: Ejecutar auditoría protegida con liberación de RAM ---
def _ejecutar_auditoria_protegida(flat_turns: list, safe_project_name: str) -> dict:
    """Ejecuta el motor analítico con blindaje estricto de memoria."""
    engine = PMAPEngine()
    engine.ingest_structured_data(flat_turns)
    results = engine.run_forensic_audit()

    # Generación automática de reportes Markdown (.md)
    writer = ForensicReportWriter()
    out_dir = writer.generate_all_reports(safe_project_name, results)

    results["system_meta"] = {
        "project": safe_project_name,
        "reports_dir": out_dir,
        "turns_processed": len(flat_turns)
    }

    # Liberación activa de memoria RAM
    del engine
    del writer
    gc.collect()

    return results


# --- ENDPOINT: INGESTA AUTOMÁTICA (Bookmarklet Firefox / Auto-Analyze) ---
# [FIX] Cambiado de 'async def' a 'def' para evitar el bloqueo del Event Loop.
# FastAPI delega automáticamente las funciones síncronas a un ThreadPool interno,
# manteniendo el servidor receptivo mientras se ejecutan las operaciones pesadas
# (Gemini API, DuckDB, escritura de archivos).
@app.post("/api/v1/audit/auto-analyze")
def auto_analyze(
    project_name: str = Form(...),
    raw_text: str = Form(...)
):
    try:
        # 1. Obtener cliente Gemini reutilizable (singleton)
        client = _get_gemini_client()

        # 2. Sanitizar el nombre del archivo y crear directorios de persistencia
        safe_project_name = "".join([c for c in project_name if c.isalpha() or c.isdigit() or c in " _-"]).strip()
        if not safe_project_name:
            safe_project_name = "sin_nombre"
        
        from pmap.config import DATOS_CRUDOS_DIR, OUTPUT_DIR
        DATOS_CRUDOS_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        # 3. Guardar automáticamente el archivo de texto crudo con el nombre del usuario
        raw_file_path = str(DATOS_CRUDOS_DIR / f"{safe_project_name}.txt")
        with open(raw_file_path, "w", encoding="utf-8") as f:
            f.write(raw_text)

        # 4. Purificación estructural con Gemini (conexión reutilizada)
        system_prompt = """
        Rol: Serializador JSON Forense. Convierte el chat suministrado en un array JSON válido.
        Reglas: No resumas, vuelca los bloques de código C++/Python íntegros, elimina metadatos parasitarios de la web.
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{system_prompt}\n\nHistorial a procesar:\n{raw_text}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ChatHistory,
                temperature=0.0,          # Rigidez matemática absoluta
                max_output_tokens=65536   # [FIX] Ampliado de 4096 a 65536 para evitar truncado silencioso en chats largos
            )
        )

        # 5. Procesar la respuesta estructurada
        structured_data = json.loads(response.text.strip())
        flat_turns = structured_data.get("turns", [])

        # Guardar el JSON purificado para el registro forense local en la carpeta datos_crudos
        json_file_path = str(DATOS_CRUDOS_DIR / f"{safe_project_name}.json")
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(flat_turns, f, indent=2, ensure_ascii=False)

        # 6. Inyección automática en el motor de análisis PMAP (DuckDB / Grafos)
        results = _ejecutar_auditoria_protegida(flat_turns, safe_project_name)
        results["system_meta"]["raw_saved"] = raw_file_path
        results["system_meta"]["json_saved"] = json_file_path

        # 7. Lógica del Paywall (Eliminada - Todo Abierto)
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

        return JSONResponse(content=results)

    except HTTPException:
        raise
    except Exception as e:
        gc.collect()
        return JSONResponse(content={"error": f"Fallo en el pipeline automatizado: {str(e)}"}, status_code=500)


# --- ENDPOINT: SUBIDA MANUAL DE JSON (Dashboard) ---
# [FIX] Mantenemos 'async def' aquí porque UploadFile.read() es un método
# asíncrono nativo de Starlette. Es la ÚNICA operación async real del endpoint.
# El resto del procesado pesado (DuckDB) se delega a un hilo secundario.
@app.post("/api/v1/audit/upload")
async def audit_upload(file: UploadFile = File(...)):
    """
    Recibe un archivo .json con el historial del chat ya estructurado.
    Procesa la auditoría forense completa y devuelve los resultados.
    """
    try:
        # 1. Leer y parsear el archivo JSON (operación async nativa de Starlette)
        raw_bytes = await file.read()
        text = raw_bytes.decode("utf-8")
        
        # json.loads con strict=False para tolerar caracteres de control
        data = json.loads(text, strict=False)

        # 2. Normalizar formato (soportar Google Takeout, array plano, etc.)
        parser = ForensicJSONParser()
        
        if isinstance(data, list):
            flat_turns = parser.purify_json_data(data)
        elif isinstance(data, dict) and "turns" in data:
            flat_turns = parser.purify_json_data(data["turns"])
        else:
            raise ValueError("Formato JSON no reconocido. Se espera un array o un objeto con clave 'turns'.")

        if not flat_turns:
            return JSONResponse(content={"error": "El archivo no contiene turnos válidos."}, status_code=400)

        # 3. Derivar nombre de proyecto del archivo
        safe_name = Path(file.filename).stem if file.filename else "upload"
        safe_name = "".join([c for c in safe_name if c.isalpha() or c.isdigit() or c in " _-"]).strip() or "upload"

        # Guardar una copia del JSON cargado en la carpeta de datos crudos en la raíz
        from pmap.config import DATOS_CRUDOS_DIR
        DATOS_CRUDOS_DIR.mkdir(parents=True, exist_ok=True)
        json_file_path = str(DATOS_CRUDOS_DIR / f"{safe_name}.json")
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(flat_turns, f, indent=2, ensure_ascii=False)

        # 4. Ejecutar auditoría protegida (delegada a ThreadPool para no bloquear el Event Loop)
        import asyncio
        results = await asyncio.to_thread(_ejecutar_auditoria_protegida, flat_turns, safe_name)

        # 5. Lógica del Paywall (Eliminada - Todo Abierto)
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

        return JSONResponse(content=results)

    except json.JSONDecodeError as e:
        return JSONResponse(content={"error": f"JSON inválido: {str(e)}"}, status_code=400)
    except Exception as e:
        gc.collect()
        return JSONResponse(content={"error": f"Fallo en el análisis: {str(e)}"}, status_code=500)


# --- ENDPOINTS DE REGISTRO / COMPATIBILIDAD ---
@app.post("/api/v1/license/activate")
def activate_license(req: LicenseRequest):
    # Todo nodo iniciado ya ha validado su registro
    return JSONResponse(content={"status": "success", "message": "Nodo verificado y activo."})

@app.get("/api/v1/license/status")
def license_status():
    return JSONResponse(content={"is_pro": True})

@app.get("/api/v1/config/supabase")
def get_supabase_config():
    return {
        "url": os.environ.get("SUPABASE_URL", "https://TU_PROYECTO.supabase.co"),
        "anon_key": os.environ.get("SUPABASE_ANON_KEY", "eyJ_AQUÍ_VA_TU_ANON_KEY")
    }

def verify_user_registration():
    from pmap.config import PROJECT_ROOT
    key_path = PROJECT_ROOT / "user.key"
    
    print("==========================================")
    print(" NODO PMAP.APP SOVEREIGN - INICIANDO...")
    print("==========================================")
    
    # Cargar .env manualmente si existe
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if "=" in line:
                            k, v = line.split("=", 1)
                            os.environ[k.strip()] = v.strip().strip("'\"")
        except Exception:
            pass
                        
    email_value = None
    if key_path.exists():
        try:
            with open(key_path, "r", encoding="utf-8") as f:
                email_value = f.read().strip()
        except Exception as e:
            print(f"[!] Error leyendo user.key: {e}")
            
    # Fallbacks de compatibilidad por si se usaban formatos anteriores
    if not email_value:
        for old_file in ["user_token.key", "license.key"]:
            old_path = PROJECT_ROOT / old_file
            if old_path.exists():
                try:
                    with open(old_path, "r", encoding="utf-8") as f:
                        val = f.read().strip()
                        if val:
                            email_value = val
                            break
                except Exception:
                    pass

    if not email_value:
        print("[!] Archivo 'user.key' no encontrado o vacío.")
        print("\n==========================================")
        print("Por favor, regístrate gratis en https://pmap.app para obtener acceso")
        print("==========================================\n")
        import sys
        sys.exit(1)

    # Admin / Local bypass
    mock_mode = os.environ.get("PMAP_MOCK_MODE", "false").lower() == "true"
    if email_value in [
        "PMAP-PRO-OSCAR-NAVARRO-VEGAS-ADMIN",
        "PMAP-PRO-OSCARNAVARROVEGAS-ADMIN",
        "PMAP-PRO-OSCAR-NAVARRO-VEGAS",
        "test@pmap.app",
        "admin@pmap.app",
        "FREE-OPEN-SOURCE-TOKEN"
    ] or "@" not in email_value:
        print(f"✅ Acceso autorizado para [Bypass local: {email_value}]")
        return

    if mock_mode:
        print(f"✅ Acceso autorizado para [Modo simulado: {email_value}]")
        return

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY")

    if not url or not key or "TU_PROYECTO" in url:
        print("[!] SUPABASE_URL o SUPABASE_ANON_KEY no configurados en .env.")
        print("\n==========================================")
        print("Por favor, regístrate gratis en https://pmap.app para obtener acceso")
        print("==========================================\n")
        import sys
        sys.exit(1)

    try:
        from supabase import create_client, Client
        supabase: Client = create_client(url, key)
        
        # Consultar si el email existe en la tabla registered_users
        response = supabase.table("registered_users").select("id").eq("email", email_value).execute()
        
        if response.data and len(response.data) > 0:
            print(f"✅ Acceso autorizado para [{email_value}]")
            return
        else:
            print(f"[!] El correo '{email_value}' no está registrado en la base de datos.")
            print("\n==========================================")
            print("Por favor, regístrate gratis en https://pmap.app para obtener acceso")
            print("==========================================\n")
            import sys
            sys.exit(1)
            
    except Exception as e:
        print(f"[!] Error de conexión con Supabase: {e}")
        print("\n==========================================")
        print("Por favor, regístrate gratis en https://pmap.app para obtener acceso")
        print("==========================================\n")
        import sys
        sys.exit(1)

# Ejecutar validación inmediata al importar el módulo
verify_user_registration()

if __name__ == "__main__":
    import uvicorn
    import shutil
    from pmap.config import OUTPUT_DIR
    
    # Limpieza de reportes anteriores
    if OUTPUT_DIR.exists():
        print("[+] Purgando reportes forenses de sesiones anteriores...")
        for filename in os.listdir(OUTPUT_DIR):
            file_path = OUTPUT_DIR / filename
            try:
                if file_path.is_file() or file_path.is_symlink():
                    file_path.unlink()
                elif file_path.is_dir():
                    shutil.rmtree(file_path)
            except Exception as e:
                pass

    print("[+] Levantando motor de análisis forense libre en RAM (http://127.0.0.1:8000)...")
    uvicorn.run(app, host="127.0.0.1", port=8000, workers=1)