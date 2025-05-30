
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

        try:
            precio = float(last['Close'])
            ema20 = float(last['EMA20'])
            ema50 = float(last['EMA50'])
            rsi = float(last['RSI'])

            st.metric("💰 Precio Actual del Oro", f"${precio:.2f}")
            st.write(f"**EMA 20:** ${ema20:.2f}")
            st.write(f"**EMA 50:** ${ema50:.2f}")
            st.write(f"**RSI:** {rsi:.2f}")

            # Lógica de recomendación
            if precio > ema20 > ema50 and rsi < 70:
                st.success("✅ Recomendación: Considera ENTRAR en LONG (compra).")
            elif precio < ema20 < ema50 and rsi > 30:
                st.success("✅ Recomendación: Considera ENTRAR en SHORT (venta).")
            else:
                st.warning("⏸️ Recomendación: ESPERA. No hay una señal clara aún.")

            try:
                st.line_chart(data[['Close', 'EMA20', 'EMA50']].dropna().tail(100))
            except Exception as graph_error:
                st.warning(f"⚠️ No se pudo mostrar el gráfico: {graph_error}")

        except Exception as e:
            st.error(f"❌ Error al procesar los datos: {e}")
    else:
        st.warning("⚠️ No hay suficientes datos limpios para el análisis. Intenta más tarde.")
