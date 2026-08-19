import pandas as pd
import streamlit as st
from screener import analyze_stock

st.set_page_config(page_title="Fundamental & Supertrend Screener", layout="wide")
st.title("📈 Stock Screener & Trailing SL Dashboard")

DEFAULT_WATCHLIST = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "ICICIBANK.NS", "BHARTIARTL.NS", "TATASTEEL.NS", "LT.NS", "HDFCBANK.NS"]

st.sidebar.header("⚙️ Configuration")
tickers_input = st.sidebar.text_area("Enter Stocks Tickers (NSE suffix .NS):", value=", ".join(DEFAULT_WATCHLIST), height=150)
tickers = [t.strip() for t in tickers_input.split(",") if t.strip()]

if st.button("🚀 Run Screener Scan"):
    with st.spinner("Processing Data..."):
        results = [analyze_stock(ticker) for ticker in tickers if analyze_stock(ticker) is not None]
        if results:
            df = pd.DataFrame(results)
            st.subheader("Filtered & Monitored Stocks")
            st.dataframe(df, use_container_width=True)

            exits = df[df["Status"].str.contains("EXIT")]
            if not exits.empty:
                st.error("⚠️ Stocks to Exit (Daily Supertrend Turned SELL):")
                st.table(exits[["Ticker", "Price", "Trailing SL (Daily ST)", "Status"]])
        else:
            st.warning("No stocks matched all strict fundamental + multi-timeframe criteria.")
