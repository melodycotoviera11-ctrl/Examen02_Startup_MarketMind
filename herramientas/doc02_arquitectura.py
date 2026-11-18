import sys
sys.path.insert(0, "/home/claude/examen2/herramientas")
from plantilla import Documento

INTEGRANTES = [
    "[[Carné]], Valeria Abarca Chacón",
    "2024224269, Melody Onid Coto Viera",
    "[[Carné]], Pamela Cruz Segura",
]
d = Documento("Examen parcial 02.", "MarketMind BI, arquitectura de datos y modelo dimensional",
              INTEGRANTES, "martes 24 de noviembre de 2026")
B = "/home/claude/examen2/02_Arquitectura/"
T = 18  # tamaño de letra en tablas (9 pt)

d.h1("Arquitectura de datos de MarketMind BI")
d.parrafo("La arquitectura de MarketMind cumple dos funciones. Entrega a cada cliente un panel con los resultados de "
          "sus campañas y da a la dirección de la startup el seguimiento de ingresos, costos, uso y cancelaciones. Ambas "
          "salen del mismo flujo de datos. Todos los datos del prototipo son simulados.", despues=100)

d.h2("Orígenes de datos")
d.leyenda("Orígenes de datos, contenido, frecuencia y responsable lógico")
d.tabla(["Origen", "Archivo", "Qué produce", "Frecuencia", "Responsable lógico"],
        [["Sistema de facturación", "clientes.csv, planes.csv, facturas.csv",
          "Clientes, planes y una factura por cliente al mes", "Clientes a diario, facturas el día 1 de cada mes", "Finanzas y ventas"],
         ["API de plataformas de anuncios", "resultados_campanas.csv",
          "Impresiones, clics, gasto, conversiones e ingresos por campaña y día", "Diaria, cada madrugada", "Integraciones"],
         ["Hoja de control de campañas", "campanas.xlsx",
          "Campañas conectadas, marca, canal, objetivo y presupuesto", "Cada vez que se conecta una campaña", "Soporte al cliente"],
         ["Registro de actividad del panel", "uso_plataforma.csv",
          "Una fila por sesión, con duración, página, alertas y descargas", "Cada hora, consolidado diario", "Producto"],
         ["Contabilidad", "costos_operativos.csv",
          "Costos tecnológicos, comerciales y operativos del mes", "Mensual", "Finanzas"],
         ["Catálogo interno", "canales.csv", "Canales de anuncios y su plataforma", "Cuando se agrega un canal", "Producto"]],
        [2.3, 2.6, 3.4, 2.3, 1.6], size=T, negrita_col1=True)

d.h2("Flujo de extremo a extremo")
d.leyenda("Flujo de datos desde los orígenes hasta los perfiles de usuario", tipo="Figura")
d.imagen(B + "flujo_datos.png", 16.0)
d.parrafo("Los archivos llegan sin cambios a la carpeta datos_brutos (recepción). Power Query realiza el ETL y los datos "
          "limpios forman el modelo en estrella, donde se definen relaciones, medidas DAX y roles de seguridad. El informe se "
          "publica en Power BI Service para los clientes y la dirección.")

d.h2("Datos operacionales y hechos analíticos")
d.parrafo("Los archivos de origen son datos operacionales, porque registran la operación diaria y pueden traer errores. "
          "En el modelo se separan en tablas de hechos (Fact), que guardan los eventos que se miden, y dimensiones (Dim), "
          "que describen su contexto. La granularidad indica qué representa cada fila de una tabla de hechos.", despues=80)
d.leyenda("Tablas de hechos, proceso que miden y granularidad")
d.tabla(["Tabla de hechos", "Proceso", "Granularidad", "Medidas base"],
        [["Fact_Facturacion", "Comercial de MarketMind", "Una factura por cliente por mes", "subtotal, descuento, IVA, total, días para pagar"],
         ["Fact_ResultadosCampana", "Servicio que recibe el cliente", "Una campaña por día", "impresiones, clics, gasto, conversiones, ingresos atribuidos"],
         ["Fact_UsoPlataforma", "Uso del producto", "Una sesión de un usuario", "minutos, alertas revisadas, reportes descargados"],
         ["Fact_Costos", "Rentabilidad de MarketMind", "Un concepto de costo por mes", "monto en colones"]],
        [3.1, 2.3, 2.5, 3.9], size=T, negrita_col1=True)

d.h2("Modelo dimensional")
d.leyenda("Modelo lógico en estrella con claves primarias, claves foráneas y cardinalidad", tipo="Figura")
d.imagen(B + "modelo_dimensional.png", 13.5)
d.leyenda("Dimensiones del modelo")
d.tabla(["Dimensión", "Qué describe", "Atributos principales", "Tablas de hechos que filtra"],
        [["Dim_Calendario", "Fechas de nov. 2025 a oct. 2026, creada con DAX",
          "Año, mes, AñoMes, trimestre, día de la semana, fin de semana y temporada",
          "Las cuatro"],
         ["Dim_Cliente", "Empresas y agencias clientes",
          "Industria, tamaño, provincia, canal de adquisición, fechas de alta y baja",
          "Facturación, uso y resultados"],
         ["Dim_Plan", "Planes Starter, Growth y Agencia", "Precio mensual y límites de marcas y canales",
          "Facturación y resultados"],
         ["Dim_Campana", "Campañas publicitarias conectadas", "Nombre, marca, industria, objetivo, fechas y presupuesto",
          "Resultados"],
         ["Dim_Canal", "Canales de anuncios", "Nombre, plataforma y tipo de canal", "Resultados"]],
        [2.2, 3.0, 4.4, 2.2], size=T, negrita_col1=True)
d.parrafo("Todas las relaciones son de uno a muchos, filtran desde la dimensión hacia el hecho y no hay relaciones entre "
          "tablas de hechos, por lo que no existen caminos ambiguos. Dim_Calendario, Dim_Cliente y Dim_Plan son compartidas y "
          "permiten cruzar procesos con un mismo filtro. En el ETL se derivan el id_canal (homologando el canal), el "
          "id_cliente de los resultados (desde campañas) y su id_plan (plan vigente en ese mes). Las medidas DAX se explican "
          "en el resumen técnico.", antes=120)

d.h2("Calidad, seguridad y actualización")
d.leyenda("Definición conceptual de controles")
d.tabla(["Aspecto", "Cómo se maneja"],
        [["Controles de calidad",
          "Power Query corrige las once anomalías sembradas y valida claves únicas, integridad referencial, gasto no "
          "negativo, clics menores o iguales a impresiones y fechas dentro del periodo, comparando conteos antes y después."],
         ["Permisos de acceso",
          "La dirección ve todo el modelo. Un rol de seguridad por filas (RLS) filtra Dim_Cliente para que cada cliente vea "
          "solo sus datos. En producción sería dinámico con USERPRINCIPALNAME() y en el prototipo se prueba con cuentas Viewer."],
         ["Frecuencia de actualización",
          "Actualización diaria programada en Power BI Service a las 6 de la mañana. Facturación y costos cambian cada mes."],
         ["Protección de datos",
          "Solo cifras agregadas, sin datos personales de compradores, credenciales cifradas, permisos mínimos y respeto a la "
          "Ley 8968 de Protección de Datos Personales."]],
        [2.4, 9.4], size=T, negrita_col1=True)

d.guardar("/home/claude/examen2/02_Arquitectura/02_Arquitectura.docx")
print("ok")
