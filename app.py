import streamlit as st
import requests
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
import pytz
import streamlit.components.v1 as components

st.set_page_config(page_title="SMART TRADING AI", page_icon="📈", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    .main-title { color: #d4af37; text-align: center; font-size: 2.2rem; font-weight: bold; }
    .sub-title { color: #58a6ff; text-align: center; font-size: 1.1rem; margin-bottom: 2rem; }
    .stButton>button { background-color: #1f6feb; color: white; border-radius: 6px; width: 100%; font-weight: bold; }
    .clock { color: #d4af37; text-align: center; font-size: 1.2rem; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

algeria_tz = pytz.timezone('Africa/Algiers')
now = datetime.now(algeria_tz)
time_str = now.strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f'<div class="clock">🇩🇿 توقيت الجزائر: {time_str}</div>', unsafe_allow_html=True)

st.markdown('<div class="main-title">🌟 SMART TRADING AI 🌟</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">GOLDRIDER & RAZAKE TRADING</div>', unsafe_allow_html=True)

TELEGRAM_TOKEN = "9206676062:AAHxMkW31LJsb3jiPdALejr9fy_Nx_XH82A"
TELEGRAM_CHAT_ID = "-1003911614530"

def send_telegram_alert(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        st.error(f"Telegram Error: {e}")

def calculate_obv(df):
    return (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()

def fetch_data(symbol, period, interval):
    ticker_symbol = symbol
    if symbol == "XAUUSD": ticker_symbol = "GC=F"
    elif symbol == "XAGUSD": ticker_symbol = "SI=F"
    elif symbol == "USOIL": ticker_symbol = "CL=F"
    elif symbol == "BTCUSD": ticker_symbol = "BTC-USD"
    elif symbol == "ETHUSD": ticker_symbol = "ETH-USD"
    elif symbol == "SOLUSD": ticker_symbol = "SOL-USD"
    elif symbol == "BNBUSD": ticker_symbol = "BNB-USD"
    elif symbol == "XRPUSD": ticker_symbol = "XRP-USD"
    elif symbol == "ADAUSD": ticker_symbol = "ADA-USD"
    elif symbol == "DOGEUSD": ticker_symbol = "DOGE-USD"
    elif symbol == "EURUSD": ticker_symbol = "EURUSD=X"
    elif symbol == "GBPUSD": ticker_symbol = "GBPUSD=X"
    elif symbol == "USDJPY": ticker_symbol = "USDJPY=X"
    elif symbol == "USDCAD": ticker_symbol = "USDCAD=X"
    elif symbol == "AUDUSD": ticker_symbol = "AUDUSD=X"
    elif symbol == "NZDUSD": ticker_symbol = "NZDUSD=X"
    elif symbol == "USDCHF": ticker_symbol = "USDCHF=X"
    elif symbol == "EURGBP": ticker_symbol = "EURGBP=X"
    elif symbol == "EURJPY": ticker_symbol = "EURJPY=X"
    elif symbol == "GBPJPY": ticker_symbol = "GBPJPY=X"
    
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(period=period, interval=interval)
    return df

def analyze_smc(df):
    if len(df) < 50: return None
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    df['SMA200'] = df['Close'].rolling(window=200).mean()
    df['OBV'] = calculate_obv(df)
    df['OBV_MA'] = df['OBV'].rolling(window=20).mean()
    
    last_close = df['Close'].iloc[-1]
    sma50 = df['SMA50'].iloc[-1]
    sma200 = df['SMA200'].iloc[-1]
    obv = df['OBV'].iloc[-1]
    obv_ma = df['OBV_MA'].iloc[-1]
    
    fvg_type = None
    if len(df) >= 3:
        if df['Low'].iloc[-1] > df['High'].iloc[-3]: fvg_type = "Bullish FVG"
        elif df['High'].iloc[-1] < df['Low'].iloc[-3]: fvg_type = "Bearish FVG"

    structure = "عرضي"
    signal = "NEUTRAL"
    if last_close > sma50 and sma50 > sma200 and obv > obv_ma:
        structure = "BOS صاعد"
        signal = "BUY"
    elif last_close < sma50 and sma50 < sma200 and obv < obv_ma:
        structure = "BOS هابط"
        signal = "SELL"
        
    return {"price": last_close, "structure": structure, "signal": signal, "fvg": fvg_type or "لا يوجد", "obv_status": "سيولة صاعدة" if obv > obv_ma else "سيولة هابطة"}

st.sidebar.header("لوحة التحكم")
symbol = st.sidebar.selectbox("اختر الزوج:", ["XAUUSD", "XAGUSD", "USOIL", "EURUSD", "GBPUSD", "USDJPY", "USDCAD", "AUDUSD", "NZDUSD", "USDCHF", "EURGBP", "EURJPY", "GBPJPY", "BTCUSD", "ETHUSD", "SOLUSD", "BNBUSD", "XRPUSD", "ADAUSD", "DOGEUSD", "AAPL", "TSLA", "MSFT", "AMZN", "GOOGL", "META", "NVDA"])
timeframe = st.sidebar.selectbox("الإطار الزمني:", ["1m", "3m", "5m", "15m", "1h", "4h", "1d", "1wk", "1mo", "3mo", "6mo", "1y"])

period = "5d" if timeframe in ["1m", "3m", "5m", "15m"] else "1mo"
data = fetch_data(symbol, period=period, interval=timeframe)

tab1, tab2, tab3 = st.tabs(["التحليل المباشر", "حاسبة المخاطر", "معلومات"])

with tab1:
    if not data.empty:
        results = analyze_smc(data)
        if results:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("السعر", f"${results['price']:.2f}")
            col2.metric("الإشارة", results['signal'])
            col3.metric("OBV", results['obv_status'])
            col4.metric("FVG", results['fvg'])
            
            st.markdown("---")
            st.subheader(f"شارت TradingView لـ {symbol}")
            tv_symbol = symbol
            if symbol == "XAUUSD": tv_symbol = "OANDA:XAUUSD"
            elif symbol == "XAGUSD": tv_symbol = "OANDA:XAGUSD"
            elif symbol == "EURUSD": tv_symbol = "FX:EURUSD"
            elif symbol == "GBPUSD": tv_symbol = "FX:GBPUSD"
            elif symbol == "BTCUSD": tv_symbol = "BINANCE:BTCUSDT"
            elif symbol == "ETHUSD": tv_symbol = "BINANCE:ETHUSDT"
            elif symbol == "SOLUSD": tv_symbol = "BINANCE:SOLUSDT"
            elif symbol == "BNBUSD": tv_symbol = "BINANCE:BNBUSDT"
            elif symbol == "XRPUSD": tv_symbol = "BINANCE:XRPUSDT"
            elif symbol == "ADAUSD": tv_symbol = "BINANCE:ADAUSDT"
            elif symbol == "DOGEUSD": tv_symbol = "BINANCE:DOGEUSDT"
            
            tv_html = f'<iframe src="https://s.tradingview.com/widgetembed/?symbol={tv_symbol}&interval=5&theme=dark&style=1&locale=ar" width="100%" height="500" frameborder="0" allowtransparency="true" scrolling="no"></iframe>'
            components.html(tv_html, height=520)
            
            st.markdown("---")
            col_info, _ = st.columns([1, 1])
            with col_info:
                st.write(f"**هيكل السوق:** {results['structure']}")
                entry = results['price']
                if results['signal'] == "BUY":
                    sl, tp1, tp2, tp3, tp4 = entry - 5.0, entry + 5.0, entry + 10.0, entry + 15.0, entry + 20.0
                else:
                    sl, tp1, tp2, tp3, tp4 = entry + 5.0, entry - 5.0, entry - 10.0, entry - 15.0, entry - 20.0
                    
                st.write(f"🛑 **وقف الخسارة:** `{sl:.2f}` (5$)")
                st.write(f"🎯 **الهدف 1:** `{tp1:.2f}` (5$)")
                st.write(f"🎯 **الهدف 2:** `{tp2:.2f}` (10$)")
                st.write(f"🎯 **الهدف 3:** `{tp3:.2f}` (15$)")
                st.write(f"🎯 **الهدف 4:** `{tp4:.2f}` (20$)")
                
                if st.button("📲 إرسال التقرير لتليجرام"):
                    msg = f"🌟 *GOLDRIDER AI* 🌟\n\n📈 *الزوج:* {symbol}\n🔹 *الإشارة:* `{results['signal']}`\n💰 *الدخول:* `{entry:.2f}`\n🛑 *الستوب:* `{sl:.2f}` (5$)\n🎯 *الأهداف:* `{tp1:.2f}` | `{tp2:.2f}` | `{tp3:.2f}` | `{tp4:.2f}`\n\n📌 *ملاحظة:* يتم تأمين الصفقة عند +5$."
                    send_telegram_alert(msg)
                    st.success("تم الإرسال إلى تيليجرام بنجاح!")
        else:
            st.warning("بيانات غير كافية لحساب المؤشرات. جرب إطاراً زمنياً أكبر.")
    else:
        st.error("تعذر جلب البيانات. جرب زوجاً آخر أو إطاراً زمنياً مختلفاً.")

with tab2:
    st.subheader("حاسبة إدارة المخاطر")
    balance = st.number_input("رأس المال ($)", value=1000.0)
    risk = st.number_input("نسبة المخاطرة (%)", value=1.0)
    entry_price = st.number_input("سعر الدخول", value=2000.0)
    sl_price = st.number_input("سعر وقف الخسارة", value=1995.0)
    if entry_price != sl_price:
        risk_amount = balance * (risk / 100)
        lot_size = risk_amount / abs(entry_price - sl_price)
        st.metric("حجم العقد المناسب", f"{lot_size:.2f}")

with tab3:
    st.info("تطبيق SMART TRADING AI - GOLDRIDER & RAZAKE TRADING")
    st.write("**الأهداف:** 4 أهداف (5$، 10$، 15$، 20$).")
    st.write("**وقف الخسارة:** 5$.")
    st.write("**التأمين:** عند +5$ (نقل الوقف للدخول).")
    st.write("**الأصول المدعومة:** جميع أزواج الفوركس، الأسهم، السلع، والعملات الرقمية.")
