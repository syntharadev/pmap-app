# RUTA: pmap_core/pmap/license_manager.py

import os
import jwt
from datetime import datetime, timedelta
from pathlib import Path

try:
    from supabase import create_client, Client
except ImportError:
    pass

class LicenseManager:
    """
    Gestor de Licencias Sovereign Pro.
    Emite un JWT local para operar offline.
    """
    def __init__(self):
        # Clave secreta local para firmar el JWT en el NUC (fallback a clave hardcodeada si no existe en .env)
        self.secret_key = os.environ.get("PMAP_JWT_SECRET", "pmap_sovereign_k27_secret_key")
        self.token_file = Path(os.path.expanduser("~/.pmap_license.jwt"))
        self.mock_mode = os.environ.get("PMAP_MOCK_MODE", "false").lower() == "true"

    def verify_pro_license(self, license_key: str) -> bool:
        clean_key = license_key.strip()
        # Admin bypass for master license key (Offline Sovereign Validation)
        if clean_key in [
            "PMAP-PRO-OSCAR-NAVARRO-VEGAS-ADMIN",
            "PMAP-PRO-OSCARNAVARROVEGAS-ADMIN",
            "PMAP-PRO-OSCAR-NAVARRO-VEGAS"
        ]:
            return True

        if self.mock_mode:
            return clean_key.startswith("PMAP-")

        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_ANON_KEY")

        if not url or not key:
            print("[ERROR] Para validación en producción, configura SUPABASE_URL y SUPABASE_ANON_KEY")
            return False

        try:
            import requests
        except ImportError:
            print("[ERROR] Falta instalar requests/supabase")
            return False

        try:
            supabase: Client = create_client(url, key)
            # Consulta Zero-Knowledge usando el agujero de gusano RPC (evita scraping RLS)
            response = supabase.rpc("verify_license_secure", {"p_key": license_key}).execute()
            data = response.data
            
            if data and len(data) > 0:
                record = data[0]
                if record.get("tier") == "pro" and record.get("status") == "active":
                    return True
            return False
        except Exception as e:
            print(f"[ERROR] Verificación de licencia en Supabase falló: {e}")
            return False

    def activate_license(self, license_key: str) -> dict:
        if self.verify_pro_license(license_key):
            payload = {
                "tier": "PRO",
                "license_key": license_key,
                "exp": datetime.utcnow() + timedelta(days=1) # Caché de 24 horas
            }
            token = jwt.encode(payload, self.secret_key, algorithm="HS256")
            
            with open(self.token_file, "w") as f:
                f.write(token)
                
            return {"status": "success", "message": "Sovereign PRO activado localmente. Caché offline 24h."}
        else:
            return {"status": "error", "message": "Clave inválida o inactiva en el Hub Central."}

    def is_pro_active(self) -> bool:
        if not self.token_file.exists():
            return False
        try:
            with open(self.token_file, "r") as f:
                token = f.read().strip()
            jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return True
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return False