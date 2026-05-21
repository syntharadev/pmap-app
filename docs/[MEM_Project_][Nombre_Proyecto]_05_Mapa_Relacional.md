# [MEM_Project_] {Nombre_Proyecto} - Grafo de Relaciones

## 1. Matriz de Impacto Cruzado
- `config.json` -> Afecta a -> `orquestador.py` (Validado)
- `neural_oracle.hpp` -> Afecta a -> `cst_diff.py` (Enlace Roto en Turno {X})

## 2. Podredumbre de Dependencias Globales
Análisis de variables globales o configuraciones de entorno (`venv`, Dockerfiles) que el LLM dejó de trackear tras regenerar un script esclavo.