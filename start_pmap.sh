#!/bin/bash
# PMAP.APP - Script de Arranque Soberano (Sovereign Boot)

echo "=========================================="
echo " NODO PMAP.APP SOVEREIGN - INICIANDO..."
echo "=========================================="

# NUEVO: 1. Cargar variables de entorno locales (API KEY)
if [ -f .env ]; then
    echo "[+] Cargando credenciales soberanas desde .env..."
    export $(cat .env | xargs)
else
    echo "[!] ADVERTENCIA: No se encontró el archivo .env local."
fi

# 2. Verificar existencia del entorno virtual (De tu script)
if [ ! -d ".venv" ]; then
    echo "[+] Entorno virtual no detectado. Creando (.venv)..."
    python3 -m venv .venv
fi

# 3. Activar entorno virtual
echo "[+] Activando entorno virtual..."
source .venv/bin/activate

# 4. Validar e instalar dependencias (De tu script)
echo "[+] Verificando dependencias core (DuckDB, NetworkX, FastAPI)..."
pip install -r requirements.txt -q

# 5. Limpiar temporales antiguos (De tu script)
if [ -d "outputs" ]; then
    echo "[+] Purgando reportes forenses de sesiones anteriores..."
    rm -rf outputs/*
fi

# ACTUALIZADO: 6. Lanzar servidor con Uvicorn (Blindaje RAM-Safe)
# [!] SEGURIDAD: 127.0.0.1 restringe el acceso al bucle local del NUC
# [!] OPTIMIZACIÓN: --workers 1 evita la duplicación de memoria en RAM
# [!] RENDIMIENTO: --reload-dir limita el escaneo de cambios al core únicamente
echo "[+] Levantando motor de análisis en RAM..."
export PYTHONPATH="$PYTHONPATH:pmap_core"
uvicorn pmap_core.pmap.server:app --host 127.0.0.1 --port 8000 --workers 1 --reload-dir pmap_core
