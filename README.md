# Examen02_Startup_MarketMind

Startup simulada de inteligencia de negocios para pymes y agencias que invierten en publicidad digital en Costa Rica.
Examen parcial 02, TI-6900 Inteligencia de Negocios.

> Todos los datos de este repositorio son **simulados**.

## Estructura

| Archivo o carpeta | Contenido |
|---|---|
| 01_LeanCanvas.pdf | Lean Canvas y justificación del negocio |
| 02_Arquitectura/ | Documento de arquitectura, diagrama de flujo de datos y diagrama del modelo dimensional |
| 03_Datos_Sinteticos/ | Carpetas datos_brutos, script_python, instrucciones y anomalias |
| 04_Prototipo_BI.pbix | ETL en Power Query, modelo, medidas DAX, dashboards y RLS |
| 05_Resumen_Tecnico/ | Resumen técnico y las siete capturas de evidencia |
| README.txt | Orden de ejecución, dependencias, rutas y enlaces |

## Capturas de evidencia (05_Resumen_Tecnico)

| Archivo | Contenido |
|---|---|
| figura_1_dashboard_campanas.png | Página 01, análisis de campañas |
| figura_2_dashboard_comercial.png | Página 02, desempeño comercial |
| figura_3_dashboard_uso_retencion.png | Página 03, uso y retención |
| figura_4_modelo_power_bi.png | Modelo dimensional en la vista de modelo de Power BI |
| figura_5_power_query.png | Transformaciones y validaciones en Power Query |
| figura_6_rls_asignacion.png | Asignación de la cuenta de prueba al rol de RLS |
| figura_7_rls_validacion.png | Vista restringida al cliente CLI-001 |

## Generar los datos

```
cd 03_Datos_Sinteticos/script_python
pip install pandas numpy openpyxl
python generar_datos.py
```

El diccionario de datos y las anomalías sembradas están en `03_Datos_Sinteticos/instrucciones/INSTRUCCIONES_DATOS.md`.

## Abrir el prototipo

Abrir `04_Prototipo_BI.pbix` en Power BI Desktop. Para actualizar los datos, cambiar el parámetro `RutaDatos`
(Transformar datos, Administrar parámetros) por la ruta de la carpeta `03_Datos_Sinteticos\datos_brutos\` y presionar Actualizar.
Los pasos completos y los enlaces al informe publicado están en `README.txt`.
