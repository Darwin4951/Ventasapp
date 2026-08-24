import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import pytz  # Para asegurar la zona horaria correcta

# Configuración de la página (debe ser lo primero de Streamlit)
st.set_page_config(page_title="Reporte Diario de Ventas", page_icon="📊", layout="centered")

# Título y descripción elegante
st.title("📊 Control y Proyección de Ventas")
st.markdown("---")

# Sección de entradas organizadas en dos columnas para mejor estética
st.subheader("Parámetros y Datos del Día")
col1, col2 = st.columns(2)

with col1:
    meta = st.number_input("Meta del mes", value=1050000.0, format="%.2f", step=10000.0)
    ventahoy = st.number_input("Venta total de hoy", value=0.0, format="%.2f", step=1000.0)
with col2:
    ventames = st.number_input("Acumulado previo del mes", value=0.0, format="%.2f", step=1000.0)
    st.write("") 
    st.write("")

# Botón principal estilizado
calcular = st.button("Calcular Resultados", type="primary", use_container_width=True)

if calcular:
    # 1. Fijar la zona horaria correcta (Honduras / Centroamérica) para que no varíe en el celular
    zona_horaria = pytz.timezone('America/Tegucigalpa')
    hoy = datetime.now(zona_horaria).date()
    
    # 2. Definir inicio y fin de mes como objetos de fecha (Date)
    inicio_mes = datetime(hoy.year, hoy.month, 1).date()
    
    if hoy.month == 12:
        fin_mes = datetime(hoy.year + 1, 1, 1).date()
    else:
        fin_mes = datetime(hoy.year, hoy.month + 1, 1).date()

    # 3. Total de días laborales del mes (Lunes a Sábado -> '1111110')
    total_dias_mes = np.busday_count(inicio_mes, fin_mes, weekmask='1111110')
    
    # 4. Días laborales transcurridos
    # Como np.busday_count excluye el último día, le sumamos 1 día a "hoy" (hasta mañana)
    # Numpy automáticamente sabrá si hoy es domingo y no lo contará.
    manana = hoy + timedelta(days=1)
    dias_transcurridos = np.busday_count(inicio_mes, manana, weekmask='1111110')

    # Días restantes
    dias_restantes = max(0, total_dias_mes - dias_transcurridos)
    
    # Cálculos financieros
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
