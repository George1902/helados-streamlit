# 🍦 NEGOCIO HELADOS PRO

Sistema de gestión de ventas, inventario y caja desarrollado en **Streamlit**, pensado para negocios reales pequeños (heladerías, kioscos, ventas rápidas).

---

## 🚀 Características principales

### 💰 Control de Caja

* Apertura y cierre de caja
* Registro automático de:

  * Ventas
  * Costos
  * Gastos
  * Ganancia neta
* Historial de cierres

---

### 🧾 Ventas en Tiempo Real

* Botones de **venta rápida** por producto
* Descuento automático de stock
* Cálculo inmediato de:

  * Ingresos
  * Costos
  * Ganancia

---

### 📦 Control de Inventario

* Stock configurable por producto
* Descuento automático al vender
* Persistencia de stock entre aperturas de caja

---

### 📊 Inteligencia de Negocio

* 📅 Ventas por semana (histórico acumulado)
* 🏆 Ranking de productos más vendidos
* 📈 Datos basados en historial real (no se borran al cerrar caja)

---

### 💸 Gestión de Gastos

* Registro de gastos diarios
* Impacto directo en la ganancia
* Limpieza automática al cerrar caja

---

### 📤 Exportación de Datos

* Exportar ventas en CSV
* Exportar cierres de caja

---

## 🧠 Cómo funciona internamente

El sistema separa la información en dos niveles:

### 🔹 Operación diaria

* `ventas`
* `gastos`

👉 Se limpian al cerrar caja

### 🔹 Historial acumulado

* `ventas_historicas`
* `cierres`

👉 Nunca se borran
👉 Permiten análisis real del negocio

---

## ▶️ Cómo ejecutar

1. Instalar dependencias:

```bash
pip install streamlit pandas
```

2. Ejecutar la app:

```bash
streamlit run app.py
```

---

## ⚙️ Configuración

Desde el panel lateral puedes:

* Modificar precios
* Modificar costos
* Definir stock inicial por producto

---

## 📌 Flujo de uso recomendado

1. Configurar precios, costos y stock
2. Abrir caja
3. Registrar ventas y gastos
4. Revisar KPIs
5. Cerrar caja
6. Analizar resultados semanales

---

## 🧱 Estructura del sistema

* `productos` → catálogo
* `stock` → inventario actual
* `ventas` → ventas del día
* `ventas_historicas` → histórico completo
* `gastos` → gastos del día
* `cierres` → resumen por día

---

## ⚠️ Consideraciones

* La información se guarda en memoria (session_state)
* Si reinicias la app → se pierden datos

👉 Para producción real:

* usar base de datos (SQLite, Firebase, etc.)

---

## 🚀 Próximas mejoras sugeridas

* Predicción de stock
* Alertas inteligentes automáticas
* Dashboard avanzado
* Base de datos persistente

---

## 🧑‍💼 Enfoque

Este sistema está diseñado con mentalidad de:

✔ Control total del negocio
✔ Simplicidad operativa
✔ Escalabilidad futura

---

## 🏁 Resultado

Una app ligera pero potente que permite:

* Controlar ventas
* Gestionar inventario
* Analizar el negocio
* Tomar decisiones

---

🔥 Proyecto listo para evolucionar a nivel profesional.
