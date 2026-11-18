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
const LH = 0.18, HH = 0.32;
const altura = n => HH + n * LH + 0.1;
function ent(nombre, x, y, w, campos, fact) {
  const h = altura(campos.length);
  s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: fact ? "EEF3F8" : "FFFFFF" },
    line: { color: fact ? "1F4E79" : GRIS, width: 1.5 }, objectName: nombre + " marco" });
  s.addText(nombre, { x: x + 0.03, y: y + 0.03, w: w - 0.06, h: HH - 0.04, shape: pres.shapes.RECTANGLE,
    fill: { color: fact ? "BDD7EE" : "D9D9D9" }, line: { color: fact ? "BDD7EE" : "D9D9D9", width: 0 },
    fontFace: F, fontSize: 11, bold: true, color: "1F1F1F", align: "center", valign: "middle", margin: 0, objectName: nombre });
  s.addText(campos.map((c, k) => {
      const clave = /^(PK|FK) /.test(c);
      return { text: clave ? c : "      " + c, options: { breakLine: k < campos.length - 1 } };
    }), { x: x + 0.07, y: y + HH + 0.03, w: w - 0.1, h: campos.length * LH, fontFace: F, fontSize: 10,
      color: "1F1F1F", align: "left", valign: "top", margin: 0, lineSpacing: 13, isTextBox: true, objectName: nombre + " campos" });
  return { x, y, w, h, cx: x + w / 2, cy: y + h / 2, r: x + w, b: y + h };
}
function linea(x1, y1, x2, y2, dimEnX1 = true) {
  flecha(s, x1, y1, x2, y2, false);
  const dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy), ux = dx / L, uy = dy / L;
  const etq = (t, px, py) => s.addText(t, { x: px - 0.12, y: py - 0.12, w: 0.24, h: 0.24, fontFace: F, fontSize: 11,
    bold: true, color: "1F1F1F", align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "Cardinalidad " + t });
  const off = (px, py) => [px + uy * 0.15, py - ux * 0.15];
  const d = Math.min(0.3, L * 0.3); const a = off(x1 + ux * d, y1 + uy * d), b = off(x2 - ux * d, y2 - uy * d);
  etq(dimEnX1 ? "1" : "*", a[0], a[1]);
  etq(dimEnX1 ? "*" : "1", b[0], b[1]);
}
const XC = 4.85, WC = 2.4;
const fac = ent("Fact_Facturacion", XC, 0.2, WC, ["PK id_factura", "FK id_cliente", "FK id_plan", "FK fecha_emision", "subtotal", "descuento", "iva", "total", "dias_para_pagar", "estado_pago"], true);
const uso = ent("Fact_UsoPlataforma", XC, fac.b + 0.25, WC, ["PK id_sesion", "FK id_cliente", "FK fecha", "duracion_min", "alertas_revisadas", "reporte_descargado", "pagina", "dispositivo", "rol_usuario"], true);
const res = ent("Fact_ResultadosCampana", XC, uso.b + 0.25, WC, ["PK id_resultado", "FK id_campana", "FK id_cliente", "FK id_canal", "FK id_plan", "FK fecha", "impresiones", "clics", "gasto", "conversiones", "ingresos"], true);
const cliCampos = ["PK id_cliente", "nombre", "industria", "tamaño", "provincia", "canal_adquisicion", "fecha_alta", "fecha_baja", "estado"];
const cli = ent("Dim_Cliente", 2.15, uso.cy - altura(cliCampos.length) / 2, 2.0, cliCampos, false);
const plaCampos = ["PK id_plan", "nombre", "precio", "límites"];
const pla = ent("Dim_Plan", 0.25, uso.cy - altura(plaCampos.length) / 2, 1.55, plaCampos, false);
const calCampos = ["PK Fecha", "Año", "Mes", "NombreMes", "AñoMes", "Trimestre", "DíaSemana", "EsFinDeSemana", "Temporada"];
const cal = ent("Dim_Calendario", 7.95, uso.cy - altura(calCampos.length) / 2, 2.1, calCampos, false);
const cosCampos = ["PK id_costo", "FK fecha", "concepto", "tipo_costo", "monto_crc"];
const cos = ent("Fact_Costos", 10.75, uso.cy - altura(cosCampos.length) / 2, 2.15, cosCampos, true);
const can = ent("Dim_Canal", 7.95, res.y + 0.28, 1.85, ["PK id_canal", "nombre", "plataforma", "tipo"], false);
const cam = ent("Dim_Campana", 10.35, res.y + 0.45, 2.4, ["PK id_campana", "nombre_campana", "marca", "industria_marca", "objetivo", "fecha_inicio", "fecha_fin", "presupuesto_diario"], false);

// Lado izquierdo
linea(pla.x + 0.75, pla.y, XC, fac.y + 0.45);            // Plan - Facturación
linea(pla.x + 0.75, pla.b, XC, res.b - 0.45);            // Plan - Resultados
linea(cli.r - 0.25, cli.y, XC, fac.b - 0.3);             // Cliente - Facturación
linea(cli.r, uso.cy, XC, uso.cy);                        // Cliente - Uso
linea(cli.r - 0.25, cli.b, XC, res.y + 0.35);            // Cliente - Resultados
// Lado derecho
linea(cal.x + 0.25, cal.y, XC + WC, fac.b - 0.3, true);  // Calendario - Facturación
linea(cal.x, uso.cy, XC + WC, uso.cy, true);             // Calendario - Uso
linea(cal.x + 0.25, cal.b, XC + WC, res.y + 0.3, true);  // Calendario - Resultados
linea(cal.r, cos.cy, cos.x, cos.cy, true);               // Calendario - Costos
linea(can.x, can.cy, XC + WC, can.cy, true);             // Canal - Resultados
linea(cam.x, cam.cy + 0.3, XC + WC, res.b - 0.35, true); // Campaña - Resultados

pres.writeFile({ fileName: "Diagramas_Arquitectura_MarketMind.pptx" }).then(() => console.log("ok"));
