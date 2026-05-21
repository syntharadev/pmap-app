# Copyright (c) 2026 syntharadev (syntharadev@gmail.com)
# Todos los derechos reservados. Licencia: GNU AGPLv3
import os
import sys
from pathlib import Path

# ==========================================
# PMAP.APP - CONFIGURACIÓN Y RUTAS MAESTRAS
# ==========================================

# 1. Calculamos la raíz dinámicamente
# Si está congelado por PyInstaller, la raíz es la carpeta del ejecutable
if getattr(sys, 'frozen', False):
    PROJECT_ROOT = Path(sys.executable).resolve().parent
else:
    # __file__ es .../PMAP.APP/pmap_core/pmap/config.py
    # .parent.parent.parent sube hasta la raíz del proyecto
    CORE_MODULE_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = CORE_MODULE_DIR.parent.parent

# 2. Definición de Rutas Absolutas Inmutables
DB_PATH = str(PROJECT_ROOT / "pmap_forensic.duckdb")
OUTPUT_DIR = PROJECT_ROOT / "outputs"
DATOS_CRUDOS_DIR = PROJECT_ROOT / "datos_crudos"
HTML_PATH = str(PROJECT_ROOT / "PAMAP_APP_INICIAL.html")

# Asegurar la creación de los directorios clave
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATOS_CRUDOS_DIR.mkdir(parents=True, exist_ok=True)

# Directorio temporal para ingestas y modelos ligeros
TEMP_DIR = PROJECT_ROOT / ".tmp"
TEMP_DIR.mkdir(parents=True, exist_ok=True)
SEMANTIC_DB_PATH = str(TEMP_DIR / "pmap_rules.json")

def get_temp_file(filename: str) -> str:
    """Genera una ruta absoluta segura para archivos de ingesta."""
    return str(TEMP_DIR / filename)

