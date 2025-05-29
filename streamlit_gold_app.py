
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Título
st.title("Análisis Técnico de Oro (GOLD)")

# Carga de datos de Yahoo Finance
data = yf.download("GC=F", period="15d", interval="4h")  # Oro futuro, 4h
data["EMA20"] = data["Close"].ewm(span=20, adjust=False).mean()
data["EMA50"] = data["Close"].ewm(span=50, adjust=False).mean()
delta = data["Close"].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / avg_loss
data["RSI"] = 100 - (100 / (1 + rs))

# Mostrar últimos valores
st.write("Últimos datos:")
st.dataframe(data.tail())

# Indicador de señal
ultima = data.iloc[-1]
signal = "NEUTRAL"
if ultima["Close"] > ultima["EMA20"] > ultima["EMA50"] and ultima["RSI"] < 70:
    signal = "LONG"
elif ultima["Close"] < ultima["EMA20"] < ultima["EMA50"] and ultima["RSI"] > 30:
    signal = "SHORT"

st.subheader(f"📈 Señal técnica: {signal}")

# Graficar
fig, ax = plt.subplots()
data["Close"].plot(ax=ax, label="Close", color="black")
data["EMA20"].plot(ax=ax, label="EMA20", color="green")
data["EMA50"].plot(ax=ax, label="EMA50", color="red")
ax.set_title("Precio del Oro con EMA20 y EMA50")
ax.legend()
st.pyplot(fig)

# RSI plot
st.subheader("Índice RSI")
fig2, ax2 = plt.subplots()
data["RSI"].plot(ax=ax2, color="purple")
ax2.axhline(70, color="red", linestyle="--")
ax2.axhline(30, color="green", linestyle="--")
ax2.set_title("RSI")
st.pyplot(fig2)
