import sys
sys.path.insert(0, "/home/claude/examen2/herramientas")
from plantilla import Documento

INTEGRANTES = [
    "[[Carné]], Valeria Abarca Chacón",
    "2024224269, Melody Onid Coto Viera",
    "[[Carné]], Pamela Cruz Segura",
]
d = Documento("Examen parcial 02.", "MarketMind BI, resumen técnico",
              INTEGRANTES, "martes 24 de noviembre de 2026")

d.h1("Resumen técnico")
d.h2("Integrantes")
d.tabla(["Nombre completo", "Carné", "Correo institucional", "Responsabilidad"],
        [["Melody Onid Coto Viera", "2024224269", "[[correo]]", "Lean Canvas, arquitectura, datos sintéticos, resumen técnico y README"],
         ["Pamela Cruz Segura", "[[carné]]", "[[correo]]", "ETL en Power Query, validaciones y modelo dimensional"],
         ["Valeria Abarca Chacón", "[[carné]]", "[[correo]]", "Medidas DAX, dashboards, publicación y RLS"]],
        [3, 1.6, 3.2, 5], size=18)

d.h2("Solución entregada")
d.parrafo("MarketMind BI es una startup simulada que vende un servicio de inteligencia de negocios a pymes y agencias "
          "que invierten en publicidad digital en Costa Rica. El prototipo cubre doce meses de operación, del 1 de "
          "noviembre de 2025 al 31 de octubre de 2026. Un script de Python con semilla 2026 genera ocho archivos de "
          "origen con 40 clientes y más de 18.000 registros en las tablas de hechos. Power Query limpia los datos, "
          "el modelo en estrella los organiza y el informe publicado en Power BI Service los presenta en tres "
          "páginas. Todos los datos son simulados.")

d.h2("Transformaciones en Power Query")
d.leyenda("Transformaciones aplicadas y anomalía que corrige cada una")
d.tabla(["Consulta", "Transformación", "Anomalía"],
        [["Todas", "Asignar tipos de datos (fechas, enteros y texto) con configuración regional es-CR", "Tipos de datos"],
         ["Facturas, Resultados, Uso", "Quitar filas duplicadas por id_factura, id_resultado e id_sesion", "A-01, A-02, A-03"],
         ["Resultados", "Reemplazar ingresos vacíos por 0, porque son días sin conversiones", "A-04"],
         ["Clientes", "Reemplazar provincia y canal de adquisición vacíos por “Sin dato”", "A-05"],
         ["Campañas", "Recortar espacios, homologar el nombre del canal con una tabla de equivalencias y combinar con Canales para obtener id_canal", "A-06"],
         ["Clientes, Facturas", "Recortar, poner en formato de título y reemplazar valores de provincia y método de pago", "A-07"],
         ["Resultados", "Convertir el gasto a valor absoluto", "A-08"],
         ["Resultados", "Columnas condicionales que intercambian clics e impresiones cuando clics es mayor", "A-09"],
         ["Resultados", "Combinación interna con Campañas para quitar resultados huérfanos y traer id_cliente", "A-10"],
         ["Uso", "Pasar id_cliente a mayúsculas y separar la fecha de la hora", "A-11"],
         ["Facturas", "Columna derivada días para pagar (fecha de pago menos fecha de emisión)", "Clave derivada"]],
        [2.2, 7.6, 1.6], size=18)
d.nota("[[Pamela revisa que la lista coincida con los pasos aplicados en el archivo .pbix.]]")

d.h2("Validaciones de calidad")
d.leyenda("Conteos esperados antes y después de la limpieza")
d.tabla(["Validación", "Tabla", "Antes", "Después", "Resultado"],
        [["Unicidad de la clave", "Facturas", "207 filas", "201 filas", "[[Cumple]]"],
         ["Unicidad de la clave", "Resultados", "15.049 filas", "14.827 filas", "[[Cumple]]"],
         ["Integridad referencial con Campañas", "Resultados", "15 huérfanos", "14.812 filas, 0 huérfanos", "[[Cumple]]"],
         ["Unicidad e integridad con Clientes", "Uso", "3.210 filas, 40 claves en minúscula", "3.185 filas, 0 sin cliente", "[[Cumple]]"],
         ["Rango válido de gasto", "Resultados", "12 negativos", "0 negativos", "[[Cumple]]"],
         ["Clics menores o iguales a impresiones", "Resultados", "10 filas incorrectas", "0 filas", "[[Cumple]]"],
         ["Categorías homologadas", "Campañas", "25 nombres de canal", "5 canales", "[[Cumple]]"],
         ["Sin vacíos en ingresos", "Resultados", "300 vacíos", "0 vacíos", "[[Cumple]]"]],
        [3.6, 1.8, 2.6, 2.8, 1.4], size=18)

d.h2("Modelo y medidas DAX")
d.parrafo("El modelo tiene cuatro tablas de hechos (facturación, resultados de campañas, uso de la plataforma y "
          "costos), cinco dimensiones (cliente, plan, campaña, canal y calendario), de las cuales cliente, plan y "
          "calendario son compartidas, y relaciones de uno a muchos con filtro en una sola dirección. El detalle está en el documento 02_Arquitectura.", despues=80)
d.leyenda("Medidas DAX del modelo")
d.tabla(["Medida", "Fórmula"],
        [["Ingresos", "SUM(Fact_Facturacion[subtotal_crc])"],
         ["Clientes activos", "DISTINCTCOUNT(Fact_Facturacion[id_cliente])"],
         ["Ticket medio", "DIVIDE([Ingresos], [Clientes activos])"],
         ["Variación mensual de ingresos %", "VAR ant = CALCULATE([Ingresos], DATEADD(Dim_Calendario[Fecha], -1, MONTH)) RETURN DIVIDE([Ingresos] - ant, ant)"],
         ["Ingresos acumulados del año", "TOTALYTD([Ingresos], Dim_Calendario[Fecha], \"10/31\")"],
         ["Costos", "SUM(Fact_Costos[monto_crc])"],
         ["Margen %", "DIVIDE([Ingresos] - [Costos], [Ingresos])"],
         ["Clientes cancelados", "VAR ini = MIN(Dim_Calendario[Fecha]) VAR fin = MAX(Dim_Calendario[Fecha]) RETURN CALCULATE(COUNTROWS(Dim_Cliente), Dim_Cliente[fecha_baja] >= ini, Dim_Cliente[fecha_baja] <= fin)"],
         ["Tasa de cancelación", "DIVIDE([Clientes cancelados], [Clientes activos])"],
         ["CAC del cliente", "DIVIDE(SUM(Fact_ResultadosCampana[gasto_crc]), SUM(Fact_ResultadosCampana[conversiones]))"],
         ["ROAS", "DIVIDE(SUM(Fact_ResultadosCampana[ingresos_atribuidos_crc]), SUM(Fact_ResultadosCampana[gasto_crc]))"],
         ["Gasto promedio móvil 3 meses", "DIVIDE(CALCULATE(SUM(Fact_ResultadosCampana[gasto_crc]), DATESINPERIOD(Dim_Calendario[Fecha], MAX(Dim_Calendario[Fecha]), -3, MONTH)), 3)"],
         ["Sesiones por cliente", "DIVIDE(COUNTROWS(Fact_UsoPlataforma), DISTINCTCOUNT(Fact_UsoPlataforma[id_cliente]))"]],
        [3, 8.8], size=17, negrita_col1=True)
d.nota("[[Valeria ajusta nombres y fórmulas para que coincidan con las medidas del archivo .pbix.]]")

d.h2("Publicación, enlaces y evidencias")
d.leyenda("Enlaces de la solución publicada")
d.tabla(["Elemento", "Detalle"],
        [["Informe en Power BI Service", "[[enlace]]"],
         ["Modelo semántico", "[[enlace]]"],
         ["Repositorio", "https://github.com/melodycotoviera11-ctrl/Examen02_Startup_MarketMind"],
         ["Seguridad por filas (RLS)", "[[Roles creados y cuenta Viewer usada para la prueba]]"],
         ["Acceso de la persona docente", "[[Confirmar que el profesor tiene permiso de lector]]"]],
        [3.2, 8.6], size=18, negrita_col1=True)
d.parrafo("[[Insertar aquí las capturas de las tres páginas del dashboard, del modelo en la vista de relaciones, de "
          "los pasos de Power Query y de la prueba de RLS con la cuenta de lector.]]", sangria=False)

d.h2("Hallazgos")
d.parrafo("**Hallazgo 1. El plan Starter concentra las cancelaciones.** De los 25 clientes que empezaron en Starter, "
          "9 cancelaron durante el año (36 %). En Growth canceló 1 de 9 (11 %) y en Agencia ninguno de 6. El plan de "
          "menor precio atrae clientes, pero también es el que presenta mayor cancelación.")
d.parrafo("**Hallazgo 2. El uso del panel avisa antes de una cancelación.** Los clientes que cancelaron usaban el "
          "panel 3,3 veces por semana en promedio, pero en sus últimas seis semanas pasaron a 1,1 veces, una caída de "
          "dos tercios. Los clientes que siguen activos se mantuvieron estables, cerca de 3,6 sesiones por semana.")
d.parrafo("**Hallazgo 3. Las alertas generan más valor para el cliente.** Los clientes que empezaron en Growth o "
          "Agencia, que incluyen alertas, redujeron su costo por venta de ₡9.460 en sus dos primeros meses a ₡6.060 desde "
          "el sexto mes, un 36 % menos. Los que empezaron en Starter pasaron de ₡9.048 a ₡7.035, un 22 %. Además, en "
          "restaurantes el retorno de TikTok fue de 0,49 y el de los anuncios en IA de 0,63, es decir, esos canales "
          "les generan pérdidas, mientras que Facebook e Instagram se ubican cerca de 1,4.")
d.nota("[[Valeria confirma que los números coinciden con lo que muestra el dashboard.]]")

d.h2("Recomendaciones")
d.parrafo("**Recomendación 1. Activar un programa de retención para Starter.** Crear una alerta interna cuando un "
          "cliente baje de dos sesiones por semana, para contactarlo antes de que cancele, y ofrecer a los clientes "
          "Starter activos un mes de prueba del plan Growth. De esta forma conocen las alertas, que son las que más reducen su "
          "costo por venta, y migran al plan con menor cancelación.")
d.parrafo("**Recomendación 2. Dar recomendaciones por industria.** Agregar al panel un aviso cuando el retorno de un "
          "canal sea menor a 1 para la industria del cliente. A los restaurantes, por ejemplo, se les sugeriría trasladar "
          "el presupuesto de TikTok y de los anuncios en IA hacia Instagram y Facebook. El canal de IA en beta conviene "
          "ofrecerlo primero a tecnología y educación, donde el retorno simulado fue de 6,2 y 5,4.", despues=0)

d.guardar("/home/claude/examen2/05_Resumen_Tecnico/05_Resumen_Tecnico.docx")
print("ok")
