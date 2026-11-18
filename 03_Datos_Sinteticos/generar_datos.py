"""
MarketMind BI · Generador de datos sintéticos
Examen parcial 02 · Emprendimiento BI

TODOS LOS DATOS QUE PRODUCE ESTE SCRIPT SON SIMULADOS.
Las empresas, campañas, montos y usuarios son ficticios y no representan
resultados de ninguna empresa real.

Uso
    python generar_datos.py
    python generar_datos.py --semilla 2026 --salida datos_brutos

Requisitos
    Python 3.10 o superior, pandas, numpy, openpyxl
    pip install pandas numpy openpyxl

Con la misma semilla siempre se generan exactamente los mismos archivos.
"""

import argparse
import os
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Parámetros generales
# ---------------------------------------------------------------------------
SEMILLA_POR_DEFECTO = 2026
FECHA_INICIO = date(2025, 11, 1)
FECHA_FIN = date(2026, 10, 31)
TOTAL_CLIENTES = 40
TASA_IVA = 0.13

PLANES = [
    # id, nombre, precio mensual en colones, marcas, canales, alertas
    ("PLN-01", "Starter", 10000, 1, 2, "No"),
    ("PLN-02", "Growth", 30000, 1, 5, "Sí"),
    ("PLN-03", "Agencia", 70000, 10, 5, "Sí"),
]
PRECIO_PLAN = {p[0]: p[2] for p in PLANES}
CANALES_PERMITIDOS = {p[0]: p[4] for p in PLANES}

CANALES = [
    # id, nombre, plataforma, tipo, CPM base (colones), CTR base, conversión base
    ("CAN-01", "Facebook Ads", "Meta", "Redes sociales", 1800, 0.011, 0.022),
    ("CAN-02", "Instagram Ads", "Meta", "Redes sociales", 2200, 0.009, 0.026),
    ("CAN-03", "Google Ads", "Google", "Buscador", 9500, 0.040, 0.024),
    ("CAN-04", "TikTok Ads", "TikTok", "Video corto", 1200, 0.007, 0.012),
    ("CAN-05", "Anuncios en IA (beta)", "Asistentes de IA", "Conversacional", 9000, 0.020, 0.032),
]
# Canal en versión beta. Solo para planes Growth y Agencia desde junio de 2026.
# Las categorías de salud quedan excluidas, como en los pilotos reales de anuncios en IA.
INICIO_BETA_IA = date(2026, 6, 1)
AFINIDAD_IA = {"Moda y accesorios": 0.9, "Restaurantes y cafeterías": 0.6, "Salud y estética": 0.0,
               "Fitness y gimnasios": 0.9, "Educación y cursos": 1.25, "Tecnología y electrónica": 1.35}
CANAL_INFO = {c[0]: c for c in CANALES}

# Industria: ticket promedio (colones) y afinidad por canal (multiplica la conversión)
INDUSTRIAS = {
    "Moda y accesorios": (18000, {"CAN-01": 1.0, "CAN-02": 1.45, "CAN-03": 0.8, "CAN-04": 1.3}),
    "Restaurantes y cafeterías": (9000, {"CAN-01": 1.3, "CAN-02": 1.25, "CAN-03": 0.9, "CAN-04": 1.0}),
    "Salud y estética": (35000, {"CAN-01": 1.0, "CAN-02": 1.1, "CAN-03": 1.45, "CAN-04": 0.8}),
    "Fitness y gimnasios": (25000, {"CAN-01": 1.0, "CAN-02": 1.15, "CAN-03": 0.9, "CAN-04": 1.4}),
    "Educación y cursos": (38000, {"CAN-01": 1.1, "CAN-02": 0.9, "CAN-03": 1.3, "CAN-04": 0.9}),
    "Tecnología y electrónica": (48000, {"CAN-01": 0.9, "CAN-02": 0.9, "CAN-03": 1.5, "CAN-04": 0.8}),
}

PROVINCIAS = ["San José", "Heredia", "Alajuela", "Cartago", "Puntarenas", "Guanacaste", "Limón"]
PESO_PROVINCIAS = [0.38, 0.17, 0.16, 0.14, 0.06, 0.06, 0.03]

CANALES_ADQUISICION = ["Instagram", "LinkedIn", "Webinar", "Referido", "Alianza cámara de comercio"]

# Estacionalidad del mercado costarricense (gasto y ventas)
ESTACIONALIDAD = {
    11: 1.25,  # Black Friday
    12: 1.35,  # Navidad y aguinaldo
    1: 0.75,   # cuesta de enero
    2: 1.00,   # regreso a clases
    3: 0.95,
    4: 0.88,   # Semana Santa
    5: 1.00,
    6: 0.95,
    7: 1.05,   # vacaciones de medio año
    8: 1.20,   # Día de la Madre (15 de agosto)
    9: 1.00,   # mes patrio
    10: 0.95,
}

PALABRAS_A = ["Luna", "Aurora", "Coral", "Brisa", "Roble", "Ceiba", "Nube", "Jade", "Sol",
              "Volcán", "Colibrí", "Lirio", "Monte", "Río", "Tucán", "Guaria", "Arena", "Faro"]
PREFIJOS = {
    "Moda y accesorios": ["Boutique", "Moda", "Tienda", "Estilo"],
    "Restaurantes y cafeterías": ["Café", "Soda", "Cocina", "Panadería"],
    "Salud y estética": ["Clínica", "Spa", "Centro Estético", "Consultorio"],
    "Fitness y gimnasios": ["Gimnasio", "Estudio", "Crossfit", "Box"],
    "Educación y cursos": ["Academia", "Instituto", "Escuela", "Cursos"],
    "Tecnología y electrónica": ["Tecno", "Digital", "Electro", "Compu"],
}
SUFIJOS = ["CR", "Plus", "Studio", "& Co.", "Express", "Central", ""]


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def meses_entre(inicio, fin):
    """Lista de primeros días de mes entre dos fechas, ambos extremos incluidos."""
    meses = []
    actual = date(inicio.year, inicio.month, 1)
    while actual <= fin:
        meses.append(actual)
        actual = date(actual.year + (actual.month // 12), actual.month % 12 + 1, 1)
    return meses


def fin_de_mes(d):
    siguiente = date(d.year + (d.month // 12), d.month % 12 + 1, 1)
    return siguiente - timedelta(days=1)


class Generador:
    def __init__(self, semilla):
        self.semilla = semilla
        self.rng = np.random.default_rng(semilla)
        self.nombres_usados = set()
        self.anomalias = []

    # ------------------------------------------------------------------
    def nombre_empresa(self, industria):
        for _ in range(200):
            nombre = f"{self.rng.choice(PREFIJOS[industria])} {self.rng.choice(PALABRAS_A)} {self.rng.choice(SUFIJOS)}".strip()
            if nombre not in self.nombres_usados:
                self.nombres_usados.add(nombre)
                return nombre
        raise RuntimeError("No se pudo generar un nombre único")

    # ------------------------------------------------------------------
    def generar_clientes(self):
        rng = self.rng
        meses = meses_entre(FECHA_INICIO, date(2026, 9, 1))
        # Lanzamiento fuerte en noviembre y crecimiento gradual
        pesos = np.array([8, 3, 2, 3, 3, 3, 3, 3, 4, 4, 4], dtype=float)
        pesos = pesos / pesos.sum()
        mes_alta = rng.choice(len(meses), size=TOTAL_CLIENTES, p=pesos)

        filas, perfiles = [], []
        for i in range(TOTAL_CLIENTES):
            id_cliente = f"CLI-{i + 1:03d}"
            m = meses[mes_alta[i]]
            dia = int(rng.integers(1, 28))
            fecha_alta = date(m.year, m.month, dia)

            es_agencia = rng.random() < 0.13
            if es_agencia:
                plan = "PLN-03"
                industria = "Agencia de marketing"
                nombre = f"Agencia {rng.choice(PALABRAS_A)} {rng.choice(['Digital', 'Media', 'Creativa', 'Lab'])}"
                while nombre in self.nombres_usados:
                    nombre = f"Agencia {rng.choice(PALABRAS_A)} {rng.choice(['Digital', 'Media', 'Creativa', 'Lab'])}"
                self.nombres_usados.add(nombre)
                tamano = rng.choice(["Pequeña", "Mediana"], p=[0.6, 0.4])
            else:
                plan = rng.choice(["PLN-01", "PLN-02"], p=[0.63, 0.37])
                industria = rng.choice(list(INDUSTRIAS.keys()))
                nombre = self.nombre_empresa(industria)
                tamano = rng.choice(["Micro", "Pequeña", "Mediana"], p=[0.45, 0.4, 0.15])

            compromiso = float(np.clip(rng.beta(2.5, 2.0) + (0.15 if es_agencia else 0), 0.05, 0.98))

            filas.append({
                "id_cliente": id_cliente,
                "nombre_empresa": nombre,
                "industria": industria,
                "tamano_empresa": tamano,
                "provincia": rng.choice(PROVINCIAS, p=PESO_PROVINCIAS),
                "canal_adquisicion": rng.choice(CANALES_ADQUISICION, p=[0.32, 0.14, 0.2, 0.22, 0.12]),
                "fecha_alta": fecha_alta,
                "id_plan_inicial": plan,
            })
            perfiles.append({"id_cliente": id_cliente, "plan": plan, "compromiso": compromiso,
                             "fecha_alta": fecha_alta, "es_agencia": es_agencia,
                             "industria": industria, "tamano": tamano, "nombre": nombre})

        self.clientes = pd.DataFrame(filas).sort_values("fecha_alta").reset_index(drop=True)
        self.perfiles = {p["id_cliente"]: p for p in perfiles}
        self._simular_ciclo_de_vida()

    # ------------------------------------------------------------------
    def _simular_ciclo_de_vida(self):
        """Decide mejoras de plan y cancelaciones mes a mes."""
        rng = self.rng
        riesgo_base = {"PLN-01": 0.09, "PLN-02": 0.015, "PLN-03": 0.008}
        for id_cliente, p in self.perfiles.items():
            historial = [(p["fecha_alta"], p["plan"])]
            plan_actual = p["plan"]
            fecha_baja = None
            meses_activo = 0
            for mes in meses_entre(date(p["fecha_alta"].year, p["fecha_alta"].month, 1), FECHA_FIN):
                if mes <= p["fecha_alta"]:
                    continue
                meses_activo += 1
                # Mejora de Starter a Growth en clientes que usan mucho la plataforma
                if plan_actual == "PLN-01" and meses_activo >= 2 and p["compromiso"] > 0.6 and rng.random() < 0.12:
                    plan_actual = "PLN-02"
                    historial.append((mes, plan_actual))
                # Cancelación, más probable al inicio y con poco uso
                riesgo = riesgo_base[plan_actual] * (2.0 - 1.8 * p["compromiso"])
                if meses_activo <= 3:
                    riesgo *= 1.3
                if rng.random() < riesgo:
                    fecha_baja = fin_de_mes(mes)
                    break
            p["historial_planes"] = historial
            p["fecha_baja"] = fecha_baja

        self.clientes["fecha_baja"] = self.clientes["id_cliente"].map(lambda c: self.perfiles[c]["fecha_baja"])
        self.clientes["estado"] = np.where(self.clientes["fecha_baja"].isna(), "Activo", "Cancelado")

    def plan_en_fecha(self, id_cliente, fecha):
        plan = None
        for inicio, pl in self.perfiles[id_cliente]["historial_planes"]:
            if inicio <= fecha:
                plan = pl
        return plan

    def fecha_fin_cliente(self, id_cliente):
        fb = self.perfiles[id_cliente]["fecha_baja"]
        return fb if fb is not None else FECHA_FIN

    # ------------------------------------------------------------------
    def generar_facturas(self):
        rng = self.rng
        filas = []
        n = 1
        for id_cliente, p in self.perfiles.items():
            fin = self.fecha_fin_cliente(id_cliente)
            # La prueba gratis de 14 días cubre el mes de alta; se cobra desde el mes siguiente
            primer_mes = date(p["fecha_alta"].year + (p["fecha_alta"].month // 12), p["fecha_alta"].month % 12 + 1, 1)
            meses = [m for m in meses_entre(primer_mes, FECHA_FIN) if m <= fin]
            for idx, mes in enumerate(meses):
                plan = self.plan_en_fecha(id_cliente, mes)
                precio = PRECIO_PLAN[plan]
                promo = p["fecha_alta"] < date(2026, 1, 1) and idx < 2
                descuento = round(precio * 0.5) if promo else 0
                subtotal = precio - descuento
                iva = round(subtotal * TASA_IVA)
                emision = mes
                vencimiento = mes + timedelta(days=9)

                ultimo_de_cancelado = p["fecha_baja"] is not None and idx == len(meses) - 1
                r = rng.random()
                if ultimo_de_cancelado and r < 0.4:
                    estado, fecha_pago = "Vencida", None
                elif mes >= date(2026, 10, 1) and r < 0.18:
                    estado, fecha_pago = "Pendiente", None
                elif r < 0.03:
                    estado, fecha_pago = "Vencida", None
                elif r < 0.25:
                    estado, fecha_pago = "Pagada", emision + timedelta(days=int(rng.integers(10, 26)))
                else:
                    estado, fecha_pago = "Pagada", emision + timedelta(days=int(rng.integers(0, 9)))

                metodo = rng.choice(["SINPE Móvil", "Transferencia", "Tarjeta"], p=[0.55, 0.25, 0.2]) if fecha_pago else None
                filas.append({
                    "id_factura": f"FAC-{n:05d}",
                    "id_cliente": id_cliente,
                    "id_plan": plan,
                    "periodo": mes.strftime("%Y-%m"),
                    "fecha_emision": emision,
                    "fecha_vencimiento": vencimiento,
                    "fecha_pago": fecha_pago,
                    "monto_plan_crc": precio,
                    "descuento_crc": descuento,
                    "subtotal_crc": subtotal,
                    "iva_crc": iva,
                    "total_crc": subtotal + iva,
                    "estado_pago": estado,
                    "metodo_pago": metodo,
                })
                n += 1
        self.facturas = pd.DataFrame(filas).sort_values(["fecha_emision", "id_cliente"]).reset_index(drop=True)
        self.facturas["id_factura"] = [f"FAC-{i + 1:05d}" for i in range(len(self.facturas))]

    # ------------------------------------------------------------------
    def generar_campanas_y_resultados(self):
        rng = self.rng
        campanas, resultados = [], []
        n_camp = 1

        presupuesto_diario = {"Micro": (4000, 8000), "Pequeña": (8000, 20000), "Mediana": (20000, 45000)}
        concurrentes = {"Micro": 1, "Pequeña": 2, "Mediana": 3}
        objetivos = {"CAN-01": ["Ventas", "Mensajes a WhatsApp", "Reconocimiento"],
                     "CAN-02": ["Ventas", "Mensajes a WhatsApp", "Reconocimiento"],
                     "CAN-03": ["Ventas", "Tráfico al sitio web"],
                     "CAN-04": ["Reconocimiento", "Ventas", "Tráfico al sitio web"],
                     "CAN-05": ["Tráfico al sitio web", "Ventas"]}
        temas = ["Lanzamiento", "Promo", "Temporada", "Remarketing", "Ofertas", "Marca", "Descuento"]

        for id_cliente, p in self.perfiles.items():
            inicio_cli = p["fecha_alta"] + timedelta(days=3)  # configuración inicial
            fin_cli = self.fecha_fin_cliente(id_cliente)
            if inicio_cli > fin_cli:
                continue

            # Marcas que administra: una para empresas, varias para agencias
            if p["es_agencia"]:
                marcas = []
                for _ in range(int(rng.integers(3, 7))):
                    ind = rng.choice(list(INDUSTRIAS.keys()))
                    marcas.append((self.nombre_empresa(ind), ind, rng.choice(["Micro", "Pequeña"], p=[0.5, 0.5])))
            else:
                marcas = [(p["nombre"], p["industria"], p["tamano"])]

            for marca, industria, tamano in marcas:
                ticket, afinidad = INDUSTRIAS[industria]
                # Canales preferidos de esta marca, ordenados por afinidad con algo de azar
                orden = sorted(afinidad, key=lambda c: -(afinidad[c] + rng.normal(0, 0.15)))
                lo, hi = presupuesto_diario[tamano]
                base_diaria = rng.uniform(lo, hi)
                for _slot in range(concurrentes[tamano]):
                    actual = inicio_cli + timedelta(days=int(rng.integers(0, 12)))
                    while actual <= fin_cli:
                        plan = self.plan_en_fecha(id_cliente, actual)
                        permitidos = orden[:min(CANALES_PERMITIDOS[plan], 4)]
                        # Con alertas, el cliente mueve poco a poco su presupuesto al canal que mejor le rinde
                        meses_uso = (actual - p["fecha_alta"]).days / 30.4
                        foco = 1 + (4 * min(meses_uso / 6, 1) if plan in ("PLN-02", "PLN-03") else 0.5)
                        pesos = np.array([afinidad[c] ** foco for c in permitidos])
                        canal = rng.choice(permitidos, p=pesos / pesos.sum())
                        beta_ok = (plan in ("PLN-02", "PLN-03") and actual >= INICIO_BETA_IA
                                   and AFINIDAD_IA[industria] > 0)
                        if beta_ok and rng.random() < 0.18:
                            canal = "CAN-05"
                        duracion = int(rng.integers(14, 61))
                        fin_camp = min(actual + timedelta(days=duracion - 1), fin_cli)
                        objetivo = rng.choice(objetivos[canal])
                        diario = base_diaria * rng.uniform(0.6, 1.4) / concurrentes[tamano] * 1.6
                        id_camp = f"CMP-{n_camp:04d}"
                        n_camp += 1
                        mes_txt = ["", "ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"][actual.month]
                        campanas.append({
                            "id_campana": id_camp,
                            "id_cliente": id_cliente,
                            "marca": marca,
                            "industria_marca": industria,
                            "nombre_campana": f"{rng.choice(temas)} {mes_txt} {actual.year} · {"IA" if canal == "CAN-05" else CANAL_INFO[canal][1].split()[0]}",
                            "canal": CANAL_INFO[canal][1],
                            "objetivo": objetivo,
                            "fecha_inicio": actual,
                            "fecha_fin": None if fin_camp >= FECHA_FIN and p["fecha_baja"] is None else fin_camp,
                            "presupuesto_diario_crc": int(round(diario, -2)),
                        })
                        if canal == "CAN-05":
                            diario *= 0.6  # en beta se prueba con menos presupuesto
                        self._resultados_diarios(resultados, id_camp, id_cliente, canal, industria, ticket,
                                                 {**afinidad, "CAN-05": AFINIDAD_IA[industria]},
                                                 actual, fin_camp, diario, objetivo)
                        actual = fin_camp + timedelta(days=int(rng.integers(1, 11)))

        self.campanas = pd.DataFrame(campanas)
        self.resultados = pd.DataFrame(resultados)
        self.resultados.insert(0, "id_resultado", [f"RES-{i + 1:06d}" for i in range(len(self.resultados))])

    def _resultados_diarios(self, filas, id_camp, id_cliente, canal, industria, ticket, afinidad,
                            inicio, fin, diario, objetivo):
        rng = self.rng
        _, _, _, _, cpm, ctr, cvr = CANAL_INFO[canal]
        p = self.perfiles[id_cliente]
        d = inicio
        while d <= fin:
            plan = self.plan_en_fecha(id_cliente, d)
            meses_uso = (d - p["fecha_alta"]).days / 30.4
            # Valor entregado: los clientes mejoran su conversión al usar el panel.
            # Con alertas (Growth y Agencia) el efecto es mayor.
            tope = 0.50 if plan in ("PLN-02", "PLN-03") else 0.10
            aprendizaje = 1 + tope * (0.5 + p["compromiso"]) * (1 - np.exp(-meses_uso / 3))
            est = ESTACIONALIDAD[d.month]
            if industria == "Educación y cursos" and d.month == 2:
                est *= 1.3
            finde = d.weekday() >= 5
            mult_finde = 1.15 if (finde and industria in ("Restaurantes y cafeterías", "Moda y accesorios")) else (0.9 if finde else 1.0)

            gasto = diario * est * mult_finde * rng.lognormal(0, 0.18)
            impresiones = int(gasto / (cpm * rng.lognormal(0, 0.12)) * 1000)
            ctr_obj = ctr * (0.6 if objetivo == "Reconocimiento" else 1.0)
            clics = int(rng.binomial(max(impresiones, 0), min(ctr_obj * rng.lognormal(0, 0.15), 0.5)))
            cvr_obj = cvr * afinidad[canal] * aprendizaje * (0.35 if objetivo == "Reconocimiento" else 1.0) * (0.9 + 0.1 * est)
            conversiones = int(rng.binomial(clics, min(cvr_obj, 0.6)))
            ingresos = int(round(sum(ticket * rng.lognormal(0, 0.35) for _ in range(conversiones)), -2))
            filas.append({
                "id_campana": id_camp,
                "fecha": d,
                "impresiones": impresiones,
                "clics": clics,
                "gasto_crc": int(round(gasto)),
                "conversiones": conversiones,
                "ingresos_atribuidos_crc": ingresos,
            })
            d += timedelta(days=1)

    # ------------------------------------------------------------------
    def generar_uso(self):
        rng = self.rng
        filas = []
        paginas = ["Resumen general", "Campañas", "Comparación de canales", "Alertas", "Reporte mensual"]
        roles_empresa = ["Dueño o dueña", "Encargado de marketing"]
        roles_agencia = ["Director de cuentas", "Analista de agencia", "Community manager"]
        for id_cliente, p in self.perfiles.items():
            fin = self.fecha_fin_cliente(id_cliente)
            semana = p["fecha_alta"]
            while semana <= fin:
                plan = self.plan_en_fecha(id_cliente, semana)
                tasa = 0.5 + 4.5 * p["compromiso"]
                if p["es_agencia"]:
                    tasa *= 1.6
                if (semana - p["fecha_alta"]).days < 14:
                    tasa *= 1.5  # entusiasmo inicial
                if p["fecha_baja"] is not None and (p["fecha_baja"] - semana).days < 42:
                    tasa *= 0.3  # el uso cae antes de cancelar
                if semana.month == 12 and semana.day >= 18 or (semana.month == 1 and semana.day <= 3):
                    tasa *= 0.5
                for _ in range(int(rng.poisson(tasa))):
                    dia = semana + timedelta(days=int(rng.integers(0, 7)))
                    if dia > fin or dia > FECHA_FIN:
                        continue
                    hora = int(rng.choice(range(6, 23), p=self._pesos_hora()))
                    momento = datetime(dia.year, dia.month, dia.day, hora, int(rng.integers(0, 60)))
                    pesos_pag = [0.35, 0.25, 0.18, 0.12 if plan != "PLN-01" else 0.0, 0.10]
                    pesos_pag = np.array(pesos_pag) / sum(pesos_pag)
                    pagina = rng.choice(paginas, p=pesos_pag)
                    filas.append({
                        "id_cliente": id_cliente,
                        "fecha_hora_inicio": momento,
                        "rol_usuario": rng.choice(roles_agencia if p["es_agencia"] else roles_empresa),
                        "dispositivo": rng.choice(["Computadora", "Celular", "Tableta"], p=[0.55, 0.4, 0.05]),
                        "pagina_principal": pagina,
                        "duracion_min": int(max(1, round(rng.lognormal(2.0, 0.55)))),
                        "alertas_revisadas": int(rng.poisson(1.2)) if plan != "PLN-01" else 0,
                        "reporte_descargado": "Sí" if (pagina == "Reporte mensual" or (dia.day <= 5 and rng.random() < 0.3)) else "No",
                    })
                semana += timedelta(days=7)
        self.uso = pd.DataFrame(filas).sort_values("fecha_hora_inicio").reset_index(drop=True)
        self.uso.insert(0, "id_sesion", [f"SES-{i + 1:05d}" for i in range(len(self.uso))])

    @staticmethod
    def _pesos_hora():
        w = np.array([1, 2, 4, 6, 6, 5, 4, 5, 5, 4, 3, 3, 4, 5, 5, 3, 1], dtype=float)
        return w / w.sum()

    # ------------------------------------------------------------------
    # Anomalías controladas (se corrigen después en Power Query)
    # ------------------------------------------------------------------
    def registrar(self, codigo, tipo, archivo, columna, cantidad, descripcion, correccion):
        self.anomalias.append({"codigo": codigo, "tipo": tipo, "archivo": archivo, "columna": columna,
                               "filas_afectadas": cantidad, "descripcion": descripcion,
                               "correccion_esperada_en_power_query": correccion})

    def sembrar_anomalias(self):
        rng = self.rng

        # A-01 Duplicados exactos en resultados de campañas
        idx = rng.choice(len(self.resultados), size=int(len(self.resultados) * 0.015), replace=False)
        dup = self.resultados.iloc[idx]
        self.resultados = pd.concat([self.resultados, dup]).sort_values(["id_campana", "fecha"]).reset_index(drop=True)
        self.registrar("A-01", "Duplicados", "resultados_campanas.csv", "fila completa", len(idx),
                       "La exportación de la API repitió algunas filas diarias.",
                       "Quitar filas duplicadas con base en id_resultado.")

        # A-02 Duplicados en facturas
        idx = rng.choice(len(self.facturas), size=6, replace=False)
        self.facturas = pd.concat([self.facturas, self.facturas.iloc[idx]]).sort_values("id_factura").reset_index(drop=True)
        self.registrar("A-02", "Duplicados", "facturas.csv", "fila completa", 6,
                       "El sistema de facturación exportó dos veces algunas facturas.",
                       "Quitar duplicados con base en id_factura.")

        # A-03 Duplicados en sesiones de uso
        idx = rng.choice(len(self.uso), size=25, replace=False)
        self.uso = pd.concat([self.uso, self.uso.iloc[idx]]).sort_values("id_sesion").reset_index(drop=True)
        self.registrar("A-03", "Duplicados", "uso_plataforma.csv", "fila completa", 25,
                       "El registro de actividad guardó dos veces algunas sesiones.",
                       "Quitar duplicados con base en id_sesion.")

        # A-04 Faltantes en ingresos cuando no hubo ventas
        sin_venta = self.resultados.index[self.resultados["conversiones"] == 0]
        idx = rng.choice(sin_venta, size=min(len(sin_venta), int(len(self.resultados) * 0.02)), replace=False)
        self.resultados["ingresos_atribuidos_crc"] = self.resultados["ingresos_atribuidos_crc"].astype("Int64")
        self.resultados.loc[idx, "ingresos_atribuidos_crc"] = pd.NA
        self.registrar("A-04", "Faltantes", "resultados_campanas.csv", "ingresos_atribuidos_crc", len(idx),
                       "La plataforma deja el campo vacío cuando el día no tuvo conversiones.",
                       "Reemplazar nulos por 0, ya que conversiones es 0 en esas filas.")

        # A-05 Faltantes en datos de clientes
        idx = rng.choice(len(self.clientes), size=4, replace=False)
        self.clientes.loc[idx[:2], "provincia"] = None
        self.clientes.loc[idx[2:], "canal_adquisicion"] = None
        self.registrar("A-05", "Faltantes", "clientes.csv", "provincia, canal_adquisicion", 4,
                       "Clientes registrados sin provincia o sin canal de adquisición.",
                       "Reemplazar nulos por 'Sin dato'.")

        # A-06 Categorías inconsistentes en el nombre del canal
        variantes = {"Facebook Ads": ["facebook ads", "Facebook", "FB Ads", " Facebook Ads "],
                     "Instagram Ads": ["instagram", "IG Ads", "Insta Ads", "INSTAGRAM ADS"],
                     "Google Ads": ["google ads", "Google", "GOOGLE ADS ", "Google Adwords"],
                     "TikTok Ads": ["tiktok", "Tik Tok Ads", "TIKTOK ADS", "TikTok"],
                     "Anuncios en IA (beta)": ["anuncios en ia", "IA beta", "Anuncios IA (Beta)", "ANUNCIOS EN IA"]}
        idx = rng.choice(len(self.campanas), size=int(len(self.campanas) * 0.18), replace=False)
        for i in idx:
            original = self.campanas.at[i, "canal"]
            self.campanas.at[i, "canal"] = rng.choice(variantes[original])
        self.registrar("A-06", "Categorías inconsistentes", "campanas.xlsx", "canal", len(idx),
                       "El nombre del canal se escribió a mano de varias formas.",
                       "Recortar espacios, homologar con una tabla de equivalencias y unir con canales.csv para obtener id_canal.")

        # A-07 Categorías inconsistentes en provincia y método de pago
        variantes_prov = {"San José": ["san jose", "SAN JOSE", "S.José", "San Jose"],
                          "Heredia": ["heredia", "HEREDIA "], "Alajuela": ["alajuela", "Alajuela "],
                          "Cartago": ["cartago", "CARTAGO"], "Puntarenas": ["puntarenas"],
                          "Guanacaste": ["guanacaste"], "Limón": ["Limon", "limón"]}
        cand = self.clientes.index[self.clientes["provincia"].notna()]
        idx = rng.choice(cand, size=7, replace=False)
        for i in idx:
            self.clientes.at[i, "provincia"] = rng.choice(variantes_prov[self.clientes.at[i, "provincia"]])
        cand = self.facturas.index[self.facturas["metodo_pago"].notna()]
        idx2 = rng.choice(cand, size=int(len(cand) * 0.12), replace=False)
        var_pago = {"SINPE Móvil": ["Sinpe movil", "SINPE", "sinpe móvil"], "Transferencia": ["transferencia", "Transf."],
                    "Tarjeta": ["tarjeta", "TARJETA"]}
        for i in idx2:
            self.facturas.at[i, "metodo_pago"] = rng.choice(var_pago[self.facturas.at[i, "metodo_pago"]])
        self.registrar("A-07", "Categorías inconsistentes", "clientes.csv y facturas.csv", "provincia, metodo_pago",
                       len(idx) + len(idx2), "Mayúsculas, tildes, abreviaturas y espacios distintos.",
                       "Recortar, poner en formato de título y reemplazar valores con una tabla de equivalencias.")

        # A-08 Valores fuera de rango, gasto negativo
        idx = rng.choice(len(self.resultados), size=12, replace=False)
        self.resultados.loc[idx, "gasto_crc"] = -self.resultados.loc[idx, "gasto_crc"]
        self.registrar("A-08", "Valores fuera de rango", "resultados_campanas.csv", "gasto_crc", 12,
                       "Gasto registrado con signo negativo por un error de la exportación.",
                       "Convertir a valor absoluto.")

        # A-09 Clics e impresiones invertidos
        cand = self.resultados.index[(self.resultados["clics"] > 0) & (self.resultados["impresiones"] > self.resultados["clics"])]
        idx = rng.choice(cand, size=10, replace=False)
        tmp = self.resultados.loc[idx, "impresiones"].copy()
        self.resultados.loc[idx, "impresiones"] = self.resultados.loc[idx, "clics"]
        self.resultados.loc[idx, "clics"] = tmp
        self.registrar("A-09", "Valores fuera de rango", "resultados_campanas.csv", "impresiones, clics", 10,
                       "Filas con más clics que impresiones porque las columnas venían invertidas.",
                       "Cuando clics > impresiones, intercambiar ambos valores.")

        # A-10 Integridad referencial, resultados de campañas que no existen
        muestra = self.resultados.sample(n=15, random_state=self.semilla).copy()
        muestra["id_campana"] = [f"CMP-{9000 + i}" for i in range(15)]
        muestra["id_resultado"] = [f"RES-9{i:05d}" for i in range(15)]
        self.resultados = pd.concat([self.resultados, muestra]).reset_index(drop=True)
        self.registrar("A-10", "Integridad referencial", "resultados_campanas.csv", "id_campana", 15,
                       "Resultados de campañas de prueba que no existen en campanas.xlsx.",
                       "Eliminar con una combinación interna (inner join) contra campanas.")

        # A-11 Claves con formato distinto
        idx = rng.choice(len(self.uso), size=40, replace=False)
        self.uso.loc[idx, "id_cliente"] = self.uso.loc[idx, "id_cliente"].str.lower()
        self.registrar("A-11", "Formato de clave inconsistente", "uso_plataforma.csv", "id_cliente", 40,
                       "Algunos códigos de cliente se guardaron en minúscula (cli-012).",
                       "Pasar id_cliente a mayúsculas antes de relacionar.")

    # ------------------------------------------------------------------
    def guardar(self, carpeta):
        os.makedirs(carpeta, exist_ok=True)
        enc = "utf-8-sig"
        pd.DataFrame(PLANES, columns=["id_plan", "nombre_plan", "precio_mensual_crc", "max_marcas",
                                      "max_canales", "incluye_alertas"]).to_csv(os.path.join(carpeta, "planes.csv"), index=False, encoding=enc)
        pd.DataFrame([c[:4] for c in CANALES], columns=["id_canal", "nombre_canal", "plataforma", "tipo_canal"]).to_csv(
            os.path.join(carpeta, "canales.csv"), index=False, encoding=enc)
        self.clientes.drop(columns=["estado"]).to_csv(os.path.join(carpeta, "clientes.csv"), index=False, encoding=enc)
        self.facturas.to_csv(os.path.join(carpeta, "facturas.csv"), index=False, encoding=enc)
        self.campanas.to_excel(os.path.join(carpeta, "campanas.xlsx"), index=False, sheet_name="campanas")
        self.resultados.to_csv(os.path.join(carpeta, "resultados_campanas.csv"), index=False, encoding=enc)
        self.uso.to_csv(os.path.join(carpeta, "uso_plataforma.csv"), index=False, encoding=enc)

        doc = os.path.join(os.path.dirname(os.path.abspath(carpeta)), "documentacion")
        os.makedirs(doc, exist_ok=True)
        pd.DataFrame(self.anomalias).to_csv(os.path.join(doc, "registro_anomalias.csv"), index=False, encoding=enc)


def main():
    parser = argparse.ArgumentParser(description="Genera los datos simulados de MarketMind BI.")
    parser.add_argument("--semilla", type=int, default=SEMILLA_POR_DEFECTO)
    parser.add_argument("--salida", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos_brutos"))
    args = parser.parse_args()

    g = Generador(args.semilla)
    g.generar_clientes()
    g.generar_facturas()
    g.generar_campanas_y_resultados()
    g.generar_uso()
    g.sembrar_anomalias()
    g.guardar(args.salida)

    print("DATOS SIMULADOS · MarketMind BI")
    print(f"Semilla {args.semilla}")
    print(f"clientes.csv              {len(g.clientes):>7} filas")
    print(f"facturas.csv              {len(g.facturas):>7} filas")
    print(f"campanas.xlsx             {len(g.campanas):>7} filas")
    print(f"resultados_campanas.csv   {len(g.resultados):>7} filas")
    print(f"uso_plataforma.csv        {len(g.uso):>7} filas")
    print(f"Archivos guardados en {args.salida}")


if __name__ == "__main__":
    main()
