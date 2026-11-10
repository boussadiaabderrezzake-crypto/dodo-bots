import streamlit as st
import requests
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import pytz
import plotly.graph_objects as go
import streamlit.components.v1 as components

# ==========================================
# 1. الإعدادات والسرية
# ==========================================
TOKEN = st.secrets.get("TELEGRAM_TOKEN")
CHAT_ID = st.secrets.get("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    st.error("❌ التوكن أو الـ ID غير موجودين في Secrets!")
    st.stop()

def send_telegram(msg: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        pass

# ==========================================
# 2. حالة التطبيق (حفظ الصفقات)
# ==========================================
if "open_trades" not in st.session_state:
    st.session_state.open_trades = {}
open_trades = st.session_state.open_trades

# ==========================================
# 3. جلب البيانات والتحليل
# ==========================================
def fetch_data(symbol, source):
    try:
        if source == "metal":
            df = yf.Ticker("GC=F").history(period="5d", interval="5m")
            if df.empty: return None
            df = df.rename(columns={"Open":"open","High":"high","Low":"low","Close":"close","Volume":"volume"})
            return df.tail(300)
        elif source == "crypto":
            r = requests.get(f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=5m&limit=300", timeout=10)
            if r.status_code != 200: return None
            raw = r.json()
            df = pd.DataFrame(raw, columns=["time","open","high","low","close","volume","ct","qav","trades","tb","tq","ig"])
            for c in ["open","high","low","close","volume"]: df[c] = df[c].astype(float)
            return df
    except Exception as e:
        return None

def get_current_price(symbol, source):
    try:
        if source == "metal":
            return float(requests.get(f"https://api.gold-api.com/price/{symbol}", timeout=10).json()['price'])
        elif source == "crypto":
            return float(requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}", timeout=10).json()['price'])
    except Exception as e:
        return None

def analyze_smc(df):
    if df is None or len(df) < 50: return "NEUTRAL"
    obv = (np.sign(df['close'].diff()) * df['volume']).fillna(0).cumsum()
    obv_ma = obv.rolling(20).mean()
    sma50 = df['close'].rolling(50).mean().iloc[-1]
    sma200 = df['close'].rolling(200).mean().iloc[-1]
    last_close = df['close'].iloc[-1]
    obv_val = obv.iloc[-1]
    obv_ma_val = obv_ma.iloc[-1]
    if last_close > sma50 and sma50 > sma200 and obv_val > obv_ma_val: return "BUY"
    elif last_close < sma50 and sma50 < sma200 and obv_val < obv_ma_val: return "SELL"
    return "NEUTRAL"

# ==========================================
# 4. فتح الصفقة (مرة واحدة فقط)
# ==========================================
def open_trade(symbol, name, source):
    if symbol in open_trades: return

    df = fetch_data(symbol, source)
    signal = analyze_smc(df)
    if signal == "NEUTRAL": return

    price = df['close'].iloc[-1]
    if signal == "BUY":
        sl = price - 5.0
        tp1, tp2, tp3, tp4 = price + 5.0, price + 10.0, price + 15.0, price + 20.0
        emoji = "🟢"
    else:
        sl = price + 5.0
        tp1, tp2, tp3, tp4 = price - 5.0, price - 10.0, price - 15.0, price - 20.0
        emoji = "🔴"

    open_trades[symbol] = {
        'name': name, 'type': signal, 'entry': price, 'source': source,
        'sl': sl, 'tp1': tp1, 'tp2': tp2, 'tp3': tp3, 'tp4': tp4,
        'tp1_hit': False, 'tp2_hit': False, 'tp3_hit': False, 'tp4_hit': False
    }

    msg = f"🌟 *GOLDRIDER AI & SMC*\n"
    msg += f"{emoji} *النوع:* `{signal}` ({name})\n"
    msg += f"💰 *الدخول:* `{price:.2f}`\n"
    msg += f"🛑 *الستوب لوز:* `{sl:.2f}`\n"
    msg += f"🎯 *TP1:* `{tp1:.2f}` | *TP2:* `{tp2:.2f}`\n"
    msg += f"🎯 *TP3:* `{tp3:.2f}` | *TP4:* `{tp4:.2f}`"
    send_telegram(msg)

def manage_trades():
    for symbol in list(open_trades.keys()):
        trade = open_trades[symbol]
        price = get_current_price(symbol, trade.get('source'))
        if price is None: continue

        if (trade['type'] == 'BUY' and price <= trade['sl']) or (trade['type'] == 'SELL' and price >= trade['sl']):
            send_telegram(f"❌ *ضرب الستوب لوز* 🛑\n{trade['name']} ({trade['type']})")
            del open_trades[symbol]
            continue

        if trade['type'] == 'BUY':
            if price >= trade['tp4'] and not trade['tp4_hit']:
                send_telegram(f"🏆 *تحقق الهدف الرابع (TP4)!*\n{trade['name']} +20 نقطة")
                del open_trades[symbol]; continue
            elif price >= trade['tp3'] and not trade['tp3_hit']:
                trade['tp3_hit'] = True; send_telegram(f"🎯 *تحقق الهدف الثالث (TP3)!*\n{trade['name']} +15 نقطة")
            elif price >= trade['tp2'] and not trade['tp2_hit']:
                trade['tp2_hit'] = True; send_telegram(f"🎯 *تحقق الهدف الثاني (TP2)!*\n{trade['name']} +10 نقاط")
            elif price >= trade['tp1'] and not trade['tp1_hit']:
                trade['tp1_hit'] = True; trade['sl'] = trade['entry']
                send_telegram(f"✅ *تحقق الهدف الأول (TP1) وتأمين الصفقة!* 🔒\n{trade['name']} +5 نقاط\nالستوب الآن عند الدخول.")
        else:
            if price <= trade['tp4'] and not trade['tp4_hit']:
                send_telegram(f"🏆 *تحقق الهدف الرابع (TP4)!*\n{trade['name']} +20 نقطة")
                del open_trades[symbol]; continue
            elif price <= trade['tp3'] and not trade['tp3_hit']:
                trade['tp3_hit'] = True; send_telegram(f"🎯 *تحقق الهدف الثالث (TP3)!*\n{trade['name']} +15 نقطة")
            elif price <= trade['tp2'] and not trade['tp2_hit']:
                trade['tp2_hit'] = True; send_telegram(f"🎯 *تحقق الهدف الثاني (TP2)!*\n{trade['name']} +10 نقاط")
            elif price <= trade['tp1'] and not trade['tp1_hit']:
                trade['tp1_hit'] = True; trade['sl'] = trade['entry']
                send_telegram(f"✅ *تحقق الهدف الأول (TP1) وتأمين الصفقة!* 🔒\n{trade['name']} +5 نقاط\nالستوب الآن عند الدخول.")

# ==========================================
# 5. واجهة Streamlit والتصميم
# ==========================================
st.set_page_config(page_title="SMART TRADING AI", layout="wide")

# توقيت الجزائر
algeria_tz = pytz.timezone('Africa/Algiers')
now = datetime.datetime.now(algeria_tz).strftime("%H:%M:%S | %Y-%m-%d")

# التصميم (CSS)
st.markdown(f"""
<style>
    .main-title {{ color: #d4af37; text-align: center; font-size: 40px; }}
    .sub-title {{ color: #00bfff; text-align: center; font-size: 20px; }}
    .time-box {{ text-align: center; color: #aaa; margin-bottom: 20px; }}
    .metric-box {{ background-color: #1e1e1e; padding: 15px; border-radius: 10px; margin-bottom: 10px; }}
</style>
<div class="main-title">🌟 SMART TRADING AI 🌟</div>
<div class="sub-title">GOLDRIDER & RAZAKE TRADING</div>
<div class="time-box">🇩🇿 توقيت الجزائر: {now}</div>
""", unsafe_allow_html=True)

# الأزواج والفريمات
col1, col2, col3 = st.columns(3)
with col1:
    symbol = st.selectbox("زوج التداول", ["XAUUSD", "BTCUSDT", "ETHUSDT", "EURUSD"])
with col2:
    timeframe = st.selectbox("الفريم الزمني", ["1m", "5m", "15m", "1h"])
with col3:
    st.write("")
    st.write("")
    if st.button("🚀 تحليل الأسواق الآن", use_container_width=True):
        with st.spinner("جاري التحليل وإرسال الإشارات..."):
            open_trade("XAU", "Gold (XAUUSD)", "metal")
            open_trade("BTCUSDT", "BTC/USDT", "crypto")
            manage_trades()
            st.success("✅ تم التحليل!")
            st.rerun()

# عرض الصفقات المفتوحة
st.divider()
st.subheader("📊 الصفقات المفتوحة حالياً")
if not open_trades:
    st.info("لا توجد صفقات مفتوحة حالياً. البوت ينتظر إشارة الدخول.")
else:
    for sym, t in open_trades.items():
        with st.expander(f"{t['name']} — {t['type']}"):
            st.write(f"الدخول: `{t['entry']:.2f}` | الستوب: `{t['sl']:.2f}`")

# شارت TradingView
st.divider()
st.subheader("📈 الشارت المباشر (TradingView)")
tv_symbol = "OANDA:XAUUSD" if symbol == "XAUUSD" else symbol.replace("USDT", "USD")
tv_html = f"""
<div id="tv_chart_container"></div>
<script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
<script type="text/javascript">
new TradingView.widget({{
  "width": "100%", "height": 500, "symbol": "{tv_symbol}",
  "interval": "{timeframe.replace('m','').replace('h','')}", "timezone": "Africa/Algiers",
  "theme": "dark", "style": "1", "locale": "ar",
  "container_id": "tv_chart_container"
}});
</script>
"""
components.html(tv_html, height=550)
