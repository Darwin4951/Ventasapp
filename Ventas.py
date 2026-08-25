import streamlit as np
import streamlit as st
import numpy as np
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Librería nativa, no requiere instalación en la nube


st.set_page_config(page_title="Reporte Diario de Ventas por Ruta", page_icon="📊", layout="centered")


st.title("📊 Control y Proyección de Ventas por Ruta")
st.markdown("---")

# --- DICCIONARIO MANUAL DE METAS POR RUTA ---
# escribir manualmente la meta exacta para cada ruta
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

# --- SELECCIÓN DE RUTA ACTIVA ---
st.subheader("Selección de Ruta")
lista_rutas = list(METAS_POR_RUTA.keys())

# Selector desplegable para elegir la ruta
ruta_seleccionada = st.selectbox("Elige la ruta a gestionar:", lista_rutas)

# Obtenemos automáticamente la meta manual asignada a esta ruta
meta_asignada = METAS_POR_RUTA[ruta_seleccionada]
st.info(f"📌 Estás trabajando en la **{ruta_seleccionada.upper()}** | Meta mensual fija: **L. {meta_asignada:,.2f}**")

st.markdown("---")

# --- ENTRADAS DE VENTAS DEL DÍA ---
st.subheader(f"Parámetros y Datos del Día - {ruta_seleccionada.upper()}")
col1, col2 = st.columns(2)

with col1:
    # La meta toma por defecto el valor 
    meta = st.number_input("Meta del mes de esta ruta", value=meta_asignada, format="%.2f", step=10000.0, key=f"meta_{ruta_seleccionada}")
    ventahoy = st.number_input("Venta total de hoy", value=0.0, format="%.2f", step=1000.0, key=f"hoy_{ruta_seleccionada}")
with col2:
    ventames = st.number_input("Acumulado previo del mes", value=0.0, format="%.2f", step=1000.0, key=f"mes_{ruta_seleccionada}")
    st.write("") 
    st.write("")

# Botón principal estilizado
calcular = st.button("Calcular Resultados de la Ruta", type="primary", use_container_width=True)

if calcular:
    #  Fijar la zona horaria correcta usando ZoneInfo (nativo de Python)
    zona_horaria = ZoneInfo('America/Tegucigalpa')
    hoy = datetime.now(zona_horaria).date()
    
    #  Definir inicio y fin de mes como objetos de fecha (Date)
    inicio_mes = datetime(hoy.year, hoy.month, 1).date()
    
    if hoy.month == 12:
        fin_mes = datetime(hoy.year + 1, 1, 1).date()
    else:
        fin_mes = datetime(hoy.year, hoy.month + 1, 1).date()

    #  Total de días laborales del mes (Lunes a Sábado -> '1111110')
    total_dias_mes = np.busday_count(inicio_mes, fin_mes, weekmask='1111110')
    
    # Días laborales transcurridos (sumando 1 día para incluir "hoy" correctamente)
    manana = hoy + timedelta(days=1)
    dias_transcurridos = np.busday_count(inicio_mes, manana, weekmask='1111110')

    # Días restantes
    dias_restantes = max(0, total_dias_mes - dias_transcurridos)
    
    # Cálculos hacer una soloa variable def a futuro
    acumulado = ventahoy + ventames
    nesecidad = (meta - acumulado) / dias_restantes if dias_restantes > 0 else 0
    avance = (acumulado / meta) * 100 if meta > 0 else 0.0
    
    dias_para_promedio = max(1, dias_transcurridos)
    proyeccion_dinero = (acumulado / dias_para_promedio) * total_dias_mes
    proyeccion_final = (proyeccion_dinero / meta) * 100 if meta > 0 else 0.0

    # Separador para los resultados
    st.markdown("---")
    st.subheader(f"📈 Resultados y Proyecciones - {ruta_seleccionada.upper()}")

    # Primera fila de métricas visuales 
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
