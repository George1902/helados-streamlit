import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Sistema Helados PRO", layout="centered")

# -------------------------
# CONFIGURACIÓN
# -------------------------
productos = {
    "Cono": {"precio": 1500, "costo": 700},
    "Paleta": {"precio": 1000, "costo": 400},
    "Vaso": {"precio": 2000, "costo": 900},
}

COSTO_FIJO = 50000  # puedes cambiarlo

# -------------------------
# ESTADO INICIAL
# -------------------------
if "ventas" not in st.session_state:
    st.session_state.ventas = []

if "stock" not in st.session_state:
    st.session_state.stock = {k: 50 for k in productos}

if "caja_abierta" not in st.session_state:
    st.session_state.caja_abierta = False

# -------------------------
# FUNCIONES
# -------------------------
def abrir_caja():
    st.session_state.caja_abierta = True
    st.success("Caja abierta")

def cerrar_caja(total, ganancia):
    st.session_state.caja_abierta = False
    st.warning(f"Cierre de caja\nVentas: ${total}\nGanancia: ${ganancia}")

def agregar_venta(nombre):
    if not st.session_state.caja_abierta:
        st.error("Debes abrir caja primero")
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

# -------------------------
# UI
# -------------------------
st.title("🍦 Sistema Helados PRO MAX")

# Caja
if not st.session_state.caja_abierta:
    st.button("🟢 Abrir caja", on_click=abrir_caja)
else:
    st.button(
        "🔴 Cerrar caja",
        on_click=cerrar_caja,
        args=(0, 0)  # luego se actualiza abajo
    )

# -------------------------
# DATOS
# -------------------------
df = pd.DataFrame(st.session_state.ventas)

if not df.empty:
    df["dia"] = df["fecha"].dt.date
    df["mes"] = df["fecha"].dt.month

    hoy = datetime.now().date()
    mes_actual = datetime.now().month

    ventas_hoy = df[df["dia"] == hoy]
    ventas_mes = df[df["mes"] == mes_actual]

    total_hoy = ventas_hoy["total"].sum()
    ganancia_hoy = ventas_hoy["ganancia"].sum()

    total_mes = ventas_mes["total"].sum()
    ganancia_mes = ventas_mes["ganancia"].sum()

else:
    total_hoy = ganancia_hoy = total_mes = ganancia_mes = 0

# -------------------------
# KPIs
# -------------------------
st.subheader("📊 Hoy")
col1, col2 = st.columns(2)
col1.metric("Ventas", f"${total_hoy}")
col2.metric("Ganancia", f"${ganancia_hoy}")

st.subheader("📅 Mes")
col3, col4 = st.columns(2)
col3.metric("Ventas", f"${total_mes}")
col4.metric("Ganancia", f"${ganancia_mes}")

# -------------------------
# PUNTO DE EQUILIBRIO
# -------------------------
if not df.empty:
    margen_promedio = df["ganancia"].mean()
else:
    margen_promedio = 0

punto_equilibrio = int(COSTO_FIJO / margen_promedio) if margen_promedio else 0

st.subheader("📉 Punto de equilibrio")
st.info(f"Debes vender aprox {punto_equilibrio} productos")

# -------------------------
# VENTAS
# -------------------------
st.subheader("💸 Ventas rápidas")

for nombre in productos:
    st.button(
        f"{nombre} (${productos[nombre]['precio']}) | Stock: {st.session_state.stock[nombre]}",
        on_click=agregar_venta,
        args=(nombre,)
    )

# -------------------------
# STOCK BAJO
# -------------------------
st.subheader("⚠️ Stock bajo")
for p, s in st.session_state.stock.items():
    if s <= 5:
        st.warning(f"{p}: {s}")

# -------------------------
# COMPRA SUGERIDA
# -------------------------
st.subheader("📦 Compra sugerida")
for p, s in st.session_state.stock.items():
    if s < 10:
        st.write(f"{p}: comprar {20 - s}")

# -------------------------
# GRÁFICO
# -------------------------
if not df.empty:
    st.subheader("📈 Ventas por día")
    ventas_dia = df.groupby("dia")["total"].sum()
    st.line_chart(ventas_dia)

# -------------------------
# RANKING
# -------------------------
if not df.empty:
    st.subheader("🏆 Ranking")
    ranking = df["producto"].value_counts()
    st.write(ranking)

# -------------------------
# EXPORTAR
# -------------------------
if not df.empty:
    st.subheader("📤 Exportar")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Descargar CSV",
        csv,
        "ventas_helados.csv",
        "text/csv"
    )

# -------------------------
# HISTORIAL
# -------------------------
st.subheader("📋 Historial")
st.dataframe(df)

# -------------------------
# RESET
# -------------------------
if st.button("♻️ Reiniciar sistema"):
    st.session_state.ventas = []
    st.session_state.stock = {k: 50 for k in productos}
    st.success("Sistema reiniciado")
