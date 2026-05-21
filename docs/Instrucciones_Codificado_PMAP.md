# Instrucciones de Codificación y Preservación de Contexto - PMAP.APP

## 1. Identidad del Sistema y Rol
- **Proyecto:** PMAP.APP (Plataforma Memoria y Análisis de Proyectos).
- **Rol del Sistema:** Ingeniería Senior / Arquitecto de Sistemas Forenses.
- **Objetivo:** Actuar como orquestador de análisis post-mortem de interacciones humano-LLM para erradicar la amnesia de contexto, la degradación arquitectónica y la sobrescritura silenciosa en desarrollos de software complejos.

## 2. Restricciones de Entorno y Hardware
- **Hardware Objetivo:** Intel NUC, 8 GB de RAM.
- **SO:** Linux.
- **Entorno de Desarrollo:** Python 3.11+ ejecutándose sobre un entorno virtual aislado (`venv`).
- **Gestión de Memoria (Crítico):** Los 8 GB de RAM son un cuello de botella estricto. Se prohíbe el uso de bases de datos pesadas (Java-based o contenedores externos). El sistema debe priorizar el uso de generadores de Python y procesamiento en streaming (chunking) para no desbordar la memoria durante la ingesta.

## 3. Arquitectura de Ingesta (Dual Path)
El orquestador debe procesar el historial (`.json`) bajo dos modalidades:
1. **Histórico Masivo (Google Takeout):** JSON estructurado como Grafo Acíclico Dirigido (DAG). Exige recorrido inverso desde el "nodo hoja" actual para aislar la **ruta canónica**, descartando regeneraciones y ramas muertas.
2. **Sesión Ágil (Extensión Navegador):** Array lineal estándar (`role/content`) para escrutinios rápidos del día a día.

## 4. Stack Tecnológico "Tri-Store" (Embebido y Serverless)
Para el cruce de datos forenses se empleará exclusivamente arquitectura de bases de datos embebidas:
- **DuckDB:** Motor OLAP para almacenar el JSON inmutable, indexar metadatos (timestamps, turnos) y permitir consultas rápidas sin consumo de RAM en reposo.
- **NetworkX / Kùzu:** Motor de grafos en memoria. Su objetivo es mapear Árboles de Sintaxis Concreta (CST) y calcular dependencias cruzadas entre funciones y archivos temporales.
- **LanceDB:** Motor vectorial ligero para calcular la distancia semántica (embeddings) entre las reglas iniciales y el código final, midiendo matemáticamente el sesgo posicional ("Lost-in-the-Middle").

## 5. Lógica de Análisis Forense (Motores Core)
### A. Trazabilidad Estructural (CST)
- **Tecnología:** `tree-sitter`.
- **Directriz:** Queda prohibida la comparación de texto plano (`diff` tradicional). Las modificaciones se evaluarán compilando un Árbol de Sintaxis Concreta por cada bloque de código generado y comparando los *hashes criptográficos* de sus entidades (clases, definiciones, variables). Esto detecta funciones destruidas silenciosamente por el LLM.

### B. Cálculo de Degradación (Amnesia de Reglas)
- Las reglas de negocio se extraerán del Turno 0 mediante NLP.
- El sistema contabilizará los tokens acumulados turno a turno. Si una restricción fundacional es ignorada cuando la ventana de contexto supera el umbral de degradación (ej. > 32k tokens), se auditará como **"Evicción de Contexto"** y no como un error sintáctico.

### C. Detección de "Parches Ciegos"
- Ante iteraciones repetidas de error/corrección por parte del usuario, se medirá el gradiente de **Complejidad Ciclomática**.
- Un aumento drástico de condiciones (`if/else` anidados) sin una reestructuración de dependencias será diagnosticado automáticamente como inyección de deuda técnica (parche ciego).

## 6. Especificación de Salida: Los 9 Archivos [MEM_Project_]
La autopsia culminará en la generación determinista de 9 archivos Markdown en el directorio de salida (`/outputs/`). Su inyección de datos debe ser literal, basándose en los resultados matemáticos y lógicos de los motores, sin interpretaciones vagas de la IA:
1. `..._01_Contexto_Canonico.md`: Propósito, restricciones y topología real del grafo.
2. `..._02_Degradacion_Atencional.md`: Métricas de consumo de tokens y simulación matemática de la caída de memoria.
3. `..._03_Inventario_CST_Dependencias.md`: Mapa criptográfico activo extraído con `tree-sitter`.
4. `..._04_Calidad_y_Parches_Ciegos.md`: Diagnóstico de complejidad ciclomática y falsos positivos de solución.
5. `..._05_Grafo_Relacional_Sistema.md`: Mapa de impacto cruzado (qué rompió qué).
6. `..._06_Forense_Amnesia_Sobrescritura.md`: Listado explícito de entidades AST borradas accidentalmente.
7. `..._07_Interrogatorio_PR_CoT.md`: Extracción de la confesión técnica del LLM y restitución del bloque de código purgado.
8. `..._08_Estado_Documental_Actual.md`: Discrepancia real entre lo escrito en los `.md` de documentación y lo detectado en el AST.
9. `..._09_Manifiesto_Recuperacion.md`: El "Super-Prompt" de Estado Sólido. El compilado inmaculado para iniciar una nueva conversación y restaurar el desarrollo.

## 7. Protocolos de Ejecución Estricta
- **Precisión Milimétrica:** Absolutamente ninguna línea de código proporcionada por el orquestador puede contener omisiones del tipo `// ... código existente ...`. La restitución debe ser íntegra.
- **Validación Cruzada:** Toda reparación sugerida debe ser testeada contra el motor NetworkX/Kùzu en memoria para verificar que no deje dependencias colgadas.
- **Rutas de Entorno:** Siempre se utilizarán rutas absolutas o relativas al directorio raíz del proyecto para garantizar la trazabilidad local en Linux.

---
**NOTA CRÍTICA PARA EL LLM:** Este documento constituye la matriz de este proyecto. Representa las leyes inmutables de PMAP.APP. Cualquier respuesta, script o arquitectura futura generada deberá someterse estrictamente a estas directrices para evitar la regresión técnica.
