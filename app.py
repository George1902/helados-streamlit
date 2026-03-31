import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Negocio Helados", layout="wide")

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
if "ventas" not in st.session_state:
    st.session_state.ventas = []
if "gastos" not in st.session_state:
    st.session_state.gastos = []
if "stock" not in st.session_state:
    st.session_state.stock = {k: 50 for k in productos}
if "caja_abierta" not in st.session_state:
    st.session_state.caja_abierta = False

# -------------------------
# CONFIGURAR PRODUCTOS
# -------------------------
st.sidebar.title("⚙️ Configuración")
for p in productos:
    precio = st.sidebar.number_input(f"Precio {p}", value=productos[p]["precio"], key=f"precio_{p}")
    costo = st.sidebar.number_input(f"Costo {p}", value=productos[p]["costo"], key=f"costo_{p}")
    productos[p]["precio"] = precio
    productos[p]["costo"] = costo

# -------------------------
# FUNCIONES
# -------------------------
def agregar_venta(nombre):
    if not st.session_state.caja_abierta:
        return
    if st.session_state.stock[nombre] <= 0:
        return

    data = productos[nombre]

    venta = {
        "producto": nombre,
        "total": data["precio"],
        "costo": data["costo"],
        "ganancia": data["precio"] - data["costo"],
        "fecha": datetime.now(),
    }

    st.session_state.ventas.append(venta)
    st.session_state.stock[nombre] -= 1

# -------------------------
# UI
# -------------------------
st.markdown("<h1 style='text-align:center;'>🍦 NEGOCIO HELADOS PRO</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
col1.button("🟢 Abrir Caja", on_click=lambda: st.session_state.update({"caja_abierta": True}))
col2.button("🔴 Cerrar Caja", on_click=lambda: st.session_state.update({"caja_abierta": False}))

# -------------------------
# DATA
# -------------------------
df = pd.DataFrame(st.session_state.ventas)
dg = pd.DataFrame(st.session_state.gastos)

if not df.empty:
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["dia"] = df["fecha"].dt.date
    df["hora"] = df["fecha"].dt.hour
    df["semana"] = df["fecha"].dt.isocalendar().week
    df["mes"] = df["fecha"].dt.month

# -------------------------
# KPIs CORREGIDOS
# -------------------------
ventas_total = df["total"].sum() if not df.empty else 0
costo_total = df["costo"].sum() if not df.empty else 0
gastos_total = dg["monto"].sum() if not dg.empty else 0

ganancia_neta = ventas_total - costo_total - gastos_total

k1, k2, k3, k4 = st.columns(4)
k1.metric("Ventas", f"${ventas_total}")
k2.metric("Costos", f"${costo_total}")
k3.metric("Gastos", f"${gastos_total}")
k4.metric("Ganancia Neta", f"${ganancia_neta}")

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
# INSIGHTS
# -------------------------
if not df.empty:
    st.subheader("🧠 Insights")

    top_producto = df["producto"].value_counts().idxmax()
    mejor_hora = df.groupby("hora")["total"].sum().idxmax()
    rentable = df.groupby("producto")["ganancia"].sum().idxmax()

    c1, c2, c3 = st.columns(3)
    c1.info(f"🏆 Más vendido: {top_producto}")
    c2.info(f"⏰ Mejor hora: {mejor_hora}:00")
    c3.info(f"💰 Más rentable: {rentable}")

# -------------------------
# GRÁFICOS
# -------------------------
if not df.empty:
    st.subheader("📊 Análisis")

    st.line_chart(df.groupby("dia")["total"].sum())
    st.bar_chart(df.groupby("hora")["total"].sum())
    st.bar_chart(df.groupby("producto")["ganancia"].sum())

# -------------------------
# HISTORIAL
# -------------------------
st.subheader("📋 Ventas")
st.dataframe(df)

# -------------------------
# RESET
# -------------------------
if st.button("♻️ Reset"):
    st.session_state.clear()
    st.success("Reiniciado")
