========================================================================
                      NODO SOBERANO PMAP.APP - FOSS RELEASE
========================================================================

PMAP.APP (Plataforma de Memoria y Análisis de Proyectos) es una 
herramienta local de auditoría forense diseñada para diagnosticar y 
corregir la degradación atencional, amnesia estructural y alucinaciones 
de modelos de lenguaje (LLMs) durante sesiones de programación complejas.

Esta distribución ha sido compilada bajo la licencia 'GNU AGPLv3' para 
ejecución soberana 100% local, garantizando privacidad absoluta (Zero-Knowledge).
PMAP.APP es ahora 100% gratuito y de código abierto.

------------------------------------------------------------------------
1. REQUISITOS DE INSTALACIÓN
------------------------------------------------------------------------

- Un sistema compatible con la arquitectura del ejecutable (Linux x86_64).
- Una clave de API de Google Gemini (GOOGLE_API_KEY) para el motor 
  de purificación estructural.
- Una clave de registro gratuita emitida desde https://pmap.app.

------------------------------------------------------------------------
2. ESTRUCTURA DE DIRECTORIOS
------------------------------------------------------------------------

Al iniciar el nodo, se mantendrá la siguiente topología de archivos en 
el directorio de la aplicación:

  [Raíz de PMAP.APP]
    ├── PMAP_Sovereign (Ejecutable principal)
    ├── user.key       (Archivo plano con tu email de registro gratuito)
    ├── .env           (Configuración de variables de entorno opcional)
    ├── datos_crudos/  (Carpeta permanente de almacenamiento de sesiones)
    │     ├── [Nombre_Sesion].txt  (Historial crudo)
    │     └── [Nombre_Sesion].json (Historial purificado estructurado)
    └── outputs/       (Reportes Markdown del análisis forense)

*IMPORTANTE: Todos los archivos .json extraídos o subidos se guardarán 
 permanentemente en la carpeta 'datos_crudos' en la raíz de la aplicación.*

------------------------------------------------------------------------
3. CONFIGURACIÓN INICIAL Y ARRANQUE
------------------------------------------------------------------------

Paso 1: Registrar tu Email
  1. Regístrate en https://pmap.app ingresando tu email en el formulario.
  2. Crea un archivo llamado 'user.key' en el mismo directorio que el 
     ejecutable.
  3. Abre el archivo, escribe tu dirección de correo electrónico registrada dentro y guárdalo.

Paso 2: Configurar la API Key de Gemini
  PMAP.APP utiliza Gemini para purificar los chats de IA sin pérdidas. 
  Debes exportar tu clave como variable de entorno o crear un archivo '.env' 
  junto al ejecutable con la siguiente línea:
  
    GOOGLE_API_KEY=tu_clave_de_gemini_aquí

Paso 3: Arrancar el Servidor
  Dale permisos de ejecución al binario e inícialo:
  
    $ chmod +x PMAP_Sovereign
    $ ./PMAP_Sovereign

  El servidor levantará un nodo web interactivo local en:
  
    http://127.0.0.1:8000

------------------------------------------------------------------------
4. INYECCIÓN DIRECTA (MARCADOR/BOOKMARKLET)
------------------------------------------------------------------------

PMAP.APP incluye un inyector directo compatible con navegadores Firefox y Chrome.

¿Cómo instalarlo?
  1. Abre el Dashboard web (http://127.0.0.1:8000) tras iniciar el nodo.
  2. En el panel lateral izquierdo "Inyección Directa (Firefox)", verás el
     código del marcador.
  3. Haz clic en "COPIAR" para copiar el código JavaScript al portapapeles.
  4. En tu navegador, activa la barra de marcadores (Ctrl+Shift+B).
  5. Clic derecho en la barra -> "Nuevo marcador..." (o Añadir página).
  6. Escribe un nombre intuitivo como: "🚀 Enviar a PMAP"
  7. En el campo "Dirección" o "URL", pega el código copiado.
  8. Guarda el marcador.

¿Cómo usarlo?
  1. Ve a cualquier chat de IA (ChatGPT, Claude, Gemini, etc.) que quieras auditar.
  2. Haz clic en tu marcador "🚀 Enviar a PMAP".
  3. Introduce el nombre de la sesión cuando se te solicite.
  4. ¡Listo! El chat se extraerá, estructurará en formato .json y se guardará
     directamente en la carpeta 'datos_crudos' del servidor. El análisis
     forense se actualizará automáticamente en el dashboard.

------------------------------------------------------------------------
SOPORTE Y COLABORACIÓN
------------------------------------------------------------------------

¿Tienes dudas, sugerencias o quieres reportar un caso de uso?
Contacto directo con el desarrollador: SyntharaDev@gmail.com
Repositorio oficial: https://github.com/syntharadev/pmap-app

========================================================================
   PMAP.APP - Mantén el control estructural y purga la amnesia de la IA.
========================================================================
