import json
from pmap_core.pmap.analyzer import PMAPEngine
from pmap_core.pmap.config import get_temp_file

def test_deteccion_amnesia():
    print("=== TEST DE ESTRÉS FORENSE: DETECCIÓN DE AMNESIA ===")
    
    # 1. Creamos un historial JSON simulado con un fallo estructural
    # Turno 0: El usuario define una regla y código base.
    # Turno 1: La IA reescribe el código pero BORRA una función.
    test_chat = [
        {
            "role": "user",
            "content": "Crea un motor de base de datos. Regla: Debe ser embebida."
        },
        {
            "role": "model",
            "content": "Aquí tienes:\n
http://googleusercontent.com/immersive_entry_chip/0
http://googleusercontent.com/immersive_entry_chip/1

### 2. Flujo de Trabajo con TabularisDB
1. Ejecuta tu análisis desde el Dashboard (`http://localhost:8000`) o el CLI (`python cli.py archivo.json`).
2. Abre **TabularisDB** en tu NUC.
3. Conecta al driver **DuckDB** y abre el archivo `pmap_forensic.duckdb`.
4. Ejecuta: `SELECT * FROM vulnerabilities WHERE severity = 'CRITICAL';` para ver la autopsia en tiempo real.

### 3. Recuperación de Proyectos
Cuando la IA colapse, no intentes arreglarlo en el mismo chat. 
1. Ve a la carpeta `outputs/`.
2. Abre el archivo `[MEM_Project_]..._09_Manifiesto_Recuperacion.md`.
3. Copia el **Super-Prompt de Estado Sólido** y pégalo en una nueva conversación para restaurar la integridad del código.

---

**¿Falta algo más?**
Con la **Purificación Retrospectiva** instalada, el motor ha alcanzado la madurez necesaria para procesar tus conversaciones reales con precisión milimétrica[cite: 89, 90]. El Triple Almacén está activo, el CLI es funcional y tienes herramientas de auditoría externa (TabularisDB) y interna (`audit_verify.py`).

¿Deseas realizar ahora la prueba de fuego inyectando tu archivo `conversations.json` real para ver cómo el sistema reconstruye la **Ruta Canónica**? [cite: 7, 12, 113]