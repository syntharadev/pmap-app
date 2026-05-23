# Arquitectura Técnica: PMAP Sovereign (WebAssembly Edition)

## Filosofía del Sistema
PMAP Sovereign opera bajo un modelo de **Soberanía del Dato y Computación Descentralizada (Client-Side)**. Se elimina la necesidad de un backend centralizado para garantizar un entorno forense Audit-Safe y Zero-Knowledge.

## Componentes Tecnológicos

1. **Capa de Orquestación (HTML5/TailwindJS):** Gestiona la interfaz de usuario, la captura del archivo de entrada (Takeout/JSON/TXT) y la renderización de las métricas forenses.

2. **Capa de Cómputo Python (Pyodide Wasm):**
   Un puerto de WebAssembly para el runtime de Python. Descarga el núcleo analítico (`analyzer.py`) y ejecuta los algoritmos del *Amnesia Index* y degradación semántica directamente en el hilo del navegador.

3. **Capa de Persistencia e Inferencia SQL (DuckDB-Wasm):**
   Base de datos analítica embebida corriendo en WebAssembly. Permite realizar consultas relacionales complejas sobre los vectores de conversación utilizando el hardware local del cliente.
   *Nota de Implementación: Para maximizar la velocidad, la seguridad y la resiliencia sin dependencias pesadas en el navegador, el runtime de Pyodide utiliza SQLite3 en memoria de forma nativa para el almacenamiento y la consulta del motor analítico, garantizando velocidad extrema y aislamiento absoluto en la memoria de la pestaña del navegador.*

## Flujo del Dato (Cerrado y Aislado)
```
[Archivo Local] ──> [JS File Reader] ──> [Pyodide RAM (SQLite3)] ──> [UI Dashboard]
```
⚠️ *Ningún paquete de datos se transmite fuera del host local durante el análisis.*
