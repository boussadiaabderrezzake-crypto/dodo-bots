import streamlit as st
import requests
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import pytz
import streamlit.components.v1 as components

# ==========================================
# 1. الإعدادات والسرية
# ==========================================
st.set_page_config(page_title="SMART TRADING AI", layout="wide", initial_sidebar_state="expanded")

TOKEN = st.secrets.get("TELEGRAM_TOKEN")
CHAT_ID = st.secrets.get("TELEGRAM_CHAT_ID")
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD")

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
# 2. حالة التطبيق
# ==========================================
if "open_trades" not in st.session_state:
    st.session_state.open_trades = {}
open_trades = st.session_state.open_trades

if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# ==========================================
# 3. جلب البيانات
# ==========================================
def fetch_ohlcv(symbol, source, interval="5m"):
    try:
        if source == "metal":
            df = yf.Ticker("GC=F").history(period="5d", interval=interval)
            if df.empty: return None
            df = df.rename(columns={"Open":"open","High":"high","Low":"low","Close":"close","Volume":"volume"})
            return df.tail(300)
        elif source == "crypto":
            binance_int = interval.replace("d", "1d").replace("h", "1h").replace("m", "m")
            r = requests.get(f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={binance_int}&limit=300", timeout=10)
            if r.status_code != 200: return None
            raw = r.json()
            df = pd.DataFrame(raw, columns=["time","open","high","low","close","volume","ct","qav","trades","tb","tq","ig"])
            for c in ["open","high","low","close","volume"]: df[c] = df[c].astype(float)
            return df
        else:
            df = yf.Ticker(symbol).history(period="5d", interval=interval)
            if df.empty: return None
            df = df.rename(columns={"Open":"open","High":"high","Low":"low","Close":"close","Volume":"volume"})
            return df.tail(300)
    except Exception as e:
        return None

# ==========================================
# 4. جلب السعر (gold-api فقط - آمن)
# ==========================================
def get_current_price(symbol, source):
    try:
        if source == "metal":
            r = requests.get("https://api.gold-api.com/price/XAU", timeout=10)
            if r.status_code == 200:
                return float(r.json()['price'])
        elif source == "crypto":
            return float(requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}", timeout=10).json()['price'])
        elif source == "yahoo":
            df = yf.Ticker(symbol).history(period="1d", interval="1m")
            if not df.empty: return float(df['Close'].iloc[-1])
    except Exception as e:
        return None
    return None

# ==========================================
# 5. محرك التحليل
# ==========================================
def analyze_smc(df):
    if df is None or len(df) < 50: return None
    df['sma50'] = df['close'].rolling(50).mean()
    df['obv'] = (np.sign(df['close'].diff()) * df['volume']).fillna(0).cumsum()
    df['obv_ma'] = df['obv'].rolling(20).mean()
    
    last_close = df['close'].iloc[-1]
    last_sma50 = df['sma50'].iloc[-1]
    obv_val = df['obv'].iloc[-1]
    obv_ma_val = df['obv_ma'].iloc[-1]
    
    trend = "NEUTRAL"
    if last_close > last_sma50 and obv_val > obv_ma_val: trend = "BULLISH"
    elif last_close < last_sma50 and obv_val < obv_ma_val: trend = "BEARISH"
    
    return {"trend": trend, "last_close": last_close, "sma50": last_sma50}

# ==========================================
# 6. تنفيذ التحليل
# ==========================================
def execute_analysis(symbol, name, source, interval):
    df = fetch_ohlcv(symbol, source, interval)
    if df is None: return {"error": "لا توجد بيانات."}
    res = analyze_smc(df)
    if res is None: return {"error": "فشل التحليل."}
    
    live_price = get_current_price(symbol, source)
    price = live_price if live_price else res['last_close']
    trend = res['trend']
    
    if trend == "NEUTRAL":
        send_telegram(f"⏳ *تحليل السوق:* {name}\nالنتيجة: السوق متذبذب، لا توجد إشارة.")
        return {"trend": "NEUTRAL", "price": price}
    
    if trend == "BULLISH":
        sl = price - 5.0
        tp1, tp2, tp3, tp4 = price + 5.0, price + 10.0, price + 15.0, price + 20.0
        emoji = "🟢"
    else:
        sl = price + 5.0
        tp1, tp2, tp3, tp4 = price - 5.0, price - 10.0, price - 15.0, price - 20.0
        emoji = "🔴"

    msg = f"🌟 *GOLDRIDER AI (SMC)*\n"
    msg += f"{emoji} *النوع:* `{trend}` ({name})\n"
    msg += f"💰 *الدخول:* `{price:.2f}`\n"
    msg += f"🛑 *الستوب:* `{sl:.2f}` (5$)\n"
    msg += f"🎯 *TP1:* `{tp1:.2f}` (+5$)\n"
    msg += f"🎯 *TP2:* `{tp2:.2f}` (+10$)\n"
    msg += f"🎯 *TP3:* `{tp3:.2f}` (+15$)\n"
    msg += f"🏆 *TP4:* `{tp4:.2f}` (+20$)\n"
    send_telegram(msg)
    
    open_trades[symbol] = {
        'name': name, 'type': trend, 'entry': price, 'source': source,
        'sl_original': sl, 'sl': sl,
        'tp1': tp1, 'tp2': tp2, 'tp3': tp3, 'tp4': tp4,
        'tp1_hit': False, 'tp2_hit': False, 'tp3_hit': False, 'tp4_hit': False,
        'be_set': False
    }
    
    return {"trend": trend, "price": price, "sl": sl, "tp1": tp1, "tp2": tp2, "tp3": tp3, "tp4": tp4, "emoji": emoji}

# ==========================================
# 7. إدارة الصفقات
# ==========================================
def manage_trades():
    for symbol in list(open_trades.keys()):
        trade = open_trades[symbol]
        price = get_current_price(symbol, trade.get('source'))
        if price is None: continue

        if (trade['type'] == 'BULLISH' and price <= trade['sl']) or (trade['type'] == 'BEARISH' and price >= trade['sl']):
            reason = "Break-Even" if trade['be_set'] else "الستوب لوز"
            send_telegram(f"❌ *ضرب {reason}* 🛑\n{trade['name']} ({trade['type']})")
            del open_trades[symbol]
            continue

        if trade['type'] == 'BULLISH':
            if price >= trade['tp4'] and not trade['tp4_hit']:
                trade['tp4_hit'] = True
                send_telegram(f"🏆 *تحقق الهدف الرابع (TP4)!*\n{trade['name']} +20$")
                del open_trades[symbol]; continue
            elif price >= trade['tp3'] and not trade['tp3_hit']:
                trade['tp3_hit'] = True
                send_telegram(f"🎯 *تحقق الهدف الثالث (TP3)!*\n{trade['name']} +15$")
            elif price >= trade['tp2'] and not trade['tp2_hit']:
                trade['tp2_hit'] = True
                send_telegram(f"🎯 *تحقق الهدف الثاني (TP2)!*\n{trade['name']} +10$")
            elif price >= trade['tp1'] and not trade['tp1_hit']:
                trade['tp1_hit'] = True
                trade['sl'] = trade['entry']
                trade['be_set'] = True
                send_telegram(f"✅ *تحقق الهدف الأول (TP1) وتأمين!* 🔒\n{trade['name']} +5$")
        else:
            if price <= trade['tp4'] and not trade['tp4_hit']:
                trade['tp4_hit'] = True
                send_telegram(f"🏆 *تحقق الهدف الرابع (TP4)!*\n{trade['name']} +20$")
                del open_trades[symbol]; continue
            elif price <= trade['tp3'] and not trade['tp3_hit']:
                trade['tp3_hit'] = True
                send_telegram(f"🎯 *تحقق الهدف الثالث (TP3)!*\n{trade['name']} +15$")
            elif price <= trade['tp2'] and not trade['tp2_hit']:
                trade['tp2_hit'] = True
                send_telegram(f"🎯 *تحقق الهدف الثاني (TP2)!*\n{trade['name']} +10$")
            elif price <= trade['tp1'] and not trade['tp1_hit']:
                trade['tp1_hit'] = True
                trade['sl'] = trade['entry']
                trade['be_set'] = True
                send_telegram(f"✅ *تحقق الهدف الأول (TP1) وتأمين!* 🔒\n{trade['name']} +5$")

# ==========================================
# 8. الواجهة
# ==========================================
algeria_tz = pytz.timezone('Africa/Algiers')
now = datetime.datetime.now(algeria_tz).strftime("%H:%M:%S | %Y-%m-%d")

TELEGRAM_CHANNEL_URL = "https://t.me/+8hruUT1mtE1hMzc0"
WHATSAPP_URL = "https://wa.me/213667570565"

st.markdown(f"""
<style>
    .main-title {{ color: #d4af37; text-align: center; font-size: 40px; font-weight: bold; }}
    .sub-title {{ color: #00bfff; text-align: center; font-size: 20px; margin-bottom: 5px; }}
    .time-box {{ text-align: center; color: #aaa; margin-bottom: 20px; font-family: monospace; }}
    .btn-telegram {{ display: block; width: 100%; text-align: center; padding: 12px; background-color: #0088cc; color: white; font-size: 16px; font-weight: bold; border-radius: 10px; text-decoration: none; margin-bottom: 10px; }}
    .btn-whatsapp {{ display: block; width: 100%; text-align: center; padding: 12px; background-color: #25D366; color: white; font-size: 16px; font-weight: bold; border-radius: 10px; text-decoration: none; margin-bottom: 20px; }}
    .vip-card {{ background-color: #1e1e1e; border: 1px solid #d4af37; padding: 10px; border-radius: 10px; text-align: center; margin-bottom: 10px; color: white; }}
    .vip-price {{ color: #d4af37; font-size: 20px; font-weight: bold; }}
</style>
<div class="main-title">🌟 SMART TRADING AI 🌟</div>
<div class="sub-title">GOLDRIDER & RAZAKE TRADING</div>
<div class="time-box">🇩🇿 توقيت الجزائر: {now}</div>
<a href="{TELEGRAM_CHANNEL_URL}" target="_blank" class="btn-telegram">📢 طلب الانضمام إلى قناة التليجرام</a>
<a href="{WHATSAPP_URL}" target="_blank" class="btn-whatsapp">💬 التواصل معنا على واتساب</a>
""", unsafe_allow_html=True)

st.markdown("### 👑 عروض الاشتراك في قناة VIP")
vip_plans = [("شهر واحد", "30$"), ("3 أشهر", "90$"), ("6 أشهر", "120$"), ("9 أشهر", "150$"), ("سنة كاملة", "180$")]
vip_cols = st.columns(5)
for i, (plan_name, price) in enumerate(vip_plans):
    with vip_cols[i]:
        st.markdown(f"""
        <div class="vip-card">
            <strong>{plan_name}</strong><br>
            <span class="vip-price">{price}</span><br>
            <a href="{WHATSAPP_URL}" target="_blank" style="color:#25D366; font-size:14px;">اشترك الآن</a>
        </div>
        """, unsafe_allow_html=True)

st.divider()

markets = {
    "السلع (Commodities)": {"XAUUSD": "OANDA:XAUUSD", "XAGUSD": "OANDA:XAGUSD", "USOIL": "TVC:USOIL"},
    "العملات الرقمية (Crypto)": {"BTCUSDT": "BINANCE:BTCUSDT", "ETHUSDT": "BINANCE:ETHUSDT", "SOLUSDT": "BINANCE:SOLUSDT", "BNBUSDT": "BINANCE:BNBUSDT"},
    "الفوركس (Forex)": {"EURUSD": "FX:EURUSD", "GBPUSD": "FX:GBPUSD", "USDJPY": "FX:USDJPY", "AUDUSD": "FX:AUDUSD"},
    "الأسهم (Stocks)": {"AAPL": "NASDAQ:AAPL", "TSLA": "NASDAQ:TSLA", "MSFT": "NASDAQ:MSFT", "NVDA": "NASDAQ:NVDA"}
}

timeframes = {
    "1 دقيقة": "1m", "5 دقائق": "5m", "15 دقيقة": "15m", "30 دقيقة": "30m",
    "1 ساعة": "1h", "4 ساعات": "4h", "يومي": "1d"
}
tv_timeframes = {"1m":"1", "5m":"5", "15m":"15", "30m":"30", "1h":"60", "4h":"240", "1d":"D"}

col_right, col_center, col_left = st.columns([1, 2.5, 1])

with col_left:
    st.markdown("### 🧮 حاسبة المخاطر")
    capital = st.number_input("رأس المال ($)", value=1000, step=100)
    risk_pct = st.number_input("نسبة المخاطرة (%)", value=1.0, step=0.1)
    entry = st.number_input("سعر الدخول", value=4140.0)
    sl = st.number_input("وقف الخسارة", value=4135.0)
    tp = st.number_input("الهدف", value=4150.0)
    
    risk_amount = capital * (risk_pct / 100)
    sl_distance = abs(entry - sl)
    lot = round(risk_amount / sl_distance, 2) if sl_distance > 0 else 0
    rr = round(abs(tp - entry) / sl_distance, 2) if sl_distance > 0 else 0
    
    st.metric("حجم العقد", lot)
    st.metric("Risk / Reward", f"1 : {rr}")

with col_center:
    st.markdown("### 📈 الشارت المباشر (TradingView)")
    cat_selected = st.selectbox("اختر القسم:", list(markets.keys()))
    symbol_name = st.selectbox("اختر الزوج/السهم:", list(markets[cat_selected].keys()))
    tv_symbol = markets[cat_selected][symbol_name]
    
    tf_selected = st.selectbox("اختر الفريم الزمني:", list(timeframes.keys()), index=1)
    tv_timeframe = tv_timeframes[timeframes[tf_selected]]

    tv_html = f"""
    <div id="tv_chart_container"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{
      "width": "100%", "height": 600, "symbol": "{tv_symbol}",
      "interval": "{tv_timeframe}", "timezone": "Africa/Algiers",
      "theme": "dark", "style": "1", "locale": "ar",
      "container_id": "tv_chart_container"
    }});
    </script>
    """
    components.html(tv_html, height=650)

with col_right:
    st.markdown("### 🔐 لوحة المالك")
    
    if not st.session_state.is_admin:
        pwd = st.text_input("أدخل كلمة السر", type="password")
        if st.button("دخول"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.is_admin = True
                st.success("✅ تم الدخول!")
                st.rerun()
            else:
                st.error("❌ كلمة السر خاطئة")
    
    if st.session_state.is_admin:
        st.success("🔓 مرحباً بك يا مالك البوت")
        
        if st.button("🚀 تحليل السوق", use_container_width=True):
            with st.spinner("جاري التحليل..."):
                source = "crypto" if "USDT" in symbol_name else ("metal" if "XAU" in symbol_name else "yahoo")
                sym = symbol_name if source == "crypto" else ("XAU" if "XAU" in symbol_name else symbol_name)
                st.session_state.last_analysis = execute_analysis(sym, symbol_name, source, timeframes[tf_selected])

        if st.button("🔄 تحديث الصفقات (إدارة الأهداف)", use_container_width=True):
            with st.spinner("جاري تحديث الصفقات..."):
                manage_trades()
                st.success("✅ تم تحديث الصفقات!")

        if st.session_state.last_analysis:
            res = st.session_state.last_analysis
            if "error" in res:
                st.error(res["error"])
            elif res["trend"] == "NEUTRAL":
                st.warning(f"⚠️ السوق متذبذب.\nالسعر: `{res['price']:.2f}`")
            else:
                st.success(f"✅ تم التحليل وإرسال الإشارة!")
                st.write(f"**الاتجاه:** {res['emoji']} `{res['trend']}`")
                st.write(f"**السعر:** `{res['price']:.2f}`")
                st.write(f"**الستوب:** `{res['sl']:.2f}`")
                st.write(f"**TP1:** `{res['tp1']:.2f}` | **TP2:** `{res['tp2']:.2f}`")
                st.write(f"**TP3:** `{res['tp3']:.2f}` | **TP4:** `{res['tp4']:.2f}`")

        st.divider()
        st.markdown("### 📊 الصفقات المفتوحة")
        if not open_trades:
            st.info("لا توجد صفقات مفتوحة.")
        else:
            for sym, t in open_trades.items():
                with st.expander(f"{t['name']} — {t['type']}"):
                    st.write(f"الدخول: `{t['entry']:.2f}` | الستوب: `{t['sl']:.2f}`")
                    st.write(f"TP1: {'✅' if t['tp1_hit'] else '⏳'} | TP2: {'✅' if t['tp2_hit'] else '⏳'}")
                    st.write(f"TP3: {'✅' if t['tp3_hit'] else '⏳'} | TP4: {'✅' if t['tp4_hit'] else '⏳'}")
    else:
        st.info("🔒 هذه المنطقة مخصصة للمالك فقط.")
