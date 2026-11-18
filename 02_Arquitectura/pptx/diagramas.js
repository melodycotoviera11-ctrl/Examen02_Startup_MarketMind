const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.title = "MarketMind BI, diagramas de arquitectura";
pres.theme = { headFontFace: "Arial", bodyFontFace: "Arial" };
const F = "Arial";
const GRIS = "5B6B7A";

function caja(s, txt, x, y, w, h, o = {}) {
  s.addText(txt, { x, y, w, h, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.12,
    fill: { color: o.fill || "FFFFFF" }, line: { color: o.line || GRIS, width: o.lw || 1.2 },
    fontFace: F, fontSize: o.fs || 11, color: "1F1F1F", align: "center", valign: "middle",
    bold: !!o.bold, margin: 4, objectName: o.name || txt.split("\n")[0] });
}
function grupo(s, titulo, x, y, w, h) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.15, fill: { color: "EEF3F8" },
    line: { color: "C7D3DF", width: 1 }, objectName: "Grupo " + titulo });
  s.addText(titulo, { x, y: y + 0.05, w, h: 0.32, fontFace: F, fontSize: 11, bold: true, color: "1F1F1F",
    align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "Título " + titulo });
}
function flecha(s, x1, y1, x2, y2, conPunta = true) {
  if (!conPunta && x2 < x1) { [x1, y1, x2, y2] = [x2, y2, x1, y1]; }
  const o = { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.max(Math.abs(x2 - x1), 0.001), h: Math.max(Math.abs(y2 - y1), 0.001),
    line: { color: GRIS, width: 1.25 } };
  if (conPunta) o.line.endArrowType = "triangle";
  if ((y2 < y1) !== (x2 < x1)) o.flipV = true;
  if (x2 < x1) o.flipH = true;
  s.addShape(pres.shapes.LINE, o);
}

// ---------------------------------------------------------------- Diapositiva 1
let s = pres.addSlide();
s.background = { color: "FFFFFF" };
s.addText("Flujo de datos de MarketMind BI", { x: 0.4, y: 0.25, w: 12.5, h: 0.6, fontFace: F, fontSize: 26, bold: true,
  color: "1F1F1F", margin: 0, isTextBox: true, objectName: "Título" });

grupo(s, "1. Fuentes", 0.3, 1.1, 2.4, 6.0);
const fuentes = ["Sistema de facturación\nclientes, planes, facturas",
  "API de plataformas de anuncios\nMeta, Google, TikTok, IA beta\nresultados diarios",
  "Hoja de control de campañas\ncampanas.xlsx", "Registro de actividad\ndel panel (logs)", "Contabilidad\ncostos operativos"];
const cyF = [1.95, 3.05, 4.15, 5.2, 6.25];
fuentes.forEach((t, i) => caja(s, t, 0.42, cyF[i] - 0.42, 2.16, 0.84, { fs: 10 }));

const CY = 4.15; // eje central
grupo(s, "2. Recepción (staging)", 2.95, 3.25, 1.85, 1.75);
caja(s, "Carpeta datos_brutos\nCSV y Excel sin cambios", 3.03, CY - 0.38, 1.69, 0.9, { fs: 10 });
grupo(s, "3. ETL", 5.0, 3.25, 1.7, 1.75);
caja(s, "Power Query\nlimpieza, homologación,\nclaves y validaciones", 5.08, CY - 0.38, 1.54, 0.9, { fs: 10 });
grupo(s, "4. Data mart", 6.9, 3.25, 1.65, 1.75);
caja(s, "Modelo estrella\n4 hechos, 5 dimensiones\ny calendario", 6.98, CY - 0.38, 1.49, 0.9, { fs: 10 });
grupo(s, "5. Modelo semántico", 8.75, 3.25, 1.45, 1.75);
caja(s, "Medidas DAX\nroles RLS", 8.85, CY - 0.38, 1.25, 0.9, { fs: 10 });
grupo(s, "6. Dashboards", 10.4, 2.35, 1.4, 3.65);
const cyD = [3.15, 4.2, 5.25];
["Panel del cliente", "Desempeño comercial", "Uso y retención"].forEach((t, i) => caja(s, t, 10.5, cyD[i] - 0.35, 1.2, 0.7, { fs: 10 }));
grupo(s, "7. Usuarios", 11.95, 2.35, 1.2, 3.0);
caja(s, "Clientes\npymes y agencias\n(solo sus datos)", 12.0, 3.15 - 0.45, 1.1, 0.9, { fs: 9 });
caja(s, "Dirección de\nMarketMind", 12.0, 4.6 - 0.35, 1.1, 0.7, { fs: 9 });

cyF.forEach(y => flecha(s, 2.58, y, 3.03, CY + 0.07));
flecha(s, 4.72, CY + 0.07, 5.08, CY + 0.07);
flecha(s, 6.62, CY + 0.07, 6.98, CY + 0.07);
flecha(s, 8.47, CY + 0.07, 8.85, CY + 0.07);
cyD.forEach(y => flecha(s, 10.1, CY + 0.07, 10.5, y));
flecha(s, 11.7, 3.15, 12.0, 3.15);
flecha(s, 11.7, 4.2, 12.0, 4.5);
flecha(s, 11.7, 5.25, 12.0, 4.75);

// ---------------------------------------------------------------- Diapositiva 2
s = pres.addSlide();
s.background = { color: "FFFFFF" };
s.addText("Modelo dimensional de MarketMind BI", { x: 0.4, y: 0.25, w: 12.5, h: 0.6, fontFace: F, fontSize: 26, bold: true,
  color: "1F1F1F", margin: 0, isTextBox: true, objectName: "Título" });

const K = 0.0105, OX = 1.25, OY = 1.0; // escala desde el boceto en píxeles
const px = v => OX + v * K, py = v => OY + v * K;
function entidad(nombre, x1, y1, x2, lineas, hecho) {
  const x = px(x1), y = py(y1), w = (x2 - x1) * K, hh = 0.3, fila = 0.255;
  const h = hh + lineas.length * fila + 0.08;
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: hecho ? "EEF3F8" : "FFFFFF" },
    line: { color: hecho ? "1F4E79" : GRIS, width: 1.5 }, objectName: nombre + " marco" });
  s.addText(nombre, { x: x + 0.03, y: y + 0.03, w: w - 0.06, h: hh - 0.03, shape: pres.shapes.RECTANGLE,
    fill: { color: hecho ? "BDD7EE" : "D9D9D9" }, line: { color: hecho ? "BDD7EE" : "D9D9D9", width: 0 },
    fontFace: F, fontSize: 11, bold: true, color: "1F1F1F", align: "center", valign: "middle", margin: 0, objectName: nombre });
  s.addText(lineas.map((l, i) => ({ text: l.replace(/^_/, ""), options: { italic: l.startsWith("_"), breakLine: i < lineas.length - 1 } })),
    { x: x + 0.06, y: y + hh + 0.02, w: w - 0.1, h: lineas.length * fila, fontFace: F, fontSize: 10, color: "1F1F1F",
      align: "left", valign: "top", margin: 0, paraSpaceAfter: 5.5, isTextBox: true, objectName: nombre + " campos" });
}
function rel(x1, y1, x2, y2, lx, ly) {
  flecha(s, px(x1), py(y1), px(x2), py(y2), false);
  s.addText("1 : *", { x: px(lx), y: py(ly), w: 0.45, h: 0.22, fontFace: F, fontSize: 9, color: "1F1F1F", margin: 0,
    isTextBox: true, objectName: "Cardinalidad" });
}
entidad("Dim_Plan", 35, 42, 195, ["PK id_plan", "nombre, precio, límites"], false);
entidad("Fact_Facturacion", 265, 8, 510, ["PK id_factura", "FK id_cliente, id_plan", "FK fecha_emision", "subtotal, descuento, iva, total", "dias_para_pagar, estado_pago", "_Grano una factura por cliente y mes"], true);
entidad("Dim_Cliente", 7, 222, 222, ["PK id_cliente", "nombre, industria, tamaño", "provincia, canal_adquisicion", "fecha_alta, fecha_baja, estado"], false);
entidad("Fact_UsoPlataforma", 275, 209, 502, ["PK id_sesion", "FK id_cliente, fecha", "duracion_min, alertas_revisadas", "reporte_descargado, pagina", "_Grano una sesión"], true);
entidad("Dim_Calendario", 557, 222, 765, ["PK Fecha", "Año, Mes, NombreMes", "Trimestre, DíaSemana", "EsFinDeSemana, Temporada"], false);
entidad("Fact_Costos", 812, 222, 1027, ["PK id_costo", "FK fecha, concepto, tipo_costo", "monto_crc", "_Grano un concepto por mes"], true);
entidad("Fact_ResultadosCampana", 281, 394, 495, ["PK id_resultado", "FK id_campana, id_cliente", "FK id_canal, fecha", "impresiones, clics, gasto", "conversiones, ingresos", "_Grano una campaña por día"], true);
entidad("Dim_Campana", 10, 455, 217, ["PK id_campana", "marca, industria_marca", "objetivo, fechas, presupuesto"], false);
entidad("Dim_Canal", 574, 475, 748, ["PK id_canal", "nombre, plataforma, tipo"], false);

rel(195, 88, 265, 92, 205, 70);
rel(205, 222, 265, 185, 210, 192);
rel(510, 180, 570, 222, 530, 178);
rel(222, 288, 275, 288, 228, 270);
rel(502, 288, 557, 288, 510, 270);
rel(765, 288, 812, 288, 770, 270);
rel(195, 355, 281, 410, 212, 378);
rel(570, 355, 495, 410, 540, 378);
rel(217, 500, 281, 497, 228, 480);
rel(495, 500, 574, 508, 515, 482);

pres.writeFile({ fileName: "Diagramas_Arquitectura_MarketMind.pptx" }).then(() => console.log("ok"));
