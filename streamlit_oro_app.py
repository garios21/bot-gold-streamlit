
import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Oro - Recomendación de Inversión", layout="centered")

# Título
st.title("📈 Evaluación de Inversión en Oro")

# Obtener datos históricos
data = yf.download("GC=F", period="1mo", interval="1h")  # Futuros del oro

if data.empty:
    st.error("No se pudieron obtener datos. Verifica la conexión o el símbolo.")
else:
    # Cálculo de EMA y RSI
    data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
    data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()

    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))

    # Eliminar filas con valores NaN
    data = data.dropna()

    if not data.empty:
        last = data.iloc[-1]

        st.metric("💰 Precio Actual del Oro", f"${last['Close']:.2f}")
        st.write(f"**EMA 20:** ${last['EMA20']:.2f}")
        st.write(f"**EMA 50:** ${last['EMA50']:.2f}")
        st.write(f"**RSI:** {last['RSI']:.2f}")

        # Lógica de recomendación
        if last['Close'] > last['EMA20'] > last['EMA50'] and last['RSI'] < 70:
            st.success("✅ Recomendación: Considera ENTRAR en LONG (compra).")
        elif last['Close'] < last['EMA20'] < last['EMA50'] and last['RSI'] > 30:
            st.success("✅ Recomendación: Considera ENTRAR en SHORT (venta).")
        else:
            st.warning("⏸️ Recomendación: ESPERA. No hay una señal clara aún.")

        # Mostrar gráfico
        st.line_chart(data[['Close', 'EMA20', 'EMA50']].tail(100))
    else:
        st.warning("⚠️ No hay suficientes datos limpios para el análisis. Intenta más tarde.")
