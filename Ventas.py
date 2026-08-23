import streamlit as st
import numpy as np
from datetime import date

st.title("Reporte Diario de Ventas")

# Entradas en la web
meta = st.number_input("Meta del mes:", value=1050000.0, format="%.2f")
ventahoy = st.number_input("Venta total de hoy:", value=0.0, format="%.2f")
ventames = st.number_input("Acumulado del mes:", value=0.0, format="%.2f")

if st.button("Calcular Reporte"):
    # Tus cálculos automáticos
    hoy = date.today()
    inicio_mes = f"{hoy.year}-{hoy.month:02d}-01"
    
    # Próximo mes para el límite de numpy
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
    
    # Se usa la meta ingresada por el usuario en el cuadro de texto
    nesecidad = (meta - acumulado) / dias_restantes if dias_restantes > 0 else 0
    
    # Evitar división por cero si la meta es 0
    if meta > 0:
        avance = (acumulado / meta) * 100
    else:
        avance = 0.0
    
    dias_para_promedio = max(1, dias_transcurridos)
    proyeccion_dinero = (acumulado / dias_para_promedio) * total_dias_mes
    
    if meta > 0:
        proyeccion_final = (proyeccion_dinero / meta) * 100
    else:
        proyeccion_final = 0.0

    # Mostrar resultados en pantalla
    st.success(f"Acumulado total: {acumulado:,.2f}")
    st.info(f"Necesidad diaria: {nesecidad:,.2f}")
    st.write(f"Avance actual: **{avance:.2f}%**")
    st.write(f"Proyección de Cierre: **{proyeccion_final:.2f}%**")
