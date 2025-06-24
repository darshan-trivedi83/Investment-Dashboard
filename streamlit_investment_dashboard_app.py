
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Investment Dashboard", layout="wide")
st.title("📈 Investment Dashboard with Alerts")

# --- Ticker input ---
tickers = st.text_input("Enter stock tickers separated by commas", "AAPL,MSFT,TCS.NS,INFY.NS").upper().split(",")

data = []

for ticker in tickers:
    try:
        stock = yf.Ticker(ticker.strip())
        info = stock.info
        df = stock.history(period="1mo")

        price = info.get("currentPrice")
        pe = info.get("trailingPE")
        eps = info.get("trailingEps")
        industry_pe = info.get("forwardPE")

        alert = ""
        if pe and industry_pe and pe < industry_pe:
            alert = "✅ Undervalued (P/E < Industry)"
        elif pe and industry_pe:
            alert = "⚠️ Overvalued (P/E > Industry)"
        else:
            alert = "❓ Data Incomplete"

        data.append({
            "Ticker": ticker.strip(),
            "Price": price,
            "P/E": pe,
            "EPS": eps,
            "Industry P/E": industry_pe,
            "Alert": alert
        })

        # --- Chart ---
        with st.expander(f"📊 Price Chart - {ticker.strip()}"):
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode='lines', name='Close Price'))
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.warning(f"⚠️ Could not fetch data for {ticker.strip()}: {e}")

# --- Display Table ---
st.subheader("🔍 Summary Table with Alerts")
st.dataframe(pd.DataFrame(data))
