# Examen 2 BI · MarketMind BI

Startup simulada de Inteligencia de Negocios para pymes y agencias que invierten en publicidad digital en Costa Rica.
Examen parcial 02 · Emprendimiento BI.

> Todos los datos de este repositorio son **simulados**.

## Estructura

| Carpeta o archivo | Contenido | Responsable |
|---|---|---|
| 01_LeanCanvas | Lean Canvas y justificación | Persona 1 |
| 02_Arquitectura | Diagrama de flujo y modelo dimensional | Persona 1 |
| 03_Datos_Sinteticos | Script generador, datos brutos e instrucciones | Persona 1 |
| 04_Prototipo_BI | Archivo .pbix (ETL, modelo, DAX y dashboards) | Personas 2 y 3 |
| 05_Resumen_Tecnico | Informe técnico | Persona 1 |
| README.txt | Orden de ejecución y enlaces | Persona 1 |

## Empezar

```
cd 03_Datos_Sinteticos
pip install pandas numpy openpyxl
python generar_datos.py
```

Ver `03_Datos_Sinteticos/INSTRUCCIONES_DATOS.md` para el diccionario de datos y las anomalías sembradas.
