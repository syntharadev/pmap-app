# [MEM_Project_] {Nombre_Proyecto} - Calidad Arquitectónica y Deuda

## 1. Gradiente de Complejidad Ciclomática
Mide cómo se ensució una función tras repetidos errores del usuario.
- **Función:** `parser_logica()`
  - Turno 10: Complejidad 4 (Código Limpio)
  - Turno 15: Complejidad 12 (Posible Parche Ciego)
  - **Veredicto Forense:** El LLM apiló bucles `if/else` anidados en lugar de refactorizar la abstracción. Deuda técnica inyectada.

## 2. Falsos Positivos de Validación
Listado de turnos donde la IA afirmó "Problema resuelto" pero el análisis AST demuestra que el parche es ciego o puramente cosmético.