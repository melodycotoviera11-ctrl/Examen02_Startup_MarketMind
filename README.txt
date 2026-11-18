MarketMind BI - Examen parcial 02, TI-6900 Inteligencia de Negocios
Equipo MarketMind. Valeria Abarca Chacón, Melody Coto Viera y Pamela Cruz Segura.

TODOS LOS DATOS DE ESTE PAQUETE SON SIMULADOS. Las empresas, campañas, montos y usuarios
son ficticios y no representan resultados de ninguna empresa real.


CONTENIDO

01_LeanCanvas.pdf                          Lienzo y justificación del negocio
02_Arquitectura.pdf                        Flujo de datos, modelo dimensional, calidad y seguridad
03_Datos_Sinteticos/                       Datos simulados y su generador
    datos_brutos/                          8 archivos de origen, con anomalías a propósito
    script_python/generar_datos.py         Script de Python (semilla 2026)
    instrucciones/INSTRUCCIONES_DATOS.md   Instrucciones, diccionario de datos y semilla
    anomalias/registro_anomalias.csv       Detalle de cada anomalía y su corrección
04_Prototipo_BI.pbix                       ETL, modelo, medidas DAX y dashboards
05_Resumen_Tecnico.pdf                     Integrantes, transformaciones, medidas, hallazgos y recomendaciones
README.txt                                 Este archivo


ORDEN DE EJECUCIÓN

1. Instalar Python 3.10 o superior y las librerías
       pip install pandas numpy openpyxl

2. Generar los datos (opcional, ya vienen generados en datos_brutos)
       cd 03_Datos_Sinteticos/script_python
       python generar_datos.py
   Con la semilla 2026 se obtienen exactamente los mismos archivos.

3. Abrir 04_Prototipo_BI.pbix en Power BI Desktop.

4. Actualizar la ruta de los datos. Power BI no admite rutas relativas de forma nativa,
   por eso todas las consultas leen los archivos desde el parámetro RutaDatos.
   En Transformar datos > Administrar parámetros, cambiar RutaDatos por la ruta completa
   de la carpeta 03_Datos_Sinteticos/datos_brutos en la computadora donde se abra el archivo.
   Luego presionar Actualizar. No es necesario cambiar ninguna otra ruta.

5. Revisar las páginas Panel del cliente, Desempeño comercial y Uso y retención.


DEPENDENCIAS

Python 3.10 o superior con pandas, numpy y openpyxl
Power BI Desktop (versión de noviembre de 2026 o posterior)
Cuenta institucional con permiso de lector en el área de trabajo de Power BI Service


RUTAS RELATIVAS

Todas las rutas del paquete son relativas a la carpeta principal del .zip.
El script guarda los datos en 03_Datos_Sinteticos/datos_brutos y el registro en 03_Datos_Sinteticos/anomalias,
sin importar desde dónde se ejecute.
El archivo .pbix toma los datos desde esa misma carpeta por medio del parámetro RutaDatos.


ENLACES

Informe publicado en Power BI Service   [PENDIENTE]
Repositorio   https://github.com/melodycotoviera11-ctrl/Examen02_Startup_MarketMind


SEGURIDAD POR FILAS (RLS)

[PENDIENTE] Roles creados y cuenta de lector usada para la prueba.
