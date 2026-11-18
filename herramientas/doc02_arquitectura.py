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

d.h1("Arquitectura de datos de MarketMind BI")
d.parrafo("MarketMind vende un servicio de inteligencia de negocios, por lo que su arquitectura cumple dos funciones. "
          "El primero es entregarle a cada cliente un panel con los resultados de sus campañas. El segundo es "
          "darle a la dirección de la startup el seguimiento de sus ventas, costos, uso y cancelaciones. Ambas "
          "salen del mismo flujo de datos, que se describe a continuación. Todos los datos del prototipo son "
          "simulados y se generan con el script de la carpeta 03_Datos_Sinteticos.")

d.h2("Orígenes de datos")
d.leyenda("Fuentes del prototipo, qué producen, cada cuánto y quién responde por ellas")
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
        [2.3, 2.6, 3.4, 2.3, 1.6], size=18, negrita_col1=True)

d.h2("Flujo de extremo a extremo")
d.leyenda("Flujo de datos desde las fuentes hasta los perfiles de usuario", tipo="Figura")
d.imagen(B + "flujo_datos.png", 18.5)
d.parrafo("Las fuentes dejan sus archivos sin cambios en la carpeta datos_brutos, que funciona como área de "
          "recepción. Power Query hace el ETL, que incluye tipos de datos, quitar duplicados, homologar categorías, "
          "derivar claves y validar. El resultado es un data mart con forma de estrella dentro de Power BI. Sobre ese "
          "modelo se crean las medidas DAX y los roles de seguridad, que alimentan tres páginas. El panel del cliente "
          "lo ven las pymes y agencias, cada una solo con sus datos. Las páginas comercial y de uso las ve la dirección.")

d.h2("Datos operacionales y hechos analíticos")
d.parrafo("Los archivos de origen son datos operacionales, porque registran lo que ocurre en la operación diaria y vienen "
          "con errores de captura. En el modelo se separan en dimensiones, que describen el quién, el qué y el "
          "cuándo, y en tablas de hechos, que guardan lo que se mide. Cada tabla de hechos tiene un grano definido.", despues=80)
d.leyenda("Tablas de hechos del modelo")
d.tabla(["Tabla de hechos (Fact)", "Proceso", "Granularidad", "Medidas base"],
        [["Fact_Facturacion", "Comercial de MarketMind", "Una factura por cliente por mes", "subtotal, descuento, IVA, total, días para pagar"],
         ["Fact_ResultadosCampana", "Servicio que recibe el cliente", "Una campaña por día", "impresiones, clics, gasto, conversiones, ingresos atribuidos"],
         ["Fact_UsoPlataforma", "Uso del producto", "Una sesión de un usuario", "minutos, alertas revisadas, reportes descargados"],
         ["Fact_Costos", "Rentabilidad de MarketMind", "Un concepto de costo por mes", "monto en colones"]],
        [3.1, 2.3, 2.5, 3.9], size=18, negrita_col1=True)

d.h2("Modelo dimensional")
d.leyenda("Modelo lógico en estrella con claves primarias y foráneas (la granularidad está en la Tabla 2)", tipo="Figura")
d.imagen(B + "modelo_dimensional.png", 18.0)
d.parrafo("El modelo tiene tres dimensiones compartidas. Dim_Calendario filtra las cuatro tablas de hechos, Dim_Cliente "
          "filtra facturación, uso y resultados, y Dim_Plan filtra facturación y resultados, lo que permite comparar el "
          "valor que recibe cada plan. Dim_Campana y Dim_Canal describen los resultados. Todas las relaciones son de uno a "
          "muchos, con filtro en una sola dirección desde la dimensión hacia el hecho, sin caminos ambiguos ni relaciones "
          "muchos a muchos. Las cancelaciones de cada mes se cuentan con una medida que compara Dim_Cliente[fecha_baja] con "
          "las fechas del calendario, sin agregar otra relación.")
d.parrafo("Algunas claves se derivan en el ETL. El id_canal se obtiene al homologar el nombre del canal y combinarlo "
          "con canales.csv. El id_cliente de los resultados se trae desde campañas, para que el filtro por cliente no "
          "pase por Dim_Campana. El id_plan de los resultados es el plan vigente del cliente en ese mes, tomado de la "
          "factura del mismo periodo, o el plan inicial durante el mes de prueba gratis. La tabla calendario se crea en "
          "Power BI con DAX, del 1 de noviembre de 2025 al 31 de octubre de 2026, e incluye año, mes, AñoMes para "
          "ordenar, trimestre, día de la semana, fin de semana y temporada comercial.")

d.h2("Calidad, seguridad y actualización")
d.leyenda("Definición conceptual de controles")
d.tabla(["Aspecto", "Cómo se maneja"],
        [["Controles de calidad",
          "En Power Query se corrigen las once anomalías sembradas y se valida que las claves sean únicas, que todo "
          "resultado tenga una campaña y todo hecho un cliente existente, que el gasto no sea negativo, que los clics "
          "no superen las impresiones y que las fechas estén dentro del periodo. Se comparan los conteos de filas antes "
          "y después de limpiar."],
         ["Permisos de acceso",
          "La dirección de MarketMind ve todo el modelo. Cada cliente entra con su cuenta y un rol de seguridad por "
          "filas (RLS) filtra Dim_Cliente por su id_cliente, así una agencia ve solo sus marcas y nunca las de otro "
          "cliente. En producción el filtro sería dinámico, con una tabla que relaciona el correo de USERPRINCIPALNAME() "
          "con el cliente. En el prototipo se prueba con roles fijos y cuentas con permiso de lector (Viewer)."],
         ["Frecuencia de actualización",
          "Los resultados de campañas llegan cada madrugada y el modelo se actualiza de forma programada en Power BI "
          "Service todos los días a las 6 de la mañana. Facturación y costos cambian una vez al mes, y el uso del panel "
          "se consolida a diario."],
         ["Protección de datos",
          "El modelo no guarda datos personales de los compradores finales, solo cifras agregadas por campaña y día. "
          "Las credenciales de las APIs se guardan cifradas y fuera del informe. Se aplica el principio de mínimo "
          "privilegio y se respeta la Ley 8968 de Protección de la Persona frente al Tratamiento de sus Datos "
          "Personales. En este prototipo todos los datos son ficticios."]],
        [2.4, 9.4], size=18, negrita_col1=True)

d.guardar("/home/claude/examen2/02_Arquitectura/02_Arquitectura.docx")
print("ok")
