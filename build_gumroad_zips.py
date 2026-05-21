#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PMAP.APP - Gumroad Release Packaging Script v1.0
Automates the local packaging of PMAP_Sovereign binaries into Indie, Professional, and Enterprise ZIP releases.
"""

import os
import shutil
import sys
from pathlib import Path

# Color codes for console output (cross-platform friendly check)
USE_COLORS = sys.platform != "win32" or "ANSICON" in os.environ or "WT_SESSION" in os.environ
GREEN = "\033[92m" if USE_COLORS else ""
BLUE = "\033[94m" if USE_COLORS else ""
YELLOW = "\033[93m" if USE_COLORS else ""
RED = "\033[91m" if USE_COLORS else ""
RESET = "\033[0m" if USE_COLORS else ""

def print_step(msg):
    print(f"{BLUE}[*]{RESET} {msg}")

def print_success(msg):
    print(f"{GREEN}[+]{RESET} {msg}")

def print_warning(msg):
    print(f"{YELLOW}[!]{RESET} {msg}")

def print_error(msg):
    print(f"{RED}[ERROR]{RESET} {msg}")

# Custom README contents per Tier
README_TEMPLATES = {
    "Indie": """========================================================================
                      NODO SOBERANO PMAP.APP - TIER INDIE
========================================================================

PMAP.APP (Plataforma de Memoria y Análisis de Proyectos) es una 
herramienta local de auditoría forense diseñada para diagnosticar y 
corregir la degradación atencional, amnesia estructural y alucinaciones 
de modelos de lenguaje (LLMs) durante sesiones de programación complejas.

Esta distribución ha sido empaquetada bajo la licencia 'INDIE' para 
ejecución soberana 100% local, garantizando privacidad absoluta (Zero-Knowledge).

------------------------------------------------------------------------
1. CARACTERÍSTICAS DEL TIER INDIE
------------------------------------------------------------------------
- Licencia individual para 1 desarrollador.
- Ejecución soberana local en 1 nodo.
- Auditoría forense estructural básica.
- Ingesta directa ilimitada mediante el inyector del navegador (Bookmarklet).
- Soporte estándar a través de SyntharaDev@gmail.com.

------------------------------------------------------------------------
2. REQUISITOS DE INSTALACIÓN
------------------------------------------------------------------------
- Un sistema compatible con la arquitectura del ejecutable.
- Una clave de API de Google Gemini (GOOGLE_API_KEY) para el motor 
  de purificación estructural.
- Una clave de licencia de Gumroad (Tier INDIE) para la activación.

------------------------------------------------------------------------
3. CONFIGURACIÓN INICIAL Y ARRANQUE
------------------------------------------------------------------------
Paso 1: Configurar la Licencia
  Crea un archivo llamado 'license.key' en el mismo directorio que el 
  ejecutable y pega dentro únicamente tu clave de Gumroad de PMAP.APP.
  Ejemplo de contenido de 'license.key':
  PMAP-INDIE-XXXX-XXXX-XXXX

Paso 2: Configurar la API Key de Gemini
  PMAP.APP utiliza Gemini para purificar los chats de IA sin pérdidas. 
  Debes exportar tu clave como variable de entorno o crear un archivo '.env' 
  junto al ejecutable con la siguiente línea:
  
    GOOGLE_API_KEY=tu_clave_de_gemini_aquí

Paso 3: Arrancar el Servidor
  Dale permisos de ejecución al binario (si estás en Linux o macOS) e inícialo:
  
    $ chmod +x PMAP_Sovereign
    $ ./PMAP_Sovereign

  El servidor levantará un nodo web interactivo local en:
  
    http://127.0.0.1:8000

========================================================================
   PMAP.APP - Mantén el control estructural y purga la amnesia de la IA.
========================================================================
""",
    "Professional": """========================================================================
                   NODO SOBERANO PMAP.APP - TIER PROFESSIONAL
========================================================================

PMAP.APP (Plataforma de Memoria y Análisis de Proyectos) es una 
herramienta local de auditoría forense diseñada para diagnosticar y 
corregir la degradación atencional, amnesia estructural y alucinaciones 
de modelos de lenguaje (LLMs) durante sesiones de programación complejas.

Esta distribución ha sido empaquetada bajo la licencia 'PROFESSIONAL' para 
ejecución soberana 100% local, garantizando privacidad absoluta (Zero-Knowledge).

------------------------------------------------------------------------
1. CARACTERÍSTICAS DEL TIER PROFESSIONAL
------------------------------------------------------------------------
- Licencia para desarrolladores profesionales y freelances.
- Ejecución soberana local de alto rendimiento.
- Auditoría forense estructural completa con análisis de grafos avanzado.
- Ingesta directa ilimitada de código y persistencia en DuckDB local.
- Soporte prioritario a través de SyntharaDev@gmail.com.

------------------------------------------------------------------------
2. REQUISITOS DE INSTALACIÓN
------------------------------------------------------------------------
- Un sistema compatible con la arquitectura del ejecutable.
- Una clave de API de Google Gemini (GOOGLE_API_KEY) para el motor 
  de purificación estructural.
- Una clave de licencia de Gumroad (Tier PROFESSIONAL) para la activación.

------------------------------------------------------------------------
3. CONFIGURACIÓN INICIAL Y ARRANQUE
------------------------------------------------------------------------
Paso 1: Configurar la Licencia
  Crea un archivo llamado 'license.key' en el mismo directorio que el 
  ejecutable y pega dentro únicamente tu clave de Gumroad de PMAP.APP.
  Ejemplo de contenido de 'license.key':
  PMAP-PRO-XXXX-XXXX-XXXX

Paso 2: Configurar la API Key de Gemini
  PMAP.APP utiliza Gemini para purificar los chats de IA sin pérdidas. 
  Debes exportar tu clave como variable de entorno o crear un archivo '.env' 
  junto al ejecutable con la siguiente línea:
  
    GOOGLE_API_KEY=tu_clave_de_gemini_aquí

Paso 3: Arrancar el Servidor
  Dale permisos de ejecución al binario (si estás en Linux o macOS) e inícialo:
  
    $ chmod +x PMAP_Sovereign
    $ ./PMAP_Sovereign

  El servidor levantará un nodo web interactivo local en:
  
    http://127.0.0.1:8000

========================================================================
   PMAP.APP - Mantén el control estructural y purga la amnesia de la IA.
========================================================================
""",
    "Enterprise": """========================================================================
                     NODO SOBERANO PMAP.APP - TIER ENTERPRISE
========================================================================

PMAP.APP (Plataforma de Memoria y Análisis de Proyectos) es una 
herramienta local de auditoría forense diseñada para diagnosticar y 
corregir la degradación atencional, amnesia estructural y alucinaciones 
de modelos de lenguaje (LLMs) durante sesiones de programación complejas.

Esta distribución ha sido empaquetada bajo la licencia 'ENTERPRISE' para 
ejecución soberana 100% local, garantizando privacidad absoluta (Zero-Knowledge).

------------------------------------------------------------------------
1. CARACTERÍSTICAS DEL TIER ENTERPRISE
------------------------------------------------------------------------
- Licencia corporativa para multi-usuario y entornos empresariales.
- Máximo rendimiento y escalabilidad con optimización avanzada de memoria RAM.
- Auditoría forense estructural total, grafos interactivos y reportes ejecutivos.
- Ingesta masiva y automatizada en pipelines locales seguros.
- Soporte dedicado 24/7 y asistencia de integración personalizada.

------------------------------------------------------------------------
2. REQUISITOS DE INSTALACIÓN
------------------------------------------------------------------------
- Un sistema compatible con la arquitectura del ejecutable.
- Una clave de API de Google Gemini (GOOGLE_API_KEY) para el motor 
  de purificación estructural.
- Una clave de licencia de Gumroad (Tier ENTERPRISE) para la activación.

------------------------------------------------------------------------
3. CONFIGURACIÓN INICIAL Y ARRANQUE
------------------------------------------------------------------------
Paso 1: Configurar la Licencia
  Crea un archivo llamado 'license.key' en el mismo directorio que el 
  ejecutable y pega dentro únicamente tu clave de Gumroad de PMAP.APP.
  Ejemplo de contenido de 'license.key':
  PMAP-ENT-XXXX-XXXX-XXXX

Paso 2: Configurar la API Key de Gemini
  PMAP.APP utiliza Gemini para purificar los chats de IA sin pérdidas. 
  Debes exportar tu clave como variable de entorno o crear un archivo '.env' 
  junto al ejecutable con la siguiente línea:
  
    GOOGLE_API_KEY=tu_clave_de_gemini_aquí

Paso 3: Arrancar el Servidor
  Dale permisos de ejecución al binario (si estás en Linux o macOS) e inícialo:
  
    $ chmod +x PMAP_Sovereign
    $ ./PMAP_Sovereign

  El servidor levantará un nodo web interactivo local en:
  
    http://127.0.0.1:8000

========================================================================
   PMAP.APP - Mantén el control estructural y purga la amnesia de la IA.
========================================================================
"""
}

def main():
    print("========================================================================")
    print("      PMAP.APP - GENERADOR DE ENTREGABLES PARA GUMROAD")
    print("========================================================================")

    # 1. Definir rutas clave
    project_root = Path(__file__).resolve().parent
    dist_dir = project_root / "dist"
    releases_dir = project_root / "releases"

    # 2. Localizar el binario compilado
    binary_name = "PMAP_Sovereign.exe" if sys.platform.startswith("win") else "PMAP_Sovereign"
    binary_path = dist_dir / binary_name

    if not binary_path.exists():
        # Búsqueda fallback de cualquier extensión en dist/ por si estamos en otro entorno
        fallback_paths = list(dist_dir.glob("PMAP_Sovereign*"))
        # Excluir directorios
        fallback_paths = [p for p in fallback_paths if p.is_file()]
        
        if fallback_paths:
            binary_path = fallback_paths[0]
            binary_name = binary_path.name
            print_warning(f"No se encontró el binario por defecto de la plataforma, usando fallback: {binary_name}")
        else:
            print_error(f"No se encontró ningún binario 'PMAP_Sovereign' en '{dist_dir}'.")
            print_error("Por favor, ejecuta 'python build_executables.py' o PyInstaller primero.")
            sys.exit(1)

    print_success(f"Binario de origen detectado: {binary_path} ({binary_path.stat().st_size / (1024*1024):.2f} MB)")

    # 3. Limpiar y recrear carpeta de lanzamientos
    if releases_dir.exists():
        print_step("Limpiando releases/ antiguos...")
        shutil.rmtree(releases_dir)
    releases_dir.mkdir(parents=True, exist_ok=True)

    # 4. Procesar cada nivel (Tier)
    tiers = ["Indie", "Professional", "Enterprise"]
    for tier in tiers:
        tier_dir = releases_dir / tier
        tier_dir.mkdir(parents=True, exist_ok=True)
        print_step(f"Empaquetando Tier: {tier}...")

        # Copiar binario
        target_binary = tier_dir / binary_name
        shutil.copy2(binary_path, target_binary)
        # Darle permisos de ejecución en Linux/Mac
        if not sys.platform.startswith("win"):
            os.chmod(target_binary, 0o755)

        # Generar README.txt personalizado
        readme_path = tier_dir / "README.txt"
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(README_TEMPLATES[tier])

        # Crear archivo ZIP de la carpeta
        # make_archive comprime todo el contenido de 'root_dir' y guarda el zip en 'base_name'
        zip_base_name = releases_dir / f"PMAP_Sovereign_{tier}"
        shutil.make_archive(
            base_name=str(zip_base_name),
            format="zip",
            root_dir=str(tier_dir)
        )
        
        zip_file = Path(f"{zip_base_name}.zip")
        print_success(f"  [+] Generado {zip_file.name} ({zip_file.stat().st_size / (1024*1024):.2f} MB)")

    print("========================================================================")
    print(f"{GREEN}[¡ÉXITO!] Todo empaquetado correctamente en 'releases/'{RESET}")
    print("========================================================================")

if __name__ == "__main__":
    main()
