import os
import sys
import subprocess
from pathlib import Path

def get_separator():
    """Devuelve el separador correcto para `--add-data` según el OS."""
    return ";" if sys.platform.startswith("win") else ":"

def run_build():
    sep = get_separator()
    
    # Archivos estáticos a incluir
    data_files = [
        f"index.html{sep}.",
        f"favicon.svg{sep}.",
        f"Logo_pmap_app.svg{sep}.",
        f"Instrucciones_PMAP_APP.html{sep}.",
        f"tests{sep}tests"
    ]
    
    # Construcción de comandos PyInstaller
    command = [
        sys.executable, "-m", "PyInstaller",
        "--name", "PMAP_Sovereign",
        "--onefile",
        "--clean",
        "--exclude-module", "cloud_server",
        "--paths", "pmap_core"
    ]
    
    # En Windows, ocultamos la consola. En otros, suele funcionar igual o usamos windowed
    if sys.platform.startswith("win"):
        command.append("--noconsole")
    else:
        command.append("--windowed")
        
    for df in data_files:
        command.extend(["--add-data", df])
        
    # Archivo principal
    command.append(str(Path("pmap_core/pmap/server.py")))
    
    print(f"Ejecutando PyInstaller en {sys.platform}...")
    print("Comando:", " ".join(command))
    
    try:
        subprocess.run(command, check=True)
        print("\n[+] Compilación terminada con éxito. El ejecutable está en la carpeta 'dist/'.")
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Error durante la compilación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_build()
