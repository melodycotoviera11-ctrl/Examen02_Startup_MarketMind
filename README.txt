MarketMind BI - Examen parcial 02, TI-6900 Inteligencia de Negocios
Equipo MarketMind. Valeria Abarca Chacón, Melody Coto Viera y Pamela Cruz Segura.

TODOS LOS DATOS DE ESTE PAQUETE SON SIMULADOS. Las empresas, campañas, montos y usuarios
son ficticios y no representan resultados de ninguna empresa real.


CONTENIDO

01_LeanCanvas.pdf                                  Lienzo y justificación del negocio
02_Arquitectura/02_Arquitectura.pdf                Flujo de datos, modelo dimensional, calidad y seguridad
02_Arquitectura/flujo_datos.png                    Diagrama de flujo de datos
02_Arquitectura/modelo_dimensional.png             Diagrama del modelo dimensional
03_Datos_Sinteticos/datos_brutos/                  8 archivos de origen, con anomalías a propósito
03_Datos_Sinteticos/script_python/generar_datos.py Script de Python que genera los datos (semilla 2026)
03_Datos_Sinteticos/instrucciones/                 Instrucciones, diccionario de datos y semilla
03_Datos_Sinteticos/anomalias/                     Registro de cada anomalía sembrada y su corrección
04_Prototipo_BI.pbix                               ETL en Power Query, modelo, medidas DAX y dashboards
05_Resumen_Tecnico/05_Resumen_Tecnico.pdf          Integrantes, transformaciones, medidas, hallazgos y recomendaciones
05_Resumen_Tecnico/figura_1 a figura_7 (.png)     Capturas de evidencia (dashboards, modelo, Power Query y RLS)
README.txt                                         Este archivo


ORDEN DE EJECUCIÓN

1. Instalar Python 3.10 o superior y las librerías
       pip install pandas numpy openpyxl

2. Generar los datos (opcional, ya vienen generados en datos_brutos)
       cd 03_Datos_Sinteticos/script_python
       python generar_datos.py
   El script guarda los archivos en 03_Datos_Sinteticos/datos_brutos y el registro en
   03_Datos_Sinteticos/anomalias. Con la semilla 2026 se obtienen siempre los mismos datos.

3. Abrir 04_Prototipo_BI.pbix en Power BI Desktop. El archivo ya trae los datos cargados,
   así que las páginas se pueden revisar sin actualizar.

4. Para actualizar los datos desde los archivos de origen, cambiar una sola ruta.
   Todas las consultas leen los archivos desde el parámetro RutaDatos.
   a. Inicio > Transformar datos > Administrar parámetros.
   b. Seleccionar RutaDatos y en "Valor actual" pegar la ruta completa de la carpeta
      03_Datos_Sinteticos\datos_brutos\ en la computadora donde se abra el archivo,
      terminada en una barra invertida.
   c. Aceptar, Cerrar y aplicar, y luego presionar Actualizar.

5. Revisar las páginas 01 Análisis de campañas, 02 Desempeño comercial y 03 Uso y retención.


DEPENDENCIAS

Python 3.10 o superior con pandas, numpy y openpyxl
Power BI Desktop
Cuenta institucional con permiso de lector para ver el informe en Power BI Service


RUTAS RELATIVAS

Todas las rutas de este paquete son relativas a la carpeta principal del .zip.
El script calcula sus rutas a partir de su propia ubicación, por lo que funciona en
cualquier computadora sin cambios. En Power BI las ocho consultas usan la expresión
RutaDatos & "nombre_del_archivo", así que basta con cambiar el parámetro RutaDatos
(paso 4) para que el modelo lea los datos desde la carpeta datos_brutos del paquete.


ENLACES

Informe publicado en Power BI Service
https://app.powerbi.com/groups/me/reports/ea8102a8-429b-4076-84f0-c091a4705b3f/2c54bed546c90e9727c9?experience=power-bi

Modelo semántico
https://app.powerbi.com/groups/me/modeling/35351294-fbe1-4d0a-96ce-e30c2c3faf59/modelView?experience=power-bi

Repositorio
https://github.com/melodycotoviera11-ctrl/Examen02_Startup_MarketMind


SEGURIDAD POR FILAS (RLS)

Rol Cliente_MarketMind con el filtro [id_cliente] = "CLI-001" sobre Dim_Cliente.
Se probó en Power BI Service con una cuenta de lector (Viewer), que solo ve la información
de ese cliente. El informe y el modelo se compartieron con permiso de lectura.
