# Examen 2 BI · MarketMind BI

Startup simulada de Inteligencia de Negocios para pymes y agencias que invierten en publicidad digital en Costa Rica.
Examen parcial 02 · Emprendimiento BI.

> Todos los datos de este repositorio son **simulados**.

## Estructura

| Carpeta o archivo | Contenido | Responsable |
|---|---|---|
| 01_LeanCanvas | Lean Canvas y justificación | Melody |
| 02_Arquitectura | Diagrama de flujo y modelo dimensional | Melody |
| 03_Datos_Sinteticos | Script generador, datos brutos e instrucciones | Melody |
| 04_Prototipo_BI | Archivo .pbix con ETL y modelo (Pamela) y con medidas DAX y dashboards (Valeria) | Pamela y Valeria |
| 05_Resumen_Tecnico | Informe técnico | Melody |
| README.txt | Orden de ejecución y enlaces | Melody |

## Empezar

```
cd 03_Datos_Sinteticos
pip install pandas numpy openpyxl
python generar_datos.py
```

Ver `03_Datos_Sinteticos/INSTRUCCIONES_DATOS.md` para el diccionario de datos y las anomalías sembradas.

## Documentos

Los documentos se generan desde `herramientas/` con el formato del curso. Lo resaltado en amarillo está pendiente de completar.
