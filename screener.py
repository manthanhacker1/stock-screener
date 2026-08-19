import pandas as pd
import ta
import yfinance as yf


def get_supertrend(df, period=10, multiplier=3):
    """Calculates Supertrend Indicator reliably."""
    if len(df) < period:
        return df

    high, low, close = df["High"], df["Low"], df["Close"]
    atr = ta.volatility.average_true_range(high, low, close, window=period)
    hl2 = (high + low) / 2

    basic_upper = hl2 + (multiplier * atr)
    basic_lower = hl2 - (multiplier * atr)

    upperband = pd.Series(0.0, index=df.index)
    lowerband = pd.Series(0.0, index=df.index)
    st = pd.Series(0.0, index=df.index)
    trend = pd.Series(True, index=df.index)

    for i in range(1, len(df)):
        if (
            basic_upper.iloc[i] < upperband.iloc[i - 1]
            or close.iloc[i - 1] > upperband.iloc[i - 1]
        ):
            upperband.iloc[i] = basic_upper.iloc[i]
        else:
            upperband.iloc[i] = upperband.iloc[i - 1]

        if (
            basic_lower.iloc[i] > lowerband.iloc[i - 1]
            or close.iloc[i - 1] < lowerband.iloc[i - 1]
        ):
            lowerband.iloc[i] = basic_lower.iloc[i]
        else:
            lowerband.iloc[i] = lowerband.iloc[i - 1]

        if close.iloc[i] > upperband.iloc[i - 1]:
            trend.iloc[i] = True
        elif close.iloc[i] < lowerband.iloc[i - 1]:
            trend.iloc[i] = False
        else:
            trend.iloc[i] = trend.iloc[i - 1]

        st.iloc[i] = lowerband.iloc[i] if trend.iloc[i] else upperband.iloc[i]

    df["Supertrend"] = st
    df["ST_Trend"] = trend
    return df


def analyze_stock(ticker):
    """Analyzes Price Action & Supertrend with safe error boundaries."""
    try:
        t = yf.Ticker(ticker)

        # Technical Data Fetching
        df_daily = t.history(period="6m", interval="1d")
        df_weekly = t.history(period="2y", interval="1wk")
        df_monthly = t.history(period="5y", interval="1mo")

        if df_daily.empty or len(df_daily) < 15:
            return None

        # Supertrend Calculations
        df_daily = get_supertrend(df_daily)
        df_weekly = (
            get_supertrend(df_weekly) if not df_weekly.empty else df_daily
        )
        df_monthly = (
            get_supertrend(df_monthly) if not df_monthly.empty else df_daily
        )

        st_daily_buy = df_daily["ST_Trend"].iloc[-1]
        st_weekly_buy = df_weekly["ST_Trend"].iloc[-1]
        st_monthly_buy = df_monthly["ST_Trend"].iloc[-1]

        close_price = df_daily["Close"].iloc[-1]
        st_daily_val = df_daily["Supertrend"].iloc[-1]

        # Status Logic
        if st_daily_buy and st_weekly_buy and st_monthly_buy:
            status = "STRONG BUY ✅"
        elif not st_daily_buy:
            status = "EXIT SIGNAL 🚨"
        else:
            status = "NEUTRAL ⏳"

        return {
            "Ticker": ticker.replace(".NS", ""),
            "Price": round(close_price, 2),
            "Daily ST": "BUY" if st_daily_buy else "SELL",
            "Weekly ST": "BUY" if st_weekly_buy else "SELL",
            "Monthly ST": "BUY" if st_monthly_buy else "SELL",
            "Trailing SL (Daily ST)": round(st_daily_val, 2),
            "Status": status,
        }
    except Exception:
        return None
