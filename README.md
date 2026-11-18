# Examen02_Startup_MarketMind

Startup simulada de inteligencia de negocios para pymes y agencias que invierten en publicidad digital en Costa Rica.
Examen parcial 02, TI-6900 Inteligencia de Negocios.

> Todos los datos de este repositorio son **simulados**.

## Estructura

| Archivo o carpeta | Contenido |
|---|---|
| 01_LeanCanvas.pdf | Lean Canvas y justificación del negocio |
| 02_Arquitectura/ | Documento de arquitectura y las imágenes del flujo de datos y del modelo dimensional |
| 03_Datos_Sinteticos/ | Carpetas datos_brutos, script_python, instrucciones y anomalias |
| 04_Prototipo_BI.pbix | ETL, modelo, medidas DAX y dashboards (pendiente) |
| 05_Resumen_Tecnico/ | Resumen técnico y sus capturas de evidencia |
| README.txt | Orden de ejecución, dependencias, rutas y enlaces |

## Generar los datos

```
cd 03_Datos_Sinteticos/script_python
pip install pandas numpy openpyxl
python generar_datos.py
```

El diccionario de datos y las anomalías sembradas están en `03_Datos_Sinteticos/instrucciones/INSTRUCCIONES_DATOS.md`.

## Notas para el modelo en Power BI

- Tablas de hechos `Fact_Facturacion`, `Fact_ResultadosCampana`, `Fact_UsoPlataforma` y `Fact_Costos`.
- Dimensiones `Dim_Cliente`, `Dim_Plan`, `Dim_Campana`, `Dim_Canal` y `Dim_Calendario`.
- `Fact_ResultadosCampana` lleva `id_cliente` (desde campañas), `id_canal` (homologando el canal y combinando con canales.csv) e `id_plan`.
- `id_plan` en resultados es el plan vigente del cliente ese mes. Se combina con facturas por `id_cliente` y mes. En el mes de alta (prueba gratis) no hay factura, así que se usa `id_plan_inicial` de clientes.
- `Fact_UsoPlataforma` no lleva `id_plan`.
- `Dim_Calendario` lleva una columna `AñoMes` (por ejemplo 2026-03) para ordenar los meses, porque el periodo cruza dos años.
- No hay relación entre `Dim_Calendario` y `fecha_baja`. Las cancelaciones se cuentan con la medida `Clientes cancelados` del resumen técnico.
- Las consultas leen los archivos desde un parámetro `RutaDatos`, para que el profesor solo cambie una ruta.
- El archivo .pbix se sube a la raíz con el nombre `04_Prototipo_BI.pbix`.
