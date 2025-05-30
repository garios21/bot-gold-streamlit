
import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Análisis Técnico del Oro", layout="centered")

st.title("Análisis Técnico del Oro")
st.markdown("""
Esta app evalúa el **precio del oro**, las **medias móviles** (EMA 20 y EMA 50) y el **RSI** 
para ofrecer una **recomendación de entrada o espera**.
""")
st.divider()

# Entradas manuales simuladas
st.subheader("Valores Técnicos")
price = st.number_input("Precio actual del oro (USD)", min_value=0.0, value=3300.0)
ema_20 = st.number_input("EMA 20", min_value=0.0, value=3310.0)
ema_50 = st.number_input("EMA 50", min_value=0.0, value=3295.0)
rsi = st.slider("RSI", min_value=0, max_value=100, value=50)

st.divider()

# Lógica de recomendación simple
st.subheader("Recomendación")
if price > ema_20 > ema_50 and rsi < 70:
    st.success("✅ Condición favorable. Recomendación: ENTRAR EN LONG.")
elif price < ema_20 < ema_50 and rsi > 30:
    st.warning("⚠️ Tendencia bajista en desarrollo. Recomendación: ESPERAR O SHORT.")
else:
    st.info("ℹ️ Condiciones mixtas. Recomendación: ESPERAR.")

# Pie de página
st.markdown("---")
st.caption(f"Última evaluación: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
