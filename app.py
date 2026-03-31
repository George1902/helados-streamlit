import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Helados NEGOCIO PRO", layout="wide")

# -------------------------
# CONFIG
# -------------------------
productos = {
    "Cono": {"precio": 1500, "costo": 700},
    "Paleta": {"precio": 1000, "costo": 400},
    "Vaso": {"precio": 2000, "costo": 900},
}

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

if "historial_cierres" not in st.session_state:
    st.session_state.historial_cierres = []

# -------------------------
# FUNCIONES
# -------------------------
def abrir_caja():
    st.session_state.caja_abierta = True
    st.success("Caja abierta")


def cerrar_caja():
    df = pd.DataFrame(st.session_state.ventas)
    dg = pd.DataFrame(st.session_state.gastos)

    total = df["total"].sum() if not df.empty else 0
    gastos = dg["monto"].sum() if not dg.empty else 0
    ganancia = total - gastos

    cierre = {
        "fecha": datetime.now(),
        "ventas": total,
        "gastos": gastos,
        "ganancia": ganancia
    }

    st.session_state.historial_cierres.append(cierre)
    st.session_state.ventas = []
    st.session_state.gastos = []
    st.session_state.caja_abierta = False

    st.success(f"Caja cerrada | Ganancia: ${ganancia}")


def agregar_venta(nombre):
    if not st.session_state.caja_abierta:
        st.warning("Debes abrir caja")
        return

    if st.session_state.stock[nombre] <= 0:
        st.error("Sin stock")
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


def agregar_gasto(desc, monto):
    if not st.session_state.caja_abierta:
        st.warning("Debes abrir caja")
        return

    gasto = {
        "descripcion": desc,
        "monto": monto,
        "fecha": datetime.now()
    }

    st.session_state.gastos.append(gasto)

# -------------------------
# UI
# -------------------------
st.title("🍦 NEGOCIO HELADOS PRO")

col1, col2 = st.columns(2)

col1.button("🟢 Abrir Caja", on_click=abrir_caja)
col2.button("🔴 Cerrar Caja", on_click=cerrar_caja)

# -------------------------
# KPIs
# -------------------------
df = pd.DataFrame(st.session_state.ventas)
dg = pd.DataFrame(st.session_state.gastos)

ventas_total = df["total"].sum() if not df.empty else 0
gastos_total = dg["monto"].sum() if not dg.empty else 0
ganancia = ventas_total - gastos_total

k1, k2, k3 = st.columns(3)

k1.metric("Ventas", f"${ventas_total}")
k2.metric("Gastos", f"${gastos_total}")
k3.metric("Ganancia", f"${ganancia}")

# -------------------------
# VENTAS
# -------------------------
st.subheader("💸 Ventas")
for nombre in productos:
    st.button(f"{nombre} (${productos[nombre]['precio']}) | Stock: {st.session_state.stock[nombre]}", on_click=agregar_venta, args=(nombre,))

# -------------------------
# GASTOS
# -------------------------
st.subheader("💸 Registrar gasto")
colg1, colg2 = st.columns(2)

desc = colg1.text_input("Descripción")
monto = colg2.number_input("Monto", min_value=0)

if st.button("Agregar gasto"):
    agregar_gasto(desc, monto)

# -------------------------
# GRAFICOS
# -------------------------
if not df.empty:
    df["dia"] = df["fecha"].dt.date
    st.line_chart(df.groupby("dia")["total"].sum())

# -------------------------
# HISTORIAL
# -------------------------
st.subheader("📋 Ventas")
st.dataframe(df)

st.subheader("📋 Gastos")
st.dataframe(dg)

st.subheader("📦 Cierres de caja")
st.dataframe(pd.DataFrame(st.session_state.historial_cierres))

# -------------------------
# EXPORTAR
# -------------------------
if not df.empty:
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📤 Exportar ventas", csv, "ventas.csv")

# -------------------------
# RESET
# -------------------------
if st.button("♻️ Reset total"):
    st.session_state.clear()
    st.success("Sistema reiniciado")
