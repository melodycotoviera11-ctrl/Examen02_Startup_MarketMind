# MarketMind BI · Datos sintéticos

> **Todos los datos de esta carpeta son SIMULADOS.** Las empresas, marcas, campañas, montos y usuarios son ficticios. No representan resultados de ninguna empresa real ni contienen información personal.

## Cómo regenerar los datos

1. Instalar Python 3.10 o superior.
2. Instalar las librerías con `pip install pandas numpy openpyxl`
3. Desde esta carpeta, ejecutar `python generar_datos.py`

La semilla aleatoria es **2026**. Con esa semilla el script produce siempre exactamente los mismos archivos. Para probar otra semilla se usa `python generar_datos.py --semilla 123`

El script borra y vuelve a escribir los archivos de `datos_brutos/` y el archivo `documentacion/registro_anomalias.csv`.

## Periodo y volumen

Doce meses de operación simulada, del 1 de noviembre de 2025 al 31 de octubre de 2026. Todos los montos están en colones.

| Archivo | Tipo de tabla | Filas aproximadas | Origen simulado |
|---|---|---|---|
| clientes.csv | Dimensión | 40 | Sistema de facturación y CRM |
| planes.csv | Dimensión | 3 | Sistema de facturación |
| canales.csv | Dimensión | 5 | Catálogo interno |
| campanas.xlsx | Dimensión | 430 | Hoja de control de campañas |
| facturas.csv | Hechos comerciales | 210 | Sistema de facturación |
| resultados_campanas.csv | Hechos de resultados del servicio | 15 050 | Exportación de la API de Meta, Google, TikTok y del canal de IA |
| uso_plataforma.csv | Hechos de uso del producto | 3 210 | Registro de actividad de la plataforma |

## Diccionario de datos

### clientes.csv
Una fila por empresa o agencia que contrató MarketMind BI.

| Columna | Descripción |
|---|---|
| id_cliente | Clave del cliente, formato CLI-001 |
| nombre_empresa | Nombre ficticio |
| industria | Industria del cliente. Las agencias aparecen como "Agencia de marketing" |
| tamano_empresa | Micro, Pequeña o Mediana |
| provincia | Provincia de Costa Rica |
| canal_adquisicion | Por dónde llegó el cliente a MarketMind (Instagram, LinkedIn, Webinar, Referido o Alianza cámara de comercio) |
| fecha_alta | Día en que empezó la prueba gratis de 14 días |
| id_plan_inicial | Plan con el que empezó (puede cambiar después, ver facturas) |
| fecha_baja | Último día de servicio si canceló. Vacío si sigue activo |

### planes.csv
| Columna | Descripción |
|---|---|
| id_plan | PLN-01, PLN-02, PLN-03 |
| nombre_plan | Starter, Growth, Agencia |
| precio_mensual_crc | ₡10 000, ₡30 000 y ₡70 000 antes de IVA |
| max_marcas, max_canales | Límites del plan. Starter usa 2 canales, Growth y Agencia los 5 |
| incluye_alertas | Sí o No |

### canales.csv
| Columna | Descripción |
|---|---|
| id_canal | CAN-01 a CAN-05 |
| nombre_canal | Facebook Ads, Instagram Ads, Google Ads, TikTok Ads, Anuncios en IA (beta) |
| plataforma | Meta, Google, TikTok o Asistentes de IA |
| tipo_canal | Redes sociales, Buscador, Video corto o Conversacional |

### campanas.xlsx (hoja "campanas")
Una fila por campaña publicitaria que un cliente conectó a MarketMind.

| Columna | Descripción |
|---|---|
| id_campana | Clave, formato CMP-0001 |
| id_cliente | Cliente dueño de la cuenta |
| marca | Marca anunciada. En agencias hay varias marcas por cliente |
| industria_marca | Industria de la marca |
| nombre_campana | Nombre descriptivo |
| canal | Nombre del canal escrito a mano (tiene inconsistencias a propósito, ver A-06) |
| objetivo | Ventas, Mensajes a WhatsApp, Tráfico al sitio web o Reconocimiento |
| fecha_inicio, fecha_fin | Vigencia. fecha_fin vacía significa que la campaña sigue activa al cierre del periodo |
| presupuesto_diario_crc | Presupuesto diario planeado |

### facturas.csv
**Granularidad, una fila por cliente por mes facturado.** La prueba gratis cubre el mes de alta, así que se cobra desde el mes siguiente.

| Columna | Descripción |
|---|---|
| id_factura | Clave, formato FAC-00001 |
| id_cliente, id_plan | Cliente y plan cobrado ese mes |
| periodo | Mes cobrado, formato AAAA-MM |
| fecha_emision, fecha_vencimiento, fecha_pago | Se emite el día 1 y vence el día 10. fecha_pago vacía si no se ha pagado |
| monto_plan_crc | Precio de lista del plan |
| descuento_crc | 50 % en las dos primeras facturas de quienes entraron en el lanzamiento (nov y dic 2025) |
| subtotal_crc | Monto menos descuento. **Este es el ingreso de MarketMind** |
| iva_crc, total_crc | IVA del 13 % y total cobrado |
| estado_pago | Pagada, Pendiente o Vencida |
| metodo_pago | SINPE Móvil, Transferencia o Tarjeta |

### resultados_campanas.csv
**Granularidad, una fila por campaña por día.**

| Columna | Descripción |
|---|---|
| id_resultado | Clave, formato RES-000001 |
| id_campana | Campaña |
| fecha | Día |
| impresiones, clics, conversiones | Resultados del día |
| gasto_crc | Lo que el cliente invirtió en anuncios ese día |
| ingresos_atribuidos_crc | Ventas del cliente atribuidas a la campaña |

### uso_plataforma.csv
**Granularidad, una fila por sesión de un usuario en el panel de MarketMind.**

| Columna | Descripción |
|---|---|
| id_sesion | Clave, formato SES-00001 |
| id_cliente | Cliente al que pertenece el usuario |
| fecha_hora_inicio | Fecha y hora de la sesión |
| rol_usuario | Dueño o dueña, Encargado de marketing, Analista de agencia, etc. |
| dispositivo | Computadora, Celular o Tableta |
| pagina_principal | Página donde pasó más tiempo |
| duracion_min | Minutos de la sesión |
| alertas_revisadas | Alertas que revisó (solo planes con alertas) |
| reporte_descargado | Sí o No |

## Comportamientos simulados

Estos patrones se programaron a propósito para que el análisis encuentre algo.

1. **Crecimiento de la cartera.** El lanzamiento fue en noviembre de 2025 y los clientes entran poco a poco hasta llegar a unos 32 activos en octubre de 2026.
2. **Cancelación según plan y uso.** Starter cancela bastante más que Growth y Agencia. Además, el uso del panel baja mucho en las seis semanas antes de que un cliente cancele.
3. **Mejoras de plan.** Algunos clientes Starter que usan mucho la plataforma suben a Growth.
4. **Estacionalidad.** Más gasto y ventas en noviembre (Black Friday), diciembre y agosto (Día de la Madre). Enero y Semana Santa bajan. Educación sube en febrero por el regreso a clases.
5. **Rendimiento distinto por canal e industria.** Google rinde más en salud, educación y tecnología. Instagram y TikTok funcionan mejor en moda y fitness. Restaurantes casi no recupera lo que invierte en TikTok.
6. **Valor entregado.** Con el paso de los meses los clientes bajan su costo por conversión y suben su retorno, sobre todo en los planes con alertas, porque mueven el presupuesto al canal que mejor les funciona.
7. **Canal de anuncios en IA en versión beta.** Desde junio de 2026 MarketMind conecta, en prueba, anuncios dentro de asistentes de IA. Solo está disponible para los planes Growth y Agencia, se usa con menos presupuesto y no se ofrece a salud y estética, que es una categoría sensible. Rinde bien en tecnología y educación.
8. **Fines de semana.** Restaurantes y moda venden más los sábados y domingos.

## Anomalías sembradas

El detalle exacto, con la cantidad de filas afectadas, queda en `documentacion/registro_anomalias.csv`. Ninguna se corrige a mano, todas se limpian en Power Query.

| Código | Tipo | Archivo | Corrección esperada |
|---|---|---|---|
| A-01 | Duplicados | resultados_campanas.csv | Quitar duplicados por id_resultado |
| A-02 | Duplicados | facturas.csv | Quitar duplicados por id_factura |
| A-03 | Duplicados | uso_plataforma.csv | Quitar duplicados por id_sesion |
| A-04 | Faltantes | resultados_campanas.csv | ingresos vacíos pasan a 0 (son días sin conversiones) |
| A-05 | Faltantes | clientes.csv | provincia y canal_adquisicion vacíos pasan a "Sin dato" |
| A-06 | Categorías inconsistentes | campanas.xlsx | Homologar el nombre del canal y unir con canales.csv para obtener id_canal |
| A-07 | Categorías inconsistentes | clientes.csv, facturas.csv | Homologar provincia y método de pago |
| A-08 | Fuera de rango | resultados_campanas.csv | gasto negativo pasa a valor absoluto |
| A-09 | Fuera de rango | resultados_campanas.csv | Si clics > impresiones, intercambiar valores |
| A-10 | Integridad referencial | resultados_campanas.csv | Eliminar resultados de campañas inexistentes (CMP-9000 en adelante) |
| A-11 | Formato de clave | uso_plataforma.csv | Pasar id_cliente a mayúsculas |

## Relaciones entre archivos

```
planes.id_plan ─────────────< facturas.id_plan
clientes.id_cliente ────────< facturas.id_cliente
clientes.id_cliente ────────< campanas.id_cliente
clientes.id_cliente ────────< uso_plataforma.id_cliente
canales.nombre_canal ───────< campanas.canal        (después de homologar, se usa id_canal)
campanas.id_campana ────────< resultados_campanas.id_campana
```

La tabla calendario no viene en los archivos, se crea en Power BI y se relaciona con las fechas de facturas, resultados y uso.
