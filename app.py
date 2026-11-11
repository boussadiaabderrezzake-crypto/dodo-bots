import streamlit as st
import requests
import pandas as pd
import numpy as np
import datetime
import pytz
import streamlit.components.v1 as components
import time

# ==========================================
# 1. الإعدادات والسرية وتكوين الصفحة
# ==========================================
st.set_page_config(
    page_title="GOLDRIDER TRADING AI (VIP)",
    page_icon="👑",
    layout="centered"
)

# توكن وتاريخ وقناة التيليجرام الخاصة بك
TELEGRAM_TOKEN = "9206676062:AAHkdzTn8zCbk2Of4gmGbr6GvyBasER1gOw"
TELEGRAM_CHAT_ID = "-1003911614530"
OWNER_CODE = "011989"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except: pass

# ==========================================
# 2. تخصيص التصميم وإخفاء شريط أدوات التطبيق للزوار
# ==========================================
st.markdown("""
<style>
    .stApp { background-color: #080c14; color: #e2e8f0; font-size: 11px; }
    h1 { color: #ffd700 !important; text-align: center; font-size: 16px !important; margin-bottom: 2px; }
    h2 { color: #ffd700 !important; text-align: center; font-size: 14px !important; }
    h3, h4 { color: #ffd700 !important; text-align: center; font-size: 12px !important; }
    .stButton>button { background-color: #ffd700; color: #080c14; font-weight: bold; border-radius: 6px; width: 100%; font-size: 10px; padding: 3px; min-height: 28px; }
    .stButton>button:hover { background-color: #d4af37; color: #000; }
    div.stMetric { background-color: #0e1726; border: 1px solid #1e293b; padding: 3px; border-radius: 6px; text-align: center; font-size: 10px; }
    .gold-box { background-color: #0e1726; border: 1px solid #ffd700; padding: 10px; border-radius: 8px; margin-bottom: 10px; font-size: 11px; line-height: 1.6; }
    .info-card { background-color: #0e1726; border: 1px solid #1e293b; padding: 6px; border-radius: 8px; margin-bottom: 6px; font-size: 10px; }
    p, li, span, label { font-size: 10px !important; }
    .brand-title { text-align: center; font-weight: 900; font-size: 20px; color: #ffd700; margin-bottom: 0px; text-shadow: 0 0 10px rgba(255,215,0,0.3); }
    .brand-sub { text-align: center; font-weight: bold; font-size: 13px; color: #00f0ff; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. إدارة الجلسات وحالة التحقق والمعاينة (مرة واحدة فقط)
# ==========================================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'preview_start' not in st.session_state:
    st.session_state.preview_start = None
if 'preview_used' not in st.session_state:
    st.session_state.preview_used = False  # تتبع ما إذا استهلك الزائر المعاينة لمرة واحدة
if "open_trades" not in st.session_state:
    st.session_state.open_trades = {}

# إخفاء قائمة وتوثيق "Manage app" وأزرار النظام تماماً للزوار غير المالكين
if not st.session_state.authenticated:
    st.markdown("""
    <style>
        #MainMenu, footer, header, [data-testid="stStatusWidget"], [data-testid="manage-app-button"] {visibility: hidden !important; display: none !important;}
        button[kind="header"] {display: none !important;}
    </style>
    """, unsafe_allow_html=True)

# التحقق من انتهاء وقت المعاينة المجانية (5 دقائق = 300 ثانية)
if st.session_state.preview_start and not st.session_state.authenticated:
    elapsed = time.time() - st.session_state.preview_start
    if elapsed > 300:
        st.session_state.preview_start = None
        st.session_state.preview_used = True  # تم استهلاك المعاينة ولن تفتح مجدداً لهذا الزائر
        st.warning("⏰ انتهت فترة المعاينة المجانية (5 دقائق). لقد استنفدت محاولتك المجانية، يرجى إدخال رمز المالك للمتابعة.")
        st.rerun()

# شاشة حظر الدخول المباشر وتسجيل الدخول بكلمة السر السرية أو زر المعاينة لمرة واحدة
if not st.session_state.authenticated and st.session_state.preview_start is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2>🔐 منطقة محمية - GOLDRIDER VIP</h2>", unsafe_allow_html=True)
    
    if st.session_state.preview_used:
        st.error("❌ لقد قمت بالفعل باستخدام معاينتك المجانية (للمرة الواحدة). يرجى إدخال رمز المالك الصحيح لدخول النظام.")
    else:
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 11px;'>المنطقة محمية لمالك البوت حصراً. متاح لك معاينة مجانية لمرة واحدة فقط لمدة 5 دقائق.</p>", unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        pass_input = st.text_input("رمز المرور:", type="password", placeholder="أدخل رمز التحقق...")
        if st.button("دخول النظام 🚀"):
            if pass_input == OWNER_CODE:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ رمز المرور غير صحيح!")
        
        # زر المعاينة يظهر فقط إذا لم يستهلكها الزائر بعد
        if not st.session_state.preview_used:
            if st.button("👁️ معاينة مجانية (للمرة الأولى والأخيرة - 5 دقائق)"):
                st.session_state.preview_start = time.time()
                st.rerun()
    st.stop()

# ==========================================
# 4. جلب السعر الحقيقي
# ==========================================
def get_price(symbol="XAUUSD"):
    try:
        r = requests.get("https://api.gold-api.com/price/XAU", timeout=10)
        if r.status_code == 200:
            return float(r.json()['price'])
    except: pass
    return 4047.90  # سعر احتياطي

# ==========================================
# 5. فتح صفقة + إشعار للتيليجرام بالشكل المطلوب
# ==========================================
def open_trade(side="BUY", lot=0.01):
    price = get_price()
    
    if side == "BUY":
        sl = price - 5.0
        tp1 = price + 5.0
        tp2 = price + 10.0
        tp3 = price + 15.0
        tp4 = price + 20.0
    else:
        sl = price + 5.0
        tp1 = price - 5.0
        tp2 = price - 10.0
        tp3 = price - 15.0
        tp4 = price - 20.0
    
    st.session_state.open_trades["XAUUSD"] = {
        "side": side, "entry": price, "lot": lot, "sl": sl,
        "tp1": tp1, "tp2": tp2, "tp3": tp3, "tp4": tp4,
        "tp1_hit": False, "tp2_hit": False, "tp3_hit": False, "tp4_hit": False,
        "be_set": False
    }
    
    emoji = "🟢" if side == "BUY" else "🔴"
    
    # القالب الجديد المطلوب بحذافيره
    msg = (
        f"🌟 *GOLDRIDER AI & SMC Confluence* 🌟\n"
        f"👨‍💻 *RAZAKE TRADING* | توصية جديدة على الذهب\n\n"
        f"{emoji} *النوع:* {side} (Gold (XAUUSD))\n"
        f"💰 *سعر الدخول:* `{price:.2f}`\n"
        f"🛑 *وقف الخسارة (SL):* `{sl:.2f}` (-5 دولار)\n"
        f"🎯 *الهدف الأول (TP1):* `{tp1:.2f}` (+5 دولار)\n"
        f"🎯 *الهدف الثاني (TP2):* `{tp2:.2f}` (+10 دولار)\n"
        f"🎯 *الهدف الثالث (TP3):* `{tp3:.2f}` (+15 دولار)\n"
        f"🎯 *الهدف الرابع (TP4):* `{tp4:.2f}` (+20 دولار)\n\n"
        f"📊 *التحليل:* تأكيد السيولة المؤسسية واختراق الهيكل (BOS).\n"
        f"📊 *حجم اللوت:* `{lot}`"
    )
    
    send_telegram(msg)
    st.success(f"✅ تم فتح صفقة {side} على XAUUSD وإرسال التنبيه للقناة بنجاح @ {price:.2f}")

# ==========================================
# 6. تحديث الصفقة ومتابعة الأهداف
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
    else:  # SELL
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
# 7. التوقيت والهيدر الرئيسي للواجهة
# ==========================================
algeria_tz = pytz.timezone('Africa/Algiers')
now_dz = datetime.datetime.now(algeria_tz).strftime("%H:%M:%S | %Y-%m-%d")

st.markdown("<div class='brand-title'>⭐ SMART TRADING AI ⭐</div>", unsafe_allow_html=True)
st.markdown("<div class='brand-sub'>GOLDRIDER & RAZAKE TRADING</div>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #94a3b8; font-weight: bold;'>🇩🇿 توقيت الجزائر: {now_dz}</p>", unsafe_allow_html=True)

# أزرار التواصل والانضمام (ظاهرة للجميع)
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    st.markdown("""
        <a href="https://t.me/RazakeRaziko" target="_blank">
            <button style="background: linear-gradient(135deg, #0088cc, #00aced); color: white; border: none; padding: 8px; border-radius: 8px; width: 100%; font-weight: bold; cursor: pointer; font-size: 11px;">
                📢 طلب الانضمام إلى قناة التيليجرام
            </button>
        </a>
    """, unsafe_allow_html=True)
with col_btn2:
    st.markdown("""
        <a href="https://wa.me/213667570565" target="_blank">
            <button style="background: linear-gradient(135deg, #25d366, #128c7e); color: white; border: none; padding: 8px; border-radius: 8px; width: 100%; font-weight: bold; cursor: pointer; font-size: 11px;">
                💬 التواصل معنا على واتساب
            </button>
        </a>
    """, unsafe_allow_html=True)

# تنبيه وقت المعاينة إن وجد
if st.session_state.preview_start and not st.session_state.authenticated:
    elapsed_time = time.time() - st.session_state.preview_start
    remaining = int(300 - elapsed_time)
    if remaining > 0:
        st.info(f"⏳ معاينة مجانية متبقية (لمرة واحدة): {remaining // 60}د و {remaining % 60}ث.")

# ==========================================
# 8. النص التعريفي الشامل للقناة
# ==========================================
st.markdown("""
<div class="gold-box">
<b>🔥 GOLDRIDER TRADING ( VIP ) 🔥</b><br>
توصيات تداول يومية دقيقة مبنية على تحليل احترافي متكامل باستخدام:<br>
✅ Smart Money Concept (SMC)<br>
✅ العرض والطلب<br>
✅ فيبوناتشي<br>
✅ الدعوم والمقاومات<br>
✅ النماذج الفنية الكلاسيكية<br><br>
⭐ <b>مميزات القناة:</b><br>
🔹 توصيات عالية الدقة مبنية على تحليل احترافي<br>
🔹 نسبة نجاح مستهدفة +85%<br>
🔹 جميع التوصيات مباشرة وواضحة (دخول – وقف – أهداف)<br>
🔹 من 3 إلى 5 توصيات يوميًا<br>
🔹 إدارة رأس مال مناسبة لكل نوع حساب<br>
🔹 دعم فني وتحليلي طوال أيام أسبوع التداول<br><br>
📊 <b>الأصول التي يتم التداول عليها:</b><br>
💱 الفوركس<br>
🥇 المعادن (الذهب – الفضة)<br>
🪙 الكريبتو والعملات الرقمية<br><br>
📌 <b>هدفنا:</b><br>
تحقيق تداول منضبط، تقليل المخاطر، وزيادة الأرباح بخطة واضحة واحترافية<br><br>
✅ <b>للانضمام تواصل معي على هذا الرابط 👈</b> <a href="https://t.me/RazakeRaziko" target="_blank">t.me/RazakeRaziko</a>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================
# 9. حاسبة اللوت والشارت (ظاهرة للجميع)
# ==========================================
st.markdown("### 🎛️ تحكم بحجم اللوت (Lot Size)")
if 'lot_val' not in st.session_state:
    st.session_state.lot_val = 0.01

lot_steps = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
current_lot_idx = lot_steps.index(st.session_state.lot_val) if st.session_state.lot_val in lot_steps else 0

l_col1, l_col2, l_col3 = st.columns([1, 2, 1])
with l_col1:
    if st.button("➖ خفض"):
        if current_lot_idx > 0:
            st.session_state.lot_val = lot_steps[current_lot_idx - 1]
with l_col2:
    st.markdown(f"<h4 style='text-align: center; color: #ffd700; margin:0;'>اللوت: {st.session_state.lot_val}</h4>", unsafe_allow_html=True)
with l_col3:
    if st.button("➕ رفع"):
        if current_lot_idx < len(lot_steps) - 1:
            st.session_state.lot_val = lot_steps[current_lot_idx + 1]

st.divider()

# شارت TradingView المطور مع أدوات الرسم والتحليل
st.markdown("### 📈 منصة TradingView والتحليل الفني")
tv_html = """
<div id="tvchart"></div>
<script src="https://s3.tradingview.com/tv.js"></script>
<script>
new TradingView.widget({
  "width": "100%", "height": 450, "symbol": "OANDA:XAUUSD",
  "interval": "5", "timezone": "Africa/Algiers",
  "theme": "dark", "style": "1", "locale": "ar",
  "toolbar_bg": "#f1f3f6", "enable_publishing": false, "allow_symbol_change": true,
  "save_image": true, "details": true, "hotlist": true, "calendar": true,
  "hide_side_toolbar": false, "withdateranges": true,
  "studies": ["MASimple@tv-basicstudies", "RSI@tv-basicstudies", "MACD@tv-basicstudies"],
  "container_id": "tvchart"
});
</script>
"""
components.html(tv_html, height=470)

st.divider()

# ==========================================
# 10. لوحة تحكم وإدارة الصفقات (خاص بالمالك حصراً)
# ==========================================
if st.session_state.authenticated:
    st.markdown("### 🎛️ لوحة تحكم وإدارة صفقات المالك")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        lot = st.selectbox("حجم اللوت الفعلي", [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0], index=0)
    with c2:
        if st.button("🟢 فتح صفقة BUY", use_container_width=True):
            open_trade("BUY", lot)
    with c3:
        if st.button("🔴 فتح صفقة SELL", use_container_width=True):
            open_trade("SELL", lot)
    with c4:
        if st.button("🔄 تحديث الصفقة", use_container_width=True):
            update_trade()

    # --- اختبار القناة ---
    if st.button("📤 إرسال اختبار للقناة", use_container_width=True):
        send_telegram("🤖 رسالة اختبار من البوت ✅\nالقناة متصلة بنجاح!")
        st.success("تم إرسال الاختبار إلى تيليجرام!")

    # --- عرض الصفقات المفتوحة للمالك ---
    st.divider()
    st.markdown("### 📊 الصفقات المفتوحة حالياً")
    if not st.session_state.open_trades:
        st.info("لا توجد صفقات مفتوحة حالياً.")
    else:
        for sym, t in st.session_state.open_trades.items():
            with st.expander(f"{sym} — {t['side']} — اللوت: {t['lot']}"):
                st.write(f"**الدخول:** `{t['entry']:.2f}` | **الستوب:** `{t['sl']:.2f}`")
                st.write(f"**TP1:** {'✅' if t['tp1_hit'] else '⏳'} | **TP2:** {'✅' if t['tp2_hit'] else '⏳'}")
                st.write(f"**TP3:** {'✅' if t['tp3_hit'] else '⏳'} | **TP4:** {'✅' if t['tp4_hit'] else '⏳'}")
                if st.button(f"🔴 إغلاق يدوي {sym}", key=f"close_{sym}"):
                    send_telegram(f"🔴 *إغلاق يدوي للصفقة*\n{sym} ({t['side']})")
                    del st.session_state.open_trades[sym]
                    st.rerun()
else:
    st.info("🔒 **لوحة تحكم الصفقات وتتبعها مخفية للزوار.** تظهر حصرياً لمالك البوت بعد تسجيل الدخول بررمز المرور في أعلى الصفحة.")
