========================================================================
                      NODO SOBERANO PMAP.APP - BROWSER RELEASE
========================================================================

PMAP.APP (Plataforma de Memoria y Análisis de Proyectos) es una 
herramienta local de auditoría forense diseñada para diagnosticar y 
corregir la degradación atencional, amnesia estructural y alucinaciones 
de modelos de lenguaje (LLMs) durante sesiones de programación complejas.

Esta distribución ha sido adaptada para ejecución soberana 100% en el 
navegador (Client-Side), garantizando privacidad absoluta (Zero-Knowledge).
PMAP.APP es 100% gratuito, de código abierto y libre de dependencias de red.

------------------------------------------------------------------------
1. ARQUITECTURA SOBERANA (CLIENT-SIDE)
------------------------------------------------------------------------

A diferencia de las versiones tradicionales basadas en servidores backend
locales o peticiones en la nube, esta edición corre enteramente dentro de tu 
navegador mediante WebAssembly:

- Pyodide: Entorno virtual de Python compilado para ejecutarse en el navegador.
- SQLite: Motor relacional embebido local para análisis de transacciones.
- NetworkX: Librería matemática para el análisis del grafo de dependencias AST.

Tus datos (historiales de chat y código) nunca viajan por internet,
procesándose directamente en la memoria RAM local.

------------------------------------------------------------------------
2. INSTRUCCIONES DE USO EN 3 PASOS
------------------------------------------------------------------------

Paso 1: Obtén tu evidencia (Bookmarklet Extractor)
  1. Activa la barra de marcadores en tu navegador (Ctrl+Shift+B o Cmd+Shift+B).
  2. Haz clic derecho sobre ella y selecciona "Nuevo marcador..." o "Añadir página...".
  3. Asígnale el nombre: "🚀 PMAP Extract".
  4. En el campo "URL" o "Dirección", pega el código del bookmarklet disponible
     en el panel lateral de PMAP.APP (o en Instrucciones_PMAP_APP.html).
  5. Ve a tu chat activo con la IA (ChatGPT, Claude, Gemini) y haz clic en
     el marcador. Purificará el historial y lo descargará como un archivo '.json'.
  *(También puedes subir exportaciones oficiales de ChatGPT o Google Takeout).*

Paso 2: Carga tu archivo
  1. Abre el panel de PMAP.APP en tu navegador.
  2. Arrastra y suelta o sube el archivo '.json' descargado utilizando el
     cajón de entrada analítica de la web.

Paso 3: Auditoría Forense
  1. El motor de WebAssembly procesará de forma inmediata las métricas.
  2. Observa el índice de degradación atencional, el mapa de amnesia AST y
     las vulnerabilidades detectadas cronológicamente en el feed de auditoría.

------------------------------------------------------------------------
3. CÓMO LEVANTAR EL NODO LOCALMENTE
------------------------------------------------------------------------

PMAP.APP no requiere un backend de Python activo ni base de datos externa.
Puedes ejecutar la interfaz web estática de tres formas sencillas:

Opción A: Servidor Web Local (Recomendado)
  Levanta un servidor estático rápido desde la terminal en el directorio raíz:

    $ python3 -m http.server 8080

  Y abre tu navegador en: http://localhost:8080

Opción B: GitHub Pages / Alojamiento Estático
  Simplemente sube este repositorio a tu cuenta de GitHub, habilita GitHub Pages
  desde la pestaña "Settings -> Pages", ¡y listo! Se desplegará automáticamente.

Opción C: Apertura Directa
  Incluso puedes hacer doble clic sobre 'index.html' en tu gestor de archivos
  y el motor correrá localmente sin levantar ningún servidor web.

------------------------------------------------------------------------
SOPORTE Y COLABORACIÓN
------------------------------------------------------------------------

¿Tienes dudas, sugerencias o quieres reportar un caso de uso?
Contacto directo con el desarrollador: SyntharaDev@gmail.com
Repositorio oficial: https://github.com/syntharadev/pmap-app

========================================================================
   PMAP.APP - Mantén el control estructural y purga la amnesia de la IA.
========================================================================
