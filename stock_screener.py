import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
from functools import lru_cache

st.set_page_config(page_title="Stock Screener - Fundamental & Technical", layout="wide")

st.title("📊 Stock Screener - Fundamental & Technical Analysis")
st.markdown("Screens stocks based on fundamental metrics and Supertrend technical indicator")

# ============ FUNDAMENTAL METRICS FUNCTIONS ============

def calculate_supertrend(data, period=10, multiplier=3):
    """Calculate Supertrend indicator"""
    high = data['High']
    low = data['Low']
    close = data['Close']
    
    hl2 = (high + low) / 2
    atr = calculate_atr(data, period)
    
    data['basic_ub'] = hl2 + multiplier * atr
    data['basic_lb'] = hl2 - multiplier * atr
    
    data['final_ub'] = data['basic_ub'].where(
        (data['basic_ub'] < data['Close'].shift(1)) | 
        (data['Close'].shift(1) > data['basic_ub'].shift(1)), 
        data['basic_ub'].shift(1)
    )
    
    data['final_lb'] = data['basic_lb'].where(
        (data['basic_lb'] > data['Close'].shift(1)) | 
        (data['Close'].shift(1) < data['basic_lb'].shift(1)), 
        data['basic_lb'].shift(1)
    )
    
    data['Supertrend'] = np.nan
    data['ST_Signal'] = np.nan
    
    for i in range(len(data)):
        if i < 1:
            continue
        if np.isnan(data['final_ub'].iloc[i]) or np.isnan(data['final_lb'].iloc[i]):
            continue
            
        if data['Supertrend'].iloc[i-1] == data['final_ub'].iloc[i-1]:
            if data['Close'].iloc[i] <= data['final_ub'].iloc[i]:
                data.loc[data.index[i], 'Supertrend'] = data['final_ub'].iloc[i]
                data.loc[data.index[i], 'ST_Signal'] = 'SELL'
            else:
                data.loc[data.index[i], 'Supertrend'] = data['final_lb'].iloc[i]
                data.loc[data.index[i], 'ST_Signal'] = 'BUY'
        else:
            if data['Close'].iloc[i] >= data['final_lb'].iloc[i]:
                data.loc[data.index[i], 'Supertrend'] = data['final_lb'].iloc[i]
                data.loc[data.index[i], 'ST_Signal'] = 'BUY'
            else:
                data.loc[data.index[i], 'Supertrend'] = data['final_ub'].iloc[i]
                data.loc[data.index[i], 'ST_Signal'] = 'SELL'
    
    return data

def calculate_atr(data, period=10):
    """Calculate Average True Range"""
    data['tr1'] = data['High'] - data['Low']
    data['tr2'] = abs(data['High'] - data['Close'].shift(1))
    data['tr3'] = abs(data['Low'] - data['Close'].shift(1))
    data['tr'] = data[['tr1', 'tr2', 'tr3']].max(axis=1)
    atr = data['tr'].rolling(period).mean()
    return atr

@lru_cache(maxsize=32)
def get_stock_data(ticker, period='1y'):
    """Fetch stock data from Yahoo Finance"""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        info = stock.info
        return hist, info
    except:
        return None, None

def check_fundamental_criteria(ticker, info):
    """Check if stock meets fundamental criteria"""
    criteria_results = {}
    
    try:
        # EPS checks
        eps_current = info.get('trailingEps', None)
        eps_forward = info.get('forwardEps', None)
        criteria_results['EPS > 0'] = eps_current > 0 if eps_current else False
        
        # Market cap check
        market_cap = info.get('marketCap', 0)
        criteria_results['Market Cap > 1000Cr'] = market_cap > 1000000000
        
        # Debt to Equity
        debt_to_equity = info.get('debtToEquity', float('inf'))
        criteria_results['Debt to Equity < 1'] = debt_to_equity < 1 if debt_to_equity != float('inf') else False
        
        # Asset Turnover (approximation: revenue/total assets)
        revenue = info.get('totalRevenue', 0)
        total_assets = info.get('totalAssets', 1)
        asset_turnover = revenue / total_assets if total_assets > 0 else 0
        criteria_results['Asset Turnover > 1'] = asset_turnover > 1
        
        # Sales growth
        quarterly_revenue = info.get('lastQuarterlyRevenue', 0)
        prior_quarterly_revenue = info.get('previousQuarterlyRevenue', 1)
        sales_growth = ((quarterly_revenue - prior_quarterly_revenue) / prior_quarterly_revenue * 100) if prior_quarterly_revenue > 0 else 0
        criteria_results['Sales Growth > 15%'] = sales_growth > 15
        
        # Return on Capital Employed (approximation)
        roce = info.get('returnOnCapital', 0)
        criteria_results['ROCE > 12%'] = roce > 0.12 if roce else False
        
        # Working Capital to Sales (approximation)
        wc_to_sales = info.get('workingCapital', 0) / revenue if revenue > 0 else 0
        criteria_results['WC to Sales > 20%'] = wc_to_sales > 0.20
        
        return criteria_results
    except Exception as e:
        st.error(f"Error checking fundamentals: {e}")
        return {}

def check_technical_criteria(ticker, hist):
    """Check if stock meets technical (Supertrend) criteria"""
    try:
        if hist is None or len(hist) < 20:
            return {}, None
        
        # Calculate daily supertrend
        daily_data = hist.copy()
        daily_data = calculate_supertrend(daily_data, period=10, multiplier=3)
        
        latest = daily_data.iloc[-1]
        current_price = latest['Close']
        supertrend = latest['Supertrend']
        signal = latest['ST_Signal']
        
        technical_results = {
            'Price > Supertrend (Daily)': current_price > supertrend,
            'Daily Signal': signal if pd.notna(signal) else 'N/A'
        }
        
        return technical_results, daily_data
    except:
        return {}, None

# ============ SIDEBAR CONFIGURATION ============
st.sidebar.header("⚙️ Filter Configuration")

# Fundamental filters
st.sidebar.subheader("Fundamental Criteria")
min_market_cap = st.sidebar.slider("Min Market Cap (Billions)", 1, 100, 1)
max_debt_to_equity = st.sidebar.slider("Max Debt to Equity", 0.1, 3.0, 1.0)
min_roce = st.sidebar.slider("Min ROCE (%)", 0, 50, 12)
min_sales_growth = st.sidebar.slider("Min Sales Growth (%)", 0, 100, 15)

# Technical filters
st.sidebar.subheader("Technical Criteria (Supertrend)")
require_above_st = st.sidebar.checkbox("Price must be above Supertrend", value=True)
require_buy_signal = st.sidebar.checkbox("Must be in BUY mode", value=True)

# Stock input
st.sidebar.subheader("Stock Input")
stock_input = st.sidebar.text_area("Enter stock tickers (comma-separated)", 
                                    value="RELIANCE.NS, INFY.NS, TCS.NS, WIPRO.NS, HDFC.NS",
                                    height=100)

# ============ MAIN LOGIC ============
if st.sidebar.button("🔍 Scan Stocks", key="scan_btn"):
    tickers = [t.strip() for t in stock_input.split(",") if t.strip()]
    
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, ticker in enumerate(tickers):
        status_text.text(f"Scanning {ticker}... ({idx+1}/{len(tickers)})")
        
        hist, info = get_stock_data(ticker, period='1y')
        
        if hist is None or info is None:
            continue
        
        # Check fundamental criteria
        fund_criteria = check_fundamental_criteria(ticker, info)
        
        # Check technical criteria
        tech_criteria, daily_data = check_technical_criteria(ticker, hist)
        
        # Score calculation
        fund_passed = sum(1 for v in fund_criteria.values() if v is True)
        fund_total = len(fund_criteria)
        
        tech_passed = 0
        if 'Price > Supertrend (Daily)' in tech_criteria and tech_criteria['Price > Supertrend (Daily)']:
            tech_passed += 1
        if 'Daily Signal' in tech_criteria and tech_criteria['Daily Signal'] == 'BUY':
            tech_passed += 1
        tech_total = 2
        
        total_score = fund_passed + tech_passed
        
        results.append({
            'Ticker': ticker,
            'Current Price': hist['Close'].iloc[-1] if len(hist) > 0 else 0,
            'Fundamental Score': f"{fund_passed}/{fund_total}",
            'Technical Score': f"{tech_passed}/{tech_total}",
            'Total Score': total_score,
            'Supertrend Signal': tech_criteria.get('Daily Signal', 'N/A'),
            'Fund Details': fund_criteria,
            'Tech Details': tech_criteria,
            'Chart Data': daily_data
        })
        
        progress_bar.progress((idx + 1) / len(tickers))
    
    status_text.empty()
    progress_bar.empty()
    
    if results:
        # Display results
        st.success(f"✅ Scanned {len(results)} stocks")
        
        # Create summary dataframe
        summary_df = pd.DataFrame([{
            'Ticker': r['Ticker'],
            'Current Price': f"₹{r['Current Price']:.2f}",
            'Fundamental': r['Fundamental Score'],
            'Technical': r['Technical Score'],
            'Total Score': r['Total Score'],
            'Signal': r['Supertrend Signal']
        } for r in results])
        
        # Sort by total score
        summary_df['Total Score'] = summary_df['Total Score'].astype(int)
        summary_df = summary_df.sort_values('Total Score', ascending=False)
        
        st.dataframe(summary_df, use_container_width=True)
        
        # Detailed view
        st.subheader("📈 Detailed Analysis")
        selected_ticker = st.selectbox("Select stock for detailed view", [r['Ticker'] for r in results])
        
        selected_result = next(r for r in results if r['Ticker'] == selected_ticker)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Fundamental Criteria")
            fund_data = pd.DataFrame([
                {'Criteria': k, 'Status': '✅' if v else '❌'}
                for k, v in selected_result['Fund Details'].items()
            ])
            st.dataframe(fund_data, use_container_width=True)
        
        with col2:
            st.subheader("Technical Criteria (Supertrend)")
            tech_data = pd.DataFrame([
                {'Criteria': k, 'Value': v}
                for k, v in selected_result['Tech Details'].items()
            ])
            st.dataframe(tech_data, use_container_width=True)
        
        # Chart
        if selected_result['Chart Data'] is not None:
            st.subheader(f"Price Chart with Supertrend - {selected_ticker}")
            
            chart_data = selected_result['Chart Data'].tail(60)
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=chart_data.index,
                y=chart_data['Close'],
                name='Close Price',
                line=dict(color='blue', width=2)
            ))
            
            if 'Supertrend' in chart_data.columns:
                fig.add_trace(go.Scatter(
                    x=chart_data.index,
                    y=chart_data['Supertrend'],
                    name='Supertrend',
                    line=dict(color='red', width=1, dash='dash')
                ))
            
            fig.update_layout(
                title=f"Price Action with Supertrend",
                xaxis_title="Date",
                yaxis_title="Price (₹)",
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("⚠️ No data found. Check ticker symbols (use .NS for NSE)")

# ============ INSTRUCTIONS ============
with st.expander("📖 Instructions & Help"):
    st.markdown("""
    ### How to use this screener:
    
    **1. Fundamental Criteria:**
    - EPS > 0
    - Market Cap > ₹1000 Cr
    - Debt to Equity < 1
    - Asset Turnover > 1
    - Sales Growth > 15%
    - ROCE > 12%
    
    **2. Technical Criteria (Supertrend):**
    - Price must be above Supertrend line
    - Daily signal must be BUY
    
    **3. Ticker Format:**
    - For NSE (India): Add `.NS` suffix (e.g., `RELIANCE.NS`)
    - For BSE: Add `.BO` suffix (e.g., `RELIANCE.BO`)
    - For US stocks: Use ticker directly (e.g., `AAPL`)
    
    **4. Deployment:**
    - Free on Streamlit Cloud: https://streamlit.io/cloud
    - GitHub required for free deployment
    
    """)

st.sidebar.markdown("---")
st.sidebar.markdown("**📱 Deploy Free on Streamlit Cloud**")
st.sidebar.markdown("[GitHub → Streamlit Cloud](https://streamlit.io/cloud)")
