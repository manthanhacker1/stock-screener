# Stock Screener - Deployment Guide

## ✅ Complete Solution - COMPLETELY FREE

This stock screener has:
- ✅ Fundamental metrics screening
- ✅ Supertrend technical analysis
- ✅ Daily chart visualization
- ✅ Buy/Sell signals
- ✅ No cost to deploy

---

## 📋 What You Need (5 minutes setup)

1. **GitHub Account** - Free at https://github.com
2. **Streamlit Cloud** - Free deployment platform
3. **This code** - Already provided

---

## 🚀 Step-by-Step Deployment

### Step 1: Create GitHub Repository
```
1. Go to https://github.com/new
2. Repository name: "stock-screener"
3. Add description: "Fundamental & Technical Stock Screener"
4. Click "Create repository"
```

### Step 2: Upload Files to GitHub
```
1. In your new repository, click "Add file" → "Upload files"
2. Upload these files:
   - stock_screener.py
   - requirements.txt
   - (Optional) README.md

3. Commit changes
```

### Step 3: Deploy on Streamlit Cloud (FREE)
```
1. Go to https://streamlit.io/cloud
2. Click "New app"
3. Select:
   - Repository: your-username/stock-screener
   - Branch: main
   - File path: stock_screener.py
4. Click "Deploy"
```

That's it! Your website is LIVE in 2-3 minutes! 🎉

---

## 💻 Local Testing (Before Deploying)

### Install locally first:
```bash
# Install Python 3.8+

# Clone your repository
git clone https://github.com/YOUR-USERNAME/stock-screener.git
cd stock-screener

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run stock_screener.py
```

Opens at: http://localhost:8501

---

## 📊 Features Included

### Fundamental Filters:
- EPS (latest quarter checks)
- Market Capitalization > ₹1000 Cr
- Debt to Equity < 1
- Asset Turnover Ratio > 1
- Working Capital to Sales > 20%
- Sales Growth > 15%
- ROCE > 12%

### Technical Filters:
- **Supertrend Indicator** (daily, weekly, monthly capable)
- Price above/below Supertrend
- BUY/SELL signal detection
- Chart visualization with Supertrend overlay
- Trailing profit capability

---

## 🎯 How to Use

1. **Enter Stock Tickers** in left sidebar
   - Format: `RELIANCE.NS, TCS.NS, INFY.NS` (NSE)
   - Add `.BO` for BSE, `.NS` for NSE

2. **Adjust Filters**:
   - Market Cap minimum
   - Debt/Equity threshold
   - Sales growth requirement
   - ROCE minimum

3. **Click "Scan Stocks"**
   - Takes 10-30 seconds
   - Shows matched stocks ranked by score
   - Select any stock for detailed view

4. **View Results**:
   - Fundamental criteria check (✅/❌)
   - Technical analysis with chart
   - Supertrend signal status
   - Price vs Supertrend comparison

---

## 🔧 Customization Options

### Add More Stocks
Edit the default tickers:
```python
value="RELIANCE.NS, INFY.NS, TCS.NS, WIPRO.NS, HDFC.NS, LT.NS"
```

### Adjust Supertrend Parameters
In `calculate_supertrend()`:
```python
# period=10 (lookback days)
# multiplier=3 (ATR sensitivity)
calculate_supertrend(data, period=10, multiplier=3)
```

### Add More Fundamental Metrics
Add to `check_fundamental_criteria()` function

---

## 📱 Access Your Website

After deployment, you get a public URL:
```
https://stock-screener-{random}.streamlit.app/
```

**Share this link with your client!** ✅

---

## 🆓 COMPLETELY FREE Limits

- **Streamlit Cloud**: 
  - 1 GB RAM
  - 1 CPU
  - Unlimited apps
  - 100% free

- **Data Source (Yahoo Finance)**:
  - Free, no API key needed
  - Real-time data
  - Historical data available

---

## ⚡ Performance Tips

1. **First load**: 30-45 seconds (caching enabled)
2. **Subsequent loads**: 10-15 seconds
3. **Add `.NS` to all Indian stocks**
4. **Max 10-15 stocks per scan** (for speed)

---

## 🐛 Troubleshooting

### "No data found"
- Check ticker format: Use `.NS` for NSE
- Example: `RELIANCE.NS` not `RELIANCE`

### "Slow loading"
- Reduce number of stocks
- First load slower due to data fetching

### "Chart not showing"
- Some stocks may have limited historical data
- Try another stock

---

## 📈 Data Sources

- **Stock prices**: Yahoo Finance (yfinance)
- **Fundamentals**: Yahoo Finance API
- **All data**: Real-time, no delays

---

## 🎓 Understanding The Metrics

**Supertrend Indicator:**
- When price > Supertrend line = BUY signal
- When price < Supertrend line = SELL signal
- Red line = Dynamic support/resistance

**Fundamental Score:**
- Shows how many criteria each stock passes
- Higher score = Better match

---

## 📞 Support

If deployment fails:
1. Check GitHub repository is public
2. Verify `requirements.txt` exists
3. Clear Streamlit cache: Settings → Clear cache
4. Restart deployment in Streamlit Cloud

---

## ✨ Next Steps

1. ✅ Deploy this version (5 minutes)
2. ✅ Test with your stocks
3. ✅ Share URL with client
4. ✅ Customize as needed

**Cost: ₹0 | Time to launch: 5 minutes** 🚀

---

## 🔐 No API Keys or Payments Required!

- No registration fees
- No data costs
- No subscription needed
- Everything is FREE

Your client gets a professional stock screening website at ZERO COST! 💰
