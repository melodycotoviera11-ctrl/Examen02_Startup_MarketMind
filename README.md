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

## Notas para el modelo en Power BI (Pamela y Valeria)

- Las tablas de hechos se llaman `Fact_Facturacion`, `Fact_ResultadosCampana`, `Fact_UsoPlataforma` y `Fact_Costos`.
- Dimensiones `Dim_Cliente`, `Dim_Plan`, `Dim_Campana`, `Dim_Canal` y `Dim_Calendario`.
- `Fact_ResultadosCampana` lleva `id_cliente` (desde campañas), `id_canal` (homologando el canal y combinando con canales.csv) e `id_plan`.
- `id_plan` en resultados es el plan vigente del cliente ese mes. Se combina con facturas por `id_cliente` y mes. En el mes de alta (prueba gratis) no hay factura, así que se usa `id_plan_inicial` de clientes.
- `Fact_UsoPlataforma` **no** lleva `id_plan`.
- Dim_Calendario lleva una columna `AñoMes` (por ejemplo 2026-03) para ordenar los meses, porque el periodo cruza dos años.
- Sin relación entre Dim_Calendario y `fecha_baja`. Las cancelaciones se cuentan con la medida `Clientes cancelados` del resumen técnico.
- Diagrama editable en `02_Arquitectura/pptx/Diagramas_Arquitectura_MarketMind.pptx`.
