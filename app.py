import streamlit as st
import requests
import pandas as pd
import numpy as np
import datetime
import pytz
import streamlit.components.v1 as components
import time

# ==========================================
# 1. الإعدادات والسرية
# ==========================================
st.set_page_config(
    page_title="GOLDRIDER TRADING AI (VIP)",
    page_icon="👑",
    layout="centered"
)

# ⚠️ التوكن والآي دي الجديدين (تم التحديث)
TELEGRAM_TOKEN = "9206676062:AAHkdzTn8zCbk2Of4gmGbr6GvyBasER1gOw"
TELEGRAM_CHAT_ID = "-1003911614530"
OWNER_CODE = "011989"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except: pass

# ==========================================
# 2. التصميم
# ==========================================
st.markdown("""
<style>
    .stApp { background-color: #080c14; color: #e2e8f0; }
    h1, h2, h3, h4 { color: #ffd700 !important; text-align: center; }
    .stButton>button { background-color: #ffd700; color: #080c14; font-weight: bold; border-radius: 8px; width: 100%; }
    .gold-box { background-color: #0e1726; border: 1px solid #ffd700; padding: 15px; border-radius: 10px; margin-bottom: 15px; }
    .brand-title { text-align: center; font-weight: 900; font-size: 28px; color: #ffd700; text-shadow: 0 0 10px rgba(255,215,0,0.5); }
    .brand-sub { text-align: center; font-weight: bold; font-size: 16px; color: #00f0ff; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. الجلسات والحماية
# ==========================================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'preview_start' not in st.session_state:
    st.session_state.preview_start = None
if 'preview_used' not in st.session_state:
    st.session_state.preview_used = False
if "open_trades" not in st.session_state:
    st.session_state.open_trades = {}

# إخفاء القوائم للزوار
if not st.session_state.authenticated:
    st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden !important;}
    </style>
    """, unsafe_allow_html=True)

# التحقق من وقت المعاينة (5 دقائق)
if st.session_state.preview_start and not st.session_state.authenticated:
    elapsed = time.time() - st.session_state.preview_start
    if elapsed > 300:
        st.session_state.preview_start = None
        st.session_state.preview_used = True
        st.warning("⏰ انتهت المعاينة المجانية. يرجى إدخال رمز المالك.")
        st.rerun()

# شاشة الدخول
if not st.session_state.authenticated and st.session_state.preview_start is None:
    st.markdown("<h2>🔐 منطقة محمية - GOLDRIDER VIP</h2>", unsafe_allow_html=True)
    if st.session_state.preview_used:
        st.error("❌ استنفدت المعاينة المجانية. أدخل رمز المالك.")
    else:
        st.info("🔒 المنطقة محمية. متاح لك معاينة مجانية لمرة واحدة (5 دقائق).")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pass_input = st.text_input("رمز المرور:", type="password")
        if st.button("🚀 دخول النظام"):
            if pass_input == OWNER_CODE:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ رمز غير صحيح!")
        
        if not st.session_state.preview_used:
            if st.button("👁️ معاينة مجانية (5 دقائق)"):
                st.session_state.preview_start = time.time()
                st.rerun()
    st.stop()

# ==========================================
# 4. جلب السعر
# ==========================================
def get_price(symbol="XAUUSD"):
    try:
        r = requests.get("https://api.gold-api.com/price/XAU", timeout=10)
        if r.status_code == 200:
            return float(r.json()['price'])
    except: pass
    return 4047.90

# ==========================================
# 5. فتح صفقة + إشعار
# ==========================================
def open_trade(side="BUY", lot=0.01):
    price = get_price()
    
    if side == "BUY":
        sl = price - 5.0
        tp1, tp2, tp3, tp4 = price + 5.0, price + 10.0, price + 15.0, price + 20.0
    else:
        sl = price + 5.0
        tp1, tp2, tp3, tp4 = price - 5.0, price - 10.0, price - 15.0, price - 20.0
    
    st.session_state.open_trades["XAUUSD"] = {
        "side": side, "entry": price, "lot": lot, "sl": sl,
        "tp1": tp1, "tp2": tp2, "tp3": tp3, "tp4": tp4,
        "tp1_hit": False, "tp2_hit": False, "tp3_hit": False, "tp4_hit": False,
        "be_set": False
    }
    
    emoji = "🟢" if side == "BUY" else "🔴"
    msg = (
        f"🌟 *GOLDRIDER AI & SMC Confluence* 🌟\n"
        f"👨‍💻 *RAZAKE TRADING* | توصية جديدة\n\n"
        f"{emoji} *النوع:* {side} (XAUUSD)\n"
        f"💰 *الدخول:* `{price:.2f}`\n"
        f"🛑 *الستوب:* `{sl:.2f}` (-5$)\n"
        f"🎯 *TP1:* `{tp1:.2f}` (+5$)\n"
        f"🎯 *TP2:* `{tp2:.2f}` (+10$)\n"
        f"🎯 *TP3:* `{tp3:.2f}` (+15$)\n"
        f"🏆 *TP4:* `{tp4:.2f}` (+20$)\n"
        f"📊 *اللوت:* `{lot}`"
    )
    send_telegram(msg)
    st.success(f"✅ تم فتح صفقة {side} @ {price:.2f} وإرسال الإشعار.")

# ==========================================
# 6. تحديث الصفقة
# ==========================================
def update_trade():
    if "XAUUSD" not in st.session_state.open_trades:
        st.warning("لا توجد صفقة مفتوحة.")
        return
    
    trade = st.session_state.open_trades["XAUUSD"]
    price = get_price()
    
    if trade["side"] == "BUY":
        if price <= trade["sl"]:
            send_telegram(f"❌ *ضرب الستوب لوز* 🛑\nXAUUSD (BUY)\nالسعر: {price:.2f}")
            del st.session_state.open_trades["XAUUSD"]
            st.error("تم ضرب الستوب لوز.")
            return
        if price >= trade["tp4"]:
            send_telegram(f"🏆 *TP4 تحقق!* XAUUSD (BUY) +20$")
            del st.session_state.open_trades["XAUUSD"]
            return
        if price >= trade["tp3"] and not trade["tp3_hit"]:
            trade["tp3_hit"] = True
            send_telegram(f"🎯 *TP3 تحقق!* XAUUSD (BUY) +15$")
        if price >= trade["tp2"] and not trade["tp2_hit"]:
            trade["tp2_hit"] = True
            send_telegram(f"🎯 *TP2 تحقق!* XAUUSD (BUY) +10$")
        if price >= trade["tp1"] and not trade["tp1_hit"]:
            trade["tp1_hit"] = True
            trade["sl"] = trade["entry"]
            trade["be_set"] = True
            send_telegram(f"✅ *TP1 تحقق وتأمين!* XAUUSD (BUY) +5$\nالستوب الآن عند الدخول.")
    else:
        if price >= trade["sl"]:
            send_telegram(f"❌ *ضرب الستوب لوز* 🛑\nXAUUSD (SELL)\nالسعر: {price:.2f}")
            del st.session_state.open_trades["XAUUSD"]
            st.error("تم ضرب الستوب لوز.")
            return
        if price <= trade["tp4"]:
            send_telegram(f"🏆 *TP4 تحقق!* XAUUSD (SELL) +20$")
            del st.session_state.open_trades["XAUUSD"]
            return
        if price <= trade["tp3"] and not trade["tp3_hit"]:
            trade["tp3_hit"] = True
            send_telegram(f"🎯 *TP3 تحقق!* XAUUSD (SELL) +15$")
        if price <= trade["tp2"] and not trade["tp2_hit"]:
            trade["tp2_hit"] = True
            send_telegram(f"🎯 *TP2 تحقق!* XAUUSD (SELL) +10$")
        if price <= trade["tp1"] and not trade["tp1_hit"]:
            trade["tp1_hit"] = True
            trade["sl"] = trade["entry"]
            trade["be_set"] = True
            send_telegram(f"✅ *TP1 تحقق وتأمين!* XAUUSD (SELL) +5$\nالستوب الآن عند الدخول.")
    
    st.success(f"✅ تم التحديث. السعر الحالي: {price:.2f}")

# ==========================================
# 7. الواجهة الرئيسية
# ==========================================
algeria_tz = pytz.timezone('Africa/Algiers')
now_dz = datetime.datetime.now(algeria_tz).strftime("%H:%M:%S | %Y-%m-%d")

st.markdown("<div class='brand-title'>⭐ SMART TRADING AI ⭐</div>", unsafe_allow_html=True)
st.markdown("<div class='brand-sub'>GOLDRIDER & RAZAKE TRADING</div>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #94a3b8;'>🇩🇿 توقيت الجزائر: {now_dz}</p>", unsafe_allow_html=True)

# أزرار التواصل
col1, col2 = st.columns(2)
with col1:
    st.link_button("📢 طلب الانضمام للقناة", "https://t.me/RazakeRaziko", use_container_width=True)
with col2:
    st.link_button("💬 واتساب", "https://wa.me/213667570565", use_container_width=True)

# المعاينة
if st.session_state.preview_start and not st.session_state.authenticated:
    elapsed_time = time.time() - st.session_state.preview_start
    remaining = int(300 - elapsed_time)
    if remaining > 0:
        st.info(f"⏳ معاينة متبقية: {remaining // 60}د و {remaining % 60}ث.")

# النص التعريفي
st.markdown("""
<div class="gold-box">
<b>🔥 GOLDRIDER TRADING (VIP) 🔥</b><br>
✅ Smart Money Concept (SMC)<br>
✅ العرض والطلب<br>
✅ فيبوناتشي<br>
✅ الدعوم والمقاومات<br>
🔹 نسبة نجاح +85%<br>
🔹 3-5 توصيات يومياً<br>
🔹 دعم فني وتحليلي<br><br>
📊 <b>الأصول:</b> الفوركس، الذهب، الفضة، الكريبتو<br><br>
✅ <b>للانضمام:</b> <a href="https://t.me/RazakeRaziko" target="_blank">t.me/RazakeRaziko</a>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 8. حاسبة اللوت
# ==========================================
st.markdown("### 🎛️ حجم اللوت")
if 'lot_val' not in st.session_state:
    st.session_state.lot_val = 0.01

lot_steps = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]
idx = lot_steps.index(st.session_state.lot_val) if st.session_state.lot_val in lot_steps else 0

c1, c2, c3 = st.columns([1, 2, 1])
with c1:
    if st.button("➖"):
        if idx > 0:
            st.session_state.lot_val = lot_steps[idx - 1]
            st.rerun()
with c2:
    st.markdown(f"<h3 style='text-align:center; color:#ffd700;'>اللوت: {st.session_state.lot_val}</h3>", unsafe_allow_html=True)
with c3:
    if st.button("➕"):
        if idx < len(lot_steps) - 1:
            st.session_state.lot_val = lot_steps[idx + 1]
            st.rerun()

# ==========================================
# 9. الشارت
# ==========================================
st.markdown("### 📈 شارت TradingView")
tv_html = """
<div id="tvchart"></div>
<script src="https://s3.tradingview.com/tv.js"></script>
<script>
new TradingView.widget({
  "width": "100%", "height": 450, "symbol": "OANDA:XAUUSD",
  "interval": "5", "timezone": "Africa/Algiers",
  "theme": "dark", "style": "1", "locale": "ar",
  "hide_side_toolbar": false, "withdateranges": true,
  "studies": ["MASimple@tv-basicstudies", "RSI@tv-basicstudies", "MACD@tv-basicstudies"],
  "container_id": "tvchart"
});
</script>
"""
components.html(tv_html, height=470)

# ==========================================
# 10. لوحة المالك (التحكم)
# ==========================================
if st.session_state.authenticated:
    st.markdown("### 🎛️ لوحة تحكم المالك")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        if st.button("🟢 BUY", use_container_width=True):
            open_trade("BUY", st.session_state.lot_val)
    with c2:
        if st.button("🔴 SELL", use_container_width=True):
            open_trade("SELL", st.session_state.lot_val)
    with c3:
        if st.button("🔄 تحديث", use_container_width=True):
            update_trade()
    with c4:
        if st.button("📤 اختبار", use_container_width=True):
            send_telegram("🤖 رسالة اختبار ✅ القناة متصلة!")
            st.success("تم الإرسال!")
    
    # عرض الصفقات
    st.markdown("### 📊 الصفقات المفتوحة")
    if not st.session_state.open_trades:
        st.info("لا توجد صفقات مفتوحة.")
    else:
        for sym, t in st.session_state.open_trades.items():
            with st.expander(f"{sym} — {t['side']} — {t['lot']}"):
                st.write(f"الدخول: `{t['entry']:.2f}` | الستوب: `{t['sl']:.2f}`")
                st.write(f"TP1: {'✅' if t['tp1_hit'] else '⏳'} | TP2: {'✅' if t['tp2_hit'] else '⏳'}")
                st.write(f"TP3: {'✅' if t['tp3_hit'] else '⏳'} | TP4: {'✅' if t['tp4_hit'] else '⏳'}")
                if st.button(f"🔴 إغلاق {sym}", key=f"close_{sym}"):
                    send_telegram(f"🔴 *إغلاق يدوي* {sym} ({t['side']})")
                    del st.session_state.open_trades[sym]
                    st.rerun()
else:
    st.info("🔒 لوحة التحكم مخفية للزوار.")
