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
d.parrafo("MarketMind vende un servicio de inteligencia de negocios, por lo que su arquitectura cumple dos funciones. "
          "La primera es entregar a cada cliente un panel con los resultados de sus campañas publicitarias. La segunda "
          "es dar a la dirección de la startup el seguimiento de sus ingresos, costos, uso del producto y cancelaciones. "
          "Ambas salen del mismo flujo de datos. En el prototipo todos los datos son simulados y se generan con el "
          "script de la carpeta 03_Datos_Sinteticos.")

d.h2("Orígenes de datos")
d.parrafo("La solución recibe información de seis orígenes. Cada uno representa un sistema que la startup tendría en "
          "operación real y tiene un área responsable de que los datos lleguen completos y a tiempo.", despues=80)
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
d.imagen(B + "flujo_datos.png", 18.5)
d.leyenda("Función de cada capa de la arquitectura")
d.tabla(["Capa", "Qué ocurre en ella", "Herramienta"],
        [["Recepción (staging)", "Los archivos se guardan tal como llegan en la carpeta datos_brutos. No se corrigen a mano, "
          "por lo que siempre es posible volver al dato original.", "Carpeta de archivos"],
         ["Transformación (ETL)", "Se asignan tipos de datos, se quitan duplicados, se homologan categorías, se derivan claves "
          "y se validan rangos y relaciones.", "Power Query"],
         ["Almacenamiento analítico", "Los datos limpios se organizan en un modelo en estrella, con tablas de hechos y "
          "dimensiones.", "Modelo de Power BI"],
         ["Modelo semántico", "Se definen las relaciones, las medidas DAX y los roles de seguridad. Es la capa que convierte "
          "los datos en indicadores de negocio.", "Power BI Desktop"],
         ["Visualización y acceso", "El informe se publica en Power BI Service. Los clientes ven el panel de sus "
          "campañas y la dirección ve las páginas comercial y de uso.", "Power BI Service"]],
        [2.4, 7.4, 2.0], size=T, negrita_col1=True)

d.h2("Datos operacionales y hechos analíticos")
d.parrafo("Los archivos de origen son datos operacionales, porque registran lo que ocurre en la operación diaria y "
          "pueden traer errores de captura. En el modelo se separan en dos tipos de tablas. Las tablas de hechos (Fact) "
          "guardan los eventos que se miden, como una factura o el resultado diario de una campaña. Las dimensiones "
          "(Dim) describen el contexto de esos eventos, es decir, quién, qué y cuándo. Cada tabla de hechos tiene "
          "una granularidad definida, que indica qué representa exactamente cada fila.", despues=80)
d.leyenda("Tablas de hechos, proceso que miden y granularidad")
d.tabla(["Tabla de hechos", "Proceso", "Granularidad", "Medidas base"],
        [["Fact_Facturacion", "Comercial de MarketMind", "Una factura por cliente por mes", "subtotal, descuento, IVA, total, días para pagar"],
         ["Fact_ResultadosCampana", "Servicio que recibe el cliente", "Una campaña por día", "impresiones, clics, gasto, conversiones, ingresos atribuidos"],
         ["Fact_UsoPlataforma", "Uso del producto", "Una sesión de un usuario", "minutos, alertas revisadas, reportes descargados"],
         ["Fact_Costos", "Rentabilidad de MarketMind", "Un concepto de costo por mes", "monto en colones"]],
        [3.1, 2.3, 2.5, 3.9], size=T, negrita_col1=True)

d.h2("Modelo dimensional")
d.leyenda("Modelo lógico en estrella con claves primarias, claves foráneas y cardinalidad", tipo="Figura")
d.imagen(B + "modelo_dimensional.png", 18.0)
d.parrafo("El modelo sigue un esquema en estrella. Las tablas de hechos están al centro y cada una se relaciona con "
          "las dimensiones que la describen. Todas las relaciones son de uno a muchos, como indican el 1 y el asterisco "
          "del diagrama, y filtran en una sola dirección, desde la dimensión hacia la tabla de hechos. Las tablas de "
          "hechos no se relacionan entre sí, de modo que no hay caminos ambiguos ni relaciones de muchos a muchos.", despues=80)
d.leyenda("Dimensiones del modelo")
d.tabla(["Dimensión", "Qué describe", "Atributos principales", "Tablas de hechos que filtra"],
        [["Dim_Calendario", "Las fechas del periodo, del 1 de noviembre de 2025 al 31 de octubre de 2026. Se crea con DAX.",
          "Año, mes, AñoMes para ordenar, trimestre, día de la semana, fin de semana y temporada comercial",
          "Las cuatro (compartida)"],
         ["Dim_Cliente", "Cada empresa o agencia que contrata MarketMind",
          "Industria, tamaño, provincia, canal de adquisición, fecha de alta, fecha de baja y estado",
          "Facturación, uso y resultados (compartida)"],
         ["Dim_Plan", "Los planes de suscripción Starter, Growth y Agencia", "Precio mensual y límites de marcas y canales",
          "Facturación y resultados (compartida)"],
         ["Dim_Campana", "Cada campaña publicitaria conectada", "Nombre, marca, industria de la marca, objetivo, fechas y presupuesto diario",
          "Resultados"],
         ["Dim_Canal", "Los cinco canales de anuncios", "Nombre, plataforma y tipo de canal", "Resultados"]],
        [2.2, 3.4, 3.9, 2.3], size=T, negrita_col1=True)
d.parrafo("Tres dimensiones son compartidas, lo que permite cruzar procesos distintos con los mismos filtros. Por "
          "ejemplo, al elegir un cliente en Dim_Cliente se filtran al mismo tiempo sus facturas, su uso del panel y los "
          "resultados de sus campañas. Algunas claves se derivan en el ETL. El id_canal se obtiene al homologar el nombre "
          "del canal y combinarlo con canales.csv. El id_cliente de los resultados se trae desde campañas, para que el "
          "filtro por cliente no dependa de Dim_Campana. El id_plan de los resultados corresponde al plan vigente del "
          "cliente en ese mes, tomado de la factura del mismo periodo, o al plan inicial durante el mes de prueba gratis.", antes=120)

d.h2("Modelo semántico y medidas")
d.parrafo("Sobre el modelo se definen medidas DAX, que son cálculos que responden de forma automática a los filtros que "
          "la persona usuaria elige en el informe. Las medidas se agrupan según la pregunta de negocio que responden, y "
          "sus fórmulas completas se encuentran en el resumen técnico.", despues=80)
d.leyenda("Grupos de medidas del modelo semántico")
d.tabla(["Grupo", "Medidas", "Pregunta que responden"],
        [["Comerciales", "Ingresos, clientes activos, ticket medio, variación mensual de ingresos e ingresos acumulados del año",
          "¿Cuánto factura MarketMind, con cuántos clientes y cómo cambia cada mes?"],
         ["Financieras", "Costos, margen y margen porcentual", "¿El negocio es rentable y desde qué mes?"],
         ["Retención y uso", "Clientes cancelados, tasa de cancelación y sesiones por cliente",
          "¿Cuántos clientes se pierden y quiénes están dejando de usar el panel?"],
         ["Valor para el cliente", "Gasto publicitario, costo por venta (CAC), retorno de la inversión publicitaria (ROAS) y gasto promedio móvil de tres meses",
          "¿Cuánto le cuesta cada venta al cliente y cuánto recupera por cada colón invertido?"]],
        [2.2, 5.4, 4.2], size=T, negrita_col1=True)

d.h2("Calidad, seguridad y actualización")
d.leyenda("Definición conceptual de controles")
d.tabla(["Aspecto", "Cómo se maneja"],
        [["Controles de calidad",
          "En Power Query se corrigen las once anomalías sembradas en los datos brutos. Luego se valida que las claves sean "
          "únicas, que cada resultado tenga una campaña y cada hecho un cliente existente, que el gasto no sea negativo, que "
          "los clics no superen las impresiones y que las fechas estén dentro del periodo. También se comparan los conteos "
          "de filas antes y después de la limpieza."],
         ["Permisos de acceso",
          "La dirección de MarketMind tiene acceso a todo el modelo. Cada cliente ingresa con su propia cuenta y un rol de "
          "seguridad por filas (RLS) filtra Dim_Cliente según su id_cliente, de modo que una agencia solo ve sus marcas. En "
          "producción el filtro sería dinámico, con una tabla que relaciona el correo de USERPRINCIPALNAME() con el cliente. "
          "En el prototipo se usan roles fijos y la prueba se hace con cuentas de lector (Viewer)."],
         ["Frecuencia de actualización",
          "Los resultados de campañas llegan cada madrugada y el modelo se actualiza de forma programada en Power BI Service "
          "todos los días a las 6 de la mañana. Facturación y costos cambian una vez al mes, y el uso del panel se consolida "
          "a diario."],
         ["Protección de datos",
          "El modelo no guarda datos personales de los compradores finales, solo cifras agregadas por campaña y día. Las "
          "credenciales de las APIs se guardan cifradas y fuera del informe, y cada persona recibe solo los permisos que "
          "necesita. El diseño respeta la Ley 8968 de Protección de la Persona frente al Tratamiento de sus Datos Personales. "
          "En este prototipo todos los datos son ficticios."]],
        [2.4, 9.4], size=T, negrita_col1=True)

d.guardar("/home/claude/examen2/02_Arquitectura/02_Arquitectura.docx")
print("ok")
