import streamlit as st
import numpy as np
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

st.set_page_config(page_title="Gestión de Rutas y Liquidación", page_icon="📊", layout="centered")

st.title("📊 Sistema de Gestión - Distribución de Rutas")
st.markdown("---")

pestana_ventas, pestana_liquidacion = st.tabs(["Control y Proyección de Ventas", "Liquidación Diaria"])

# ==========================================
# PESTAÑA 1: CONTROL Y PROYECCIÓN DE VENTAS
# ==========================================
with pestana_ventas:
    st.subheader("Control y Proyección de Ventas por Ruta")
    
    METAS_POR_RUTA = {
        "ruta 7201": 980000.0,
        "ruta 7202": 1000000.0,
        "ruta 7203": 1120000.0,
        "ruta 7204": 650000.0,
        "ruta 7205": 980000.0,
        "ruta 7206": 1450000.0,
        "ruta 7207": 550000.0,
        "ruta 7208": 1060000.0,
        "ruta 7209": 1080000.0,
        "ruta 7210": 1100000.0,
        "ruta 7211": 880000.0,
        "ruta 7212": 650000.0,
        "ruta 7213": 1050000.0
    }

    st.markdown("### Selección de Ruta")
    ruta_seleccionada = st.selectbox("Elige la ruta a gestionar:", list(METAS_POR_RUTA.keys()), key="select_ruta_ventas")
    meta_asignada = METAS_POR_RUTA[ruta_seleccionada]
    
    st.info(f"Estás trabajando en la **{ruta_seleccionada.upper()}** | Meta mensual fija: **L. {meta_asignada:,.2f}**")
    st.markdown("---")

    st.subheader(f"Parámetros y Datos del Día - {ruta_seleccionada.upper()}")
    col1, col2 = st.columns(2)

    with col1:
        meta = st.number_input("Meta del mes de esta ruta", value=meta_asignada, format="%.2f", step=10000.0, key=f"meta_{ruta_seleccionada}")
        venta_hoy = st.number_input("Venta total de hoy", value=0.0, format="%.2f", step=1000.0, key=f"hoy_{ruta_seleccionada}")
    
    with col2:
        venta_mes = st.number_input("Acumulado previo del mes", value=0.0, format="%.2f", step=1000.0, key=f"mes_{ruta_seleccionada}")

    if st.button("Calcular Resultados de la Ruta", type="primary", use_container_width=True):
        zona_horaria = ZoneInfo('America/Tegucigalpa')
        hoy = datetime.now(zona_horaria).date()
        
        inicio_mes = datetime(hoy.year, hoy.month, 1).date()
        fin_mes = datetime(hoy.year + 1, 1, 1).date() if hoy.month == 12 else datetime(hoy.year, hoy.month + 1, 1).date()

        total_dias_mes = np.busday_count(inicio_mes, fin_mes, weekmask='1111110')
        manana = hoy + timedelta(days=1)
        dias_transcurridos = np.busday_count(inicio_mes, manana, weekmask='1111110')
        dias_restantes = max(0, total_dias_mes - dias_transcurridos)
        
        acumulado = venta_hoy + venta_mes
        necesidad = (meta - acumulado) / dias_restantes if dias_restantes > 0 else 0
        avance = (acumulado / meta) * 100 if meta > 0 else 0.0
        
        dias_para_promedio = max(1, dias_transcurridos)
        proyeccion_dinero = (acumulado / dias_para_promedio) * total_dias_mes
        proyeccion_final = (proyeccion_dinero / meta) * 100 if meta > 0 else 0.0

        st.markdown("---")
        st.subheader(f"Resultados y Proyecciones - {ruta_seleccionada.upper()}")

        m1, m2 = st.columns(2)
        with m1:
            st.metric(label="Acumulado Total", value=f"L. {acumulado:,.2f}", delta=f"Hoy: L. {venta_hoy:,.2f}")
        with m2:
            st.metric(label="Necesidad Diaria", value=f"L. {necesidad:,.2f}", delta=f"{dias_restantes} días restantes", delta_color="inverse")

        m3, m4 = st.columns(2)
        with m3:
            st.metric(label="Avance Actual", value=f"{avance:.2f}%", delta=f"Meta: L. {meta:,.0f}")
        with m4:
            st.metric(label="Proyección de Cierre", value=f"{proyeccion_final:.2f}%", delta=f"Est. L. {proyeccion_dinero:,.2f}")

        st.markdown("### Progreso de la Meta")
        st.progress(min(1.0, max(0.0, avance / 100.0)))

# ==========================================
# PESTAÑA 2: LIQUIDACIÓN DIARIA
# ==========================================
with pestana_liquidacion:
    st.subheader("Apartado de Liquidación Diaria")
    st.write("Ingrese los datos correspondientes para calcular el balance de saldos:")

    col_l1, col_l2 = st.columns(2)

    with col_l1:
        saldo_recibido = st.number_input("Ingrese el saldo que le mandaron:", value=0.0, format="%.2f", step=100.0, key="liq_recibido")
        saldo_entregado = st.number_input("Ingrese el saldo que entregó el día anterior:", value=0.0, format="%.2f", step=100.0, key="liq_ant")
    
    with col_l2:
        saldo_hoy = st.number_input("Ingrese el saldo que entrega hoy:", value=0.0, format="%.2f", step=100.0, key="liq_hoy")

    if st.button("Calcular Liquidación", type="primary", use_container_width=True, key="btn_liq"):
        
        # Fórmulas de liquidación
        total_saldo = saldo_recibido + saldo_entregado
        saldo_total = total_saldo - saldo_hoy
        multiplicar = saldo_total * 0.94

        st.markdown("---")
        st.subheader("Resumen de Liquidación")

        l1, l2 = st.columns(2)
        with l1:
            st.metric(label="Total Saldo General", value=f"L. {total_saldo:,.2f}")
            st.metric(label="Saldo Total", value=f"L. {saldo_total:,.2f}")
        with l2:
            st.metric(label="Total sin 0.94", value=f"L. {saldo_total:,.2f}")
            st.metric(label="Total con 0.94", value=f"L. {multiplicar:,.2f}")

        st.success("¡Liquidación procesada correctamente!")
