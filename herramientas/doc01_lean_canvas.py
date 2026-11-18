import sys
sys.path.insert(0, "/home/claude/examen2/herramientas")
from plantilla import Documento, ANCHO_UTIL
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

INTEGRANTES = [
    "[[Carné]], Valeria Abarca Chacón",
    "2024224269, Melody Onid Coto Viera",
    "[[Carné]], Pamela Cruz Segura",
]
d = Documento("Examen parcial 02.", "MarketMind BI, Lean Canvas y propuesta de valor",
              INTEGRANTES, "martes 24 de noviembre de 2026")

# ----------------------------------------------------------------------
d.h1("Lean Canvas de MarketMind BI")
d.parrafo("MarketMind BI es una startup de inteligencia de negocios que ayuda a pymes y agencias pequeñas de "
          "Costa Rica a saber cuánto les deja la plata que invierten en publicidad digital. Junta en un solo "
          "panel los resultados de Meta, Google, TikTok y un canal de anuncios en IA en versión beta, y los cruza "
          "con las ventas del cliente. El lienzo resume las hipótesis del negocio.", despues=120)

bloques = {
    "problema": ["1. Problema",
                 "**a.** Los resultados de los anuncios están separados en Meta, Google y TikTok, y las ventas reales quedan en SINPE, WhatsApp o la tienda en línea. No se sabe qué campaña vendió.",
                 "**b.** No conocen su costo por venta (CAC) ni su retorno (ROAS), así que invierten a ojo.",
                 "**c.** Armar el reporte mensual en Excel toma horas y casi siempre llega tarde.",
                 "**Alternativas actuales.** Excel, el panel de cada red social por aparte, el PDF de una agencia o herramientas extranjeras en dólares."],
    "solucion": ["4. Solución",
                 "Une las campañas de todos los canales con las ventas del cliente.",
                 "Compara CAC, ROAS y conversiones por canal, campaña y marca.",
                 "Alertas cuando una campaña gasta sin vender.",
                 "Reporte mensual automático.",
                 "**MVP.** Informe en Power BI con 12 meses de datos simulados y tres páginas."],
    "puv": ["3. Propuesta única de valor",
            "**Sabé en un solo panel cuánto te deja cada colón que invertís en publicidad.**",
            "El reporte mensual pasa de unas 8 horas a menos de 1.",
            "Meta medible, bajar 15 % el costo por venta en los primeros tres meses.",
            "Pensado para Costa Rica, en colones y con ventas por SINPE y WhatsApp."],
    "ventaja": ["9. Ventaja especial",
                "Todavía no existe. Se construye con el conocimiento del mercado tico y con una base de comparación por industria que crece con cada cliente nuevo.",
                "Acceso temprano al canal de anuncios en IA en versión beta."],
    "segmentos": ["2. Segmentos de clientes",
                  "**Cliente que paga.** Dueños de pymes que invierten en publicidad digital y agencias pequeñas de marketing.",
                  "**Usuario final.** La persona encargada de redes o de mercadeo, y en las agencias el analista de cuentas.",
                  "**Primeros adoptantes.** Agencias pequeñas de la GAM y tiendas en línea que ya invierten más de ₡150.000 al mes en anuncios."],
    "metricas": ["8. Métricas clave",
                 "Ingreso mensual recurrente (MRR)",
                 "Clientes activos por plan",
                 "Tasa de cancelación mensual",
                 "Sesiones semanales por cliente",
                 "Baja del CAC de los clientes"],
    "canales": ["5. Canales",
                "**Atraer.** Instagram, LinkedIn, webinars gratis y cámaras de comercio.",
                "**Vender.** Prueba gratis de 14 días y precio de lanzamiento.",
                "**Entregar.** Informe publicado en Power BI con acceso por cliente.",
                "**Atender.** Videollamada de bienvenida y soporte por WhatsApp."],
    "costos": ["7. Estructura de costos",
               "**Tecnológicos.** Licencias Power BI Pro, capacidad Fabric F2, nube y dominio.",
               "**Comerciales.** Publicidad propia, eventos y webinars.",
               "**Operativos.** Soporte y configuración de clientes, contabilidad y comisiones de cobro.",
               "Cerca de ₡476.000 al mes al cierre del primer año."],
    "ingresos": ["6. Fuentes de ingresos",
                 "Suscripción mensual por cliente, más IVA.",
                 "**Starter** ₡10.000 (una marca, dos canales). **Growth** ₡30.000 (todos los canales y alertas). **Agencia** ₡70.000 (hasta 10 marcas).",
                 "**Supuesto.** 32 clientes activos al cierre del primer año (14 Starter, 12 Growth y 6 Agencia), con ₡920.000 de ingreso mensual."],
}

t = d.doc.add_table(rows=3, cols=10)
t.style = d.doc.styles["Table Grid"]
t.alignment = WD_TABLE_ALIGNMENT.CENTER
d.sectPr.addprevious(t._tbl)
d._fijar(t, [ANCHO_UTIL // 10] * 10)
celdas = {
    "problema": t.cell(0, 0).merge(t.cell(1, 1)),
    "solucion": t.cell(0, 2).merge(t.cell(0, 3)),
    "puv": t.cell(0, 4).merge(t.cell(1, 5)),
    "ventaja": t.cell(0, 6).merge(t.cell(0, 7)),
    "segmentos": t.cell(0, 8).merge(t.cell(1, 9)),
    "metricas": t.cell(1, 2).merge(t.cell(1, 3)),
    "canales": t.cell(1, 6).merge(t.cell(1, 7)),
    "costos": t.cell(2, 0).merge(t.cell(2, 4)),
    "ingresos": t.cell(2, 5).merge(t.cell(2, 9)),
}
for clave, celda in celdas.items():
    titulo, *items = bloques[clave]
    d._llenar(celda, ["**" + titulo + "**"] + items, size=19)
    if clave == "puv":
        d._sombra(celda, "DEEAF6")
for i, fila in enumerate(t.rows):
    trpr = fila._tr.get_or_add_trPr()
    trpr.append(OxmlElement("w:cantSplit"))
    h = OxmlElement("w:trHeight")
    h.set(qn("w:val"), ["4200", "3900", "2500"][i])
    trpr.append(h)
d.nota("Todos los montos, clientes y resultados son simulados y no corresponden a una empresa real.")

# ----------------------------------------------------------------------
d.h1("Justificación")
d.h2("Por qué este problema merece una solución de BI")
d.parrafo("Una pyme que anuncia en redes sociales recibe muchísimos datos, pero repartidos. Facebook e Instagram "
          "muestran sus números en un panel, Google en otro y TikTok en otro, y ninguno sabe qué pasó después del "
          "clic, porque en Costa Rica mucha gente compra por WhatsApp y paga por SINPE Móvil. El dueño del negocio "
          "termina viendo métricas sueltas, como alcance o “me gusta”, que no le dicen si la campaña le dejó plata.")
d.parrafo("El problema no es la falta de datos, es que nadie los junta ni los convierte en una decisión. Eso es "
          "justo lo que hace la inteligencia de negocios. MarketMind recibe los datos de las plataformas y de las "
          "ventas, los limpia, los integra en un modelo y los presenta como indicadores que cualquier persona "
          "entiende, como el costo por venta y el retorno de cada colón invertido. Así el cliente puede mover su "
          "presupuesto con evidencia y no por intuición.")

d.h2("Mercado y primeros clientes")
d.parrafo("Nos enfocamos en pymes de comercio y servicios que ya invierten en anuncios (moda, restaurantes, salud y "
          "estética, gimnasios, academias y tecnología) y en agencias pequeñas que manejan varias marcas a la vez. "
          "Las agencias son nuestras mejores primeras clientas, porque cada mes tienen que rendirle cuentas a cada "
          "marca y hoy lo hacen a mano. Empezamos en la GAM, cerca de donde podemos visitar a los clientes, y "
          "después crecemos con referidos y alianzas con cámaras de comercio.")

d.h2("En qué nos diferenciamos")
d.parrafo("Hoy el cliente tiene tres caminos. Puede revisar cada plataforma por aparte, que es gratis pero no le "
          "muestra el panorama completo. Puede armar un Excel o un tablero propio, que depende de que alguien sepa "
          "hacerlo y tenga tiempo cada mes. O puede pagar una herramienta extranjera de reportes, que cobra en "
          "dólares, está pensada para agencias grandes y no conecta ventas que entran por WhatsApp o SINPE.")
d.parrafo("MarketMind se diferencia en cuatro cosas. Cruza la inversión con las ventas reales y no solo con métricas "
          "de la red social. Habla el idioma del mercado local, con precios en colones y canales de venta ticos. "
          "Incluye alertas que avisan cuando una campaña gasta sin vender. Y tiene un plan para agencias donde cada "
          "marca ve solo su información, gracias a la seguridad por filas (RLS) de Power BI.")

d.h2("Ejemplo del valor para un cliente")
d.parrafo("En los datos simulados, Tienda Colibrí Express, una tienda de moda en el plan Growth, invertía cerca de "
          "₡327.000 al mes y todo lo ponía en Facebook. En sus dos primeros meses cada venta le costaba ₡31.800 y "
          "por cada colón invertido recuperaba apenas 62 céntimos, o sea que perdía plata. El panel le mostró que "
          "en Instagram vendía mucho más barato, y con las alertas fue moviendo el presupuesto. Seis meses después "
          "el 74 % de su inversión estaba en Instagram, cada venta le costaba ₡11.100 y recuperaba ₡1,68 por cada "
          "colón. Por ₡33.900 al mes, IVA incluido, pasó de perder dinero a ganar con sus anuncios.")

d.h2("Escenario de monetización")
d.parrafo("El escenario parte de supuestos explícitos. Los precios son mensuales y sin IVA. Cada cliente tiene 14 "
          "días de prueba gratis y empieza a pagar el mes siguiente. Quienes entraron en el lanzamiento (noviembre "
          "y diciembre de 2025) tuvieron 50 % de descuento en sus dos primeras facturas. Usamos un tipo de cambio "
          "de ₡450 por dólar para las licencias y suponemos que las tres fundadoras no cobran salario el primer año. "
          "Con esas reglas, la operación simulada llega a 32 clientes activos en octubre de 2026.", despues=80)
d.leyenda("Ingreso mensual simulado al cierre del primer año (octubre de 2026)")
d.tabla(["Plan", "Precio mensual", "Clientes activos", "Ingreso mensual"],
        [["Starter", "₡10.000", "14", "₡140.000"],
         ["Growth", "₡30.000", "12", "₡360.000"],
         ["Agencia", "₡70.000", "6", "₡420.000"],
         ["**Total**", "", "**32**", "**₡920.000**"]],
        [3, 3, 3, 3])
d.parrafo(antes=160, texto="Ese mes los costos simulados suman ₡475.900, así que el margen es de ₡444.100, cerca del 48 % de los "
          "ingresos. El negocio pierde plata los primeros cinco meses, mientras junta clientes, y llega al punto de "
          "equilibrio en abril de 2026, con 19 clientes que pagan. En el año completo factura ₡5.590.000 contra "
          "₡5.509.900 de costos, es decir, recupera lo invertido en el arranque. El riesgo principal es la "
          "cancelación del plan Starter, por eso la meta comercial es pasar a los clientes más activos al plan "
          "Growth.", despues=0)

d.guardar("/home/claude/examen2/01_LeanCanvas/01_LeanCanvas.docx")
print("ok")
