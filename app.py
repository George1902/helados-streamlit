import streamlit as st
import pandas as pd
from datetime import datetime, date

st.set_page_config(page_title="Helados GERENTE PRO", layout="wide")

# -------------------------
# CONFIG INICIAL
# -------------------------
if "productos" not in st.session_state:
    st.session_state.productos = {
        "Cono": {"precio": 1500, "costo": 700},
        "Paleta": {"precio": 1000, "costo": 400},
        "Vaso": {"precio": 2000, "costo": 900},
    }

productos = st.session_state.productos

# -------------------------
# STATE
# -------------------------
def init_state(key, default):
    if key not in st.session_state:
        st.session_state[key] = default

init_state("ventas", [])
init_state("gastos", [])
init_state("stock", {k: 50 for k in productos})
init_state("caja_abierta", False)
init_state("cierres", [])
init_state("fecha_caja", None)

# -------------------------
# SIDEBAR CONFIG
# -------------------------
st.sidebar.title("⚙️ Configuración")
for p in productos:
    productos[p]["precio"] = st.sidebar.number_input(f"Precio {p}", value=productos[p]["precio"], key=f"precio_{p}")
    productos[p]["costo"] = st.sidebar.number_input(f"Costo {p}", value=productos[p]["costo"], key=f"costo_{p}")
    if f"stock_init_{p}" not in st.session_state:
        st.session_state[f"stock_init_{p}"] = st.session_state.stock[p]

    nuevo_stock = st.sidebar.number_input(f"Stock inicial {p}", value=st.session_state[f"stock_init_{p}"], key=f"stock_{p}")

    # solo actualizar si la caja está cerrada (evita reset durante ventas)
    if not st.session_state.caja_abierta:
        st.session_state.stock[p] = nuevo_stock
        st.session_state[f"stock_init_{p}"] = nuevo_stock

# -------------------------
# FUNCIONES CAJA
# -------------------------
def abrir_caja():
    st.session_state.caja_abierta = True
    st.session_state.fecha_caja = date.today()
    st.success("🟢 Caja abierta")


def cerrar_caja():
    df = pd.DataFrame(st.session_state.ventas)
    dg = pd.DataFrame(st.session_state.gastos)

    ventas = df["total"].sum() if not df.empty else 0
    costos = df["costo"].sum() if not df.empty else 0
    gastos = dg["monto"].sum() if not dg.empty else 0

    cierre = {
        "fecha": st.session_state.fecha_caja,
        "ventas": ventas,
        "costos": costos,
        "gastos": gastos,
        "ganancia": ventas - costos - gastos,
        "tickets": len(df)
    }

    st.session_state.cierres.append(cierre)

    st.session_state.ventas = []
    st.session_state.gastos = []
    st.session_state.caja_abierta = False
    st.session_state.fecha_caja = None

    st.success("🔴 Caja cerrada y guardada")

# -------------------------
# FUNCIONES OPERATIVAS
# -------------------------
def agregar_venta(nombre):
    if not st.session_state.caja_abierta:
        st.warning("Debes abrir caja")
        return

    if st.session_state.stock[nombre] <= 0:
        st.error("Sin stock")
        return

    data = productos[nombre]

    st.session_state.ventas.append({
        "producto": nombre,
        "total": data["precio"],
        "costo": data["costo"],
        "ganancia": data["precio"] - data["costo"],
        "fecha": datetime.now(),
    })

    st.session_state.stock[nombre] -= 1


def agregar_gasto():
    if not st.session_state.caja_abierta:
        st.warning("Debes abrir caja")
        return

    desc = st.session_state.desc_gasto
    monto = st.session_state.monto_gasto

    if not desc or monto <= 0:
        st.warning("Completa los datos")
        return

    st.session_state.gastos.append({
        "descripcion": desc,
        "monto": monto,
        "fecha": datetime.now()
    })

    st.session_state.desc_gasto = ""
    st.session_state.monto_gasto = 0

# -------------------------
# UI
# -------------------------
st.markdown("<h1 style='text-align:center;'>🍦 NEGOCIO HELADOS PRO</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
col1.button("🟢 Abrir Caja", on_click=abrir_caja)
col2.button("🔴 Cerrar Caja", on_click=cerrar_caja)

# -------------------------
# DATAFRAME
# -------------------------
df = pd.DataFrame(st.session_state.ventas)
dg = pd.DataFrame(st.session_state.gastos)
dc = pd.DataFrame(st.session_state.cierres)

if not df.empty:
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["dia"] = df["fecha"].dt.date
    df["hora"] = df["fecha"].dt.hour
    df["semana"] = df["fecha"].dt.isocalendar().week
    df["mes"] = df["fecha"].dt.month

# -------------------------
# KPIs
# -------------------------
ventas_total = df["total"].sum() if not df.empty else 0
costos_total = df["costo"].sum() if not df.empty else 0
gastos_total = dg["monto"].sum() if not dg.empty else 0

ganancia = ventas_total - costos_total - gastos_total

k1, k2, k3, k4 = st.columns(4)
k1.metric("Ventas", f"${ventas_total}")
k2.metric("Costos", f"${costos_total}")
k3.metric("Gastos", f"${gastos_total}")
k4.metric("Ganancia Neta", f"${ganancia}")

# -------------------------
# COMPARACIÓN VS AYER
# -------------------------
if not dc.empty:
    dc_sorted = dc.sort_values("fecha")
    if len(dc_sorted) >= 2:
        hoy = dc_sorted.iloc[-1]
        ayer = dc_sorted.iloc[-2]
        diff = hoy["ganancia"] - ayer["ganancia"]
        st.info(f"📊 Comparación: {diff:+.0f} vs día anterior")

# -------------------------
# VENTAS
# -------------------------
st.subheader("💸 Venta rápida")
cols = st.columns(len(productos))
for i, nombre in enumerate(productos):
    with cols[i]:
        st.button(
            f"{nombre}\n${productos[nombre]['precio']}\nStock: {st.session_state.stock[nombre]}",
            on_click=agregar_venta,
            args=(nombre,)
        )

# -------------------------
# GASTOS
# -------------------------
st.subheader("💸 Registrar gasto")
colg1, colg2 = st.columns(2)
colg1.text_input("Descripción", key="desc_gasto")
colg2.number_input("Monto", min_value=0, key="monto_gasto")
st.button("Agregar gasto", on_click=agregar_gasto)

# -------------------------
# GRÁFICOS
# -------------------------
if not df.empty:
    st.subheader("📊 Análisis")
    st.markdown("**Ventas por día**")
    ventas_dia = df.groupby("dia")["total"].sum().reset_index()
    ventas_dia = ventas_dia.set_index("dia")
    st.line_chart(ventas_dia)

    st.markdown("**Ventas por hora (flujo del día)**")
    st.bar_chart(df.groupby("hora")["total"].sum())

    st.markdown("**Ganancia por producto**")
    st.bar_chart(df.groupby("producto")["ganancia"].sum())

# -------------------------
# EXPORTAR
# -------------------------
if not df.empty:
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📤 Exportar ventas", csv, "ventas.csv")

if not dc.empty:
    csv_cierres = dc.to_csv(index=False).encode("utf-8")
    st.download_button("📤 Exportar cierres de caja", csv_cierres, "cierres.csv")

# -------------------------
# HISTORIAL
# -------------------------
st.subheader("📋 Ventas")
st.dataframe(df)

st.subheader("📋 Gastos")
st.dataframe(dg)

st.subheader("📦 Cierres de caja")
st.dataframe(dc)

# -------------------------
# RESET
# -------------------------
if st.button("♻️ Reset total"):
    st.session_state.clear()
    st.success("Sistema reiniciado")
