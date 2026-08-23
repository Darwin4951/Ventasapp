import streamlit as st
import numpy as np
from datetime import date

# Configuración de la página (debe ser lo primero de Streamlit)
st.set_page_config(page_title="Reporte Diario de Ventas", page_icon="📊", layout="centered")

# Título y descripción elegante
st.title("📊 Control y Proyección de Ventas")
st.markdown("---")

# Sección de entradas organizadas en dos columnas para mejor estética
st.subheader("1. Parámetros y Datos del Día")
col1, col2 = st.columns(2)

with col1:
    meta = st.number_input("Meta del mes", value=1050000.0, format="%.2f", step=10000.0)
    ventahoy = st.number_input("Venta total de hoy", value=0.0, format="%.2f", step=1000.0)

with col2:
    ventames = st.number_input("Acumulado previo del mes", value=0.0, format="%.2f", step=1000.0)
    # Espacio visual alineado
    st.write("") 
    st.write("")

# Botón principal estilizado
calcular = st.button("🚀 Calcular Resultados", type="primary", use_container_width=True)

if calcular:
    # Cálculos automáticos
    hoy = date.today()
    inicio_mes = f"{hoy.year}-{hoy.month:02d}-01"
    
    if hoy.month == 12:
        fin_mes = f"{hoy.year + 1}-01-01"
    else:
        fin_mes = f"{hoy.year}-{hoy.month + 1:02d}-01"

    total_dias_mes = np.busday_count(inicio_mes, fin_mes, weekmask='1111110')
    dias_transcurridos = np.busday_count(inicio_mes, hoy.strftime('%Y-%m-%d'), weekmask='1111110')
    if hoy.weekday() != 6:
        dias_transcurridos += 1

    dias_restantes = max(0, total_dias_mes - dias_transcurridos)
    acumulado = ventahoy + ventames
    
    nesecidad = (meta - acumulado) / dias_restantes if dias_restantes > 0 else 0
    avance = (acumulado / meta) * 100 if meta > 0 else 0.0
    
    dias_para_promedio = max(1, dias_transcurridos)
    proyeccion_dinero = (acumulado / dias_para_promedio) * total_dias_mes
    proyeccion_final = (proyeccion_dinero / meta) * 100 if meta > 0 else 0.0

    # Separador para los resultados
    st.markdown("---")
    st.subheader("📈 Resultados y Proyecciones")

    # Primera fila de métricas visuales (Tarjetas)
    m1, m2 = st.columns(2)
    with m1:
        st.metric(label="Acumulado Total", value=f"L. {acumulado:,.2f}", delta=f"Hoy: L. {ventahoy:,.2f}")
    with m2:
        st.metric(label="Necesidad Diaria", value=f"L. {nesecidad:,.2f}", delta=f"{dias_restantes} días restantes", delta_color="inverse")

    # Segunda fila de métricas con indicadores de avance
    m3, m4 = st.columns(2)
    with m3:
        st.metric(label="Avance Actual", value=f"{avance:.2f}%", delta=f"Meta: L. {meta:,.0f}")
    with m4:
        st.metric(label="Proyección de Cierre", value=f"{proyeccion_final:.2f}%", delta=f"Est. L. {proyeccion_dinero:,.2f}")

    # Barra de progreso visual para el avance
    st.markdown("### Progreso de la Meta")
    porcentaje_barra = min(1.0, max(0.0, avance / 100.0))
    st.progress(porcentaje_barra)
