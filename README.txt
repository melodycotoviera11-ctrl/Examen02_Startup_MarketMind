MarketMind BI - Examen parcial 02, TI-6900 Inteligencia de Negocios
Equipo MarketMind. Valeria Abarca Chacón, Melody Coto Viera y Pamela Cruz Segura.

TODOS LOS DATOS DE ESTE PAQUETE SON SIMULADOS. Las empresas, campañas, montos y usuarios
son ficticios y no representan resultados de ninguna empresa real.


CONTENIDO DEL PAQUETE

01_LeanCanvas/01_LeanCanvas.pdf            Lienzo y justificación del negocio
02_Arquitectura/02_Arquitectura.pdf        Flujo de datos, modelo dimensional, calidad y seguridad
03_Datos_Sinteticos/                       Script generador, datos brutos e instrucciones
    generar_datos.py                       Script de Python (semilla 2026)
    INSTRUCCIONES_DATOS.md                 Diccionario de datos y anomalías sembradas
    datos_brutos/                          8 archivos de origen con errores a propósito
    documentacion/registro_anomalias.csv   Detalle de cada anomalía y su corrección
04_Prototipo_BI/04_Prototipo_BI.pbix       ETL, modelo, medidas DAX y dashboards
05_Resumen_Tecnico/05_Resumen_Tecnico.pdf  Integrantes, transformaciones, medidas, hallazgos
README.txt                                 Este archivo


ORDEN DE EJECUCIÓN

1. Instalar Python 3.10 o superior y las librerías
       pip install pandas numpy openpyxl

2. Generar los datos (opcional, ya vienen generados)
       cd 03_Datos_Sinteticos
       python generar_datos.py
   Con la semilla 2026 se obtienen exactamente los mismos archivos de datos_brutos.

3. Abrir 04_Prototipo_BI/04_Prototipo_BI.pbix en Power BI Desktop.

4. Si Power BI no encuentra los archivos, cambiar el parámetro RutaDatos
   (Transformar datos > Administrar parámetros) a la ruta completa de la carpeta
   03_Datos_Sinteticos/datos_brutos en su computadora y luego presionar Actualizar.
   Las consultas leen los archivos con rutas relativas a esa carpeta.

5. Revisar las páginas Panel del cliente, Desempeño comercial y Uso y retención.


DEPENDENCIAS

Python 3.10 o superior con pandas, numpy y openpyxl
Power BI Desktop (versión de noviembre de 2026 o posterior)
Cuenta institucional con acceso de lector al área de trabajo en Power BI Service


ENLACES

Informe publicado en Power BI Service   [PENDIENTE]
Repositorio   https://github.com/melodycotoviera11-ctrl/Examen02_Startup_MarketMind


SEGURIDAD POR FILAS (RLS)

[PENDIENTE] Roles creados y cuenta de lector usada para la prueba.
