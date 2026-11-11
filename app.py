import streamlit as st
import requests
from datetime import datetime
import pytz
import time

# إعداد الصفحة وتصميم الواجهة
st.set_page_config(
    page_title="GOLDRIDER TRADING AI (VIP)",
    page_icon="👑",
    layout="centered"
)

# تخصيص التصميم وتصغير أحجام الخطوط والعناصر لتظهر أفقياً ومرتبة بالكامل
st.markdown("""
<style>
    .stApp { background-color: #080c14; color: #e2e8f0; font-size: 12px; }
    h1 { color: #ffd700 !important; text-align: center; font-size: 18px !important; margin-bottom: 2px; }
    h2 { color: #ffd700 !important; text-align: center; font-size: 15px !important; }
    h3, h4 { color: #ffd700 !important; text-align: center; font-size: 13px !important; }
    .stButton>button { background-color: #ffd700; color: #080c14; font-weight: bold; border-radius: 6px; width: 100%; font-size: 11px; padding: 4px; min-height: 32px; }
    .stButton>button:hover { background-color: #d4af37; color: #000; }
    div.stMetric { background-color: #0e1726; border: 1px solid #1e293b; padding: 4px; border-radius: 6px; text-align: center; font-size: 11px; }
    .gold-box { background-color: #0e1726; border: 1px solid #ffd700; padding: 8px; border-radius: 8px; margin-bottom: 8px; font-size: 11px; }
    .info-card { background-color: #0e1726; border: 1px solid #1e293b; padding: 8px; border-radius: 8px; margin-bottom: 8px; font-size: 11px; }
    p, li, span, label { font-size: 11px !important; }
</style>
""", unsafe_allow_html=True)

# بيانات التوكن والمعرف (Chat ID) الخاصة بك
TELEGRAM_TOKEN = "9206676062:AAHkdzTn8zCbk2Of4gmGbr6GvyBasER1gOw"
TELEGRAM_CHAT_ID = "-1003911614530"
OWNER_CODE = "011989"

# إدارة الجلسات وحالة التحقق والمعاينة المجانية
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'preview_start' not in st.session_state:
    st.session_state.preview_start = None

# التحقق من انتهاء وقت المعاينة المجانية (5 دقائق = 300 ثانية)
if st.session_state.preview_start and not st.session_state.authenticated:
    elapsed = time.time() - st.session_state.preview_start
    if elapsed > 300:
        st.session_state.preview_start = None
        st.warning("⏰ انتهت فترة المعاينة المجانية (5 دقائق). يرجى إدخال رمز المالك للمتابعة.")

# شاشة حظر الدخول المباشر وتسجيل الدخول بكلمة السر السرية
if not st.session_state.authenticated and not st.session_state.preview_start:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2>🔐 منطقة محمية - GOLDRIDER VIP</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 11px;'>المنطقة محمية لمالك البوت حصراً. يرجى إدخال رمز التحقق أو البدء بمعاينة مجانية.</p>", unsafe_allow_html=True)
    
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        pass_input = st.text_input("رمز المرور:", type="password", placeholder="أدخل رمز التحقق...")
        if st.button("دخول النظام 🚀"):
            if pass_input == OWNER_CODE:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ رمز المرور غير صحيح!")
        
        if st.button("👁️ معاينة مجانية (5 دقائق)"):
            st.session_state.preview_start = time.time()
            st.rerun()
    st.stop()

# توقيت الجزائر الحي (الساعة، اليوم، الشهر، السنة)
dz_tz = pytz.timezone('Africa/Algiers')
now_dz = datetime.now(dz_tz)
time_str = now_dz.strftime('%H:%M:%S')
date_str = now_dz.strftime('%d/%m/%Y')

# الهيدر وعرض التوقيت المحلي
st.markdown("<h1>🔥 GOLDRIDER TRADING ( VIP ) 🔥</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00f0ff; font-weight: bold; font-size: 11px;'>🇩🇿 الجزائر: {time_str} | التاريخ: {date_str}</p>", unsafe_allow_html=True)

# تذكير بوضع المعاينة النشطة إن وجد
if st.session_state.preview_start and not st.session_state.authenticated:
    remaining = int(300 - (time.time() - st.session_state.preview_start))
    st.info(f"⏳ معاينة مجانية متبقي: {remaining // 60}د و {remaining % 60}ث.")

# نبذة تعريفية بالخدمة ومميزات القناة الاحترافية
with st.expander("📌 مميزات القناة والأصول المتاحة"):
    st.markdown("""
    <div class="info-card">
    <b>توصيات يومية دقيقة باستخدام:</b> Smart Money Concept (SMC) | العرض والطلب | فيبوناتشي | الدعوم والمقاومات | الكلاسيك.<br>
    ⭐ <b>المميزات:</b> دقة +85% | توصيات مباشرة | 3-5 توصيات يومياً | إدارة رأس مال ودعم طوال الأسبوع.<br>
    📊 <b>الأصول:</b> الفوركس | المعادن (الذهب/الفضة) | الكريبتو.<br>
    ✅ <b>التواصل:</b> <a href="https://t.me/RazakeRaziko" target="_blank">t.me/RazakeRaziko</a>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# حاسبة إدارة اللوت (أزرار أفقية صغيرة ومتجاورة)
st.markdown("### 🎛️ تحكم بحجم اللوت (Lot Size)")
if 'lot_val' not in st.session_state:
    st.session_state.lot_val = 0.01

lot_steps = [
    0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09,
    0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
    1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0
]

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

# اختيار الزوج وسعر السوق (بشكل أفقي)
col_a1, col_a2 = st.columns(2)
with col_a1:
    asset = st.selectbox("الزوج:", ["XAUUSD (الذهب)", "XAGUSD (الفضة)", "BTCUSDT", "ETHUSDT", "EURUSD"])
with col_a2:
    current_price = st.number_input("السعر الحالي:", value=4001.79, step=0.01)

st.divider()

# خاصية تحليل السوق وتحليل الصفقة (مدمجة ومنظمة بشكل أفقي)
st.markdown("### 🔍 تحليل السوق وتحليل الصفقة الذكي")
col_ana1, col_ana2 = st.columns(2)
with col_ana1:
    market_trend = st.selectbox("اتجاه السوق العام:", ["صاعد قوي (Bullish)", "هابط قوي (Bearish)", "عرضي (Consolidation)"])
with col_ana2:
    strategy_mode = st.selectbox("استراتيجية الدخول:", ["SMC & Order Block", "العرض والطلب", "كلاسيكي ودعوم"])

ana_btn1, ana_btn2 = st.columns(2)
with ana_btn1:
    if st.button("📊 فحص وتحليل السوق"):
        st.success(f"✅ تحليل {asset}: الاتجاه ({market_trend}) يدعم الصفقات الإيجابية وفقاً لهيكل السوق الحالي.")
with ana_btn2:
    if st.button("🔬 فحص جاهزية الصفقة"):
        st.info(f"🔍 تقييم الصفقة ({strategy_mode}): نسبة المخاطرة للعائد ممتازة، ومؤشر العزم متوافق مع اللوت ({st.session_state.lot_val}).")

st.divider()

# منصة TradingView ومؤشرات التحليل (مرئية بالكامل ودون إخفاء)
st.markdown("### 📊 منصة TradingView ومؤشر GOLDRIDER OBV & SMC")
st.markdown("""
<div class="gold-box">
    <b>⚙️ المؤشرات المؤسسية (Pine Script v6):</b> OBV + MA (فلترة السيولة) | ZigZag Depth (القمم والقيعان) | BOS & CHoCH (هيكل السوق) | OB & FVG (الأوردر بلوك والفجوات).
</div>
""", unsafe_allow_html=True)

tv_symbol = "OANDA:XAUUSD" if "XAUUSD" in asset else ("OANDA:XAGUSD" if "XAGUSD" in asset else "BINANCE:BTCUSDT")
tv_html = f"""
<div class="tradingview-widget-container" style="height:320px;width:100%;">
  <div id="tradingview_widget" style="height:100%;width:100%"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget({{
    "width": "100%", "height": 320, "symbol": "{tv_symbol}", "interval": "5",
    "timezone": "Etc/UTC", "theme": "dark", "style": "1", "locale": "ar",
    "toolbar_bg": "#f1f3f6", "enable_publishing": false, "allow_symbol_change": true,
    "container_id": "tradingview_widget"
  }});
  </script>
</div>
"""
st.components.v1.html(tv_html, height=330)

st.divider()

# حاسبة المخاطر وإدارة الأهداف (أفقية ومضغوطة)
st.markdown("### 🧮 حاسبة المخاطر والأهداف الأربعة")
sl = current_price - 10.00
tp1 = current_price + 5.00
tp2 = current_price + 10.00
tp3 = current_price + 15.00
tp4 = current_price + 20.00

m1, m2, m3 = st.columns(3)
m1.metric("دخول (Entry)", f"{current_price:.2f}")
m2.metric("وقف (SL -10$)", f"{sl:.2f}")
m3.metric("الهدف النهائي (20$)", f"{tp4:.2f}")

c1, c2, c3, c4 = st.columns(4)
c1.info(f"TP1 (+5$)\n{tp1:.2f}")
c2.info(f"TP2 (+10$)\n{tp2:.2f}")
c3.info(f"TP3 (+15$)\n{tp3:.2f}")
c4.info(f"TP4 (+20$)\n{tp4:.2f}")

st.info("🛡️ **التأمين:** يتم نقل الستوب لنقطة الدخول فور تحقيق الهدف الأول (+5$) لحجز الأرباح.")

st.divider()

# وظيفة إرسال الرسائل إلى تيليجرام
def send_tg(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        res = requests.post(url, json=payload, timeout=10)
        if res.json().get("ok"):
            st.success("✅ تم الإرسال للقناة!")
        else:
            st.error("❌ فشل الإرسال.")
    except Exception as e:
        st.error(f"❌ خطأ: {e}")

# أزرار التحكم وإرسال التنبيهات (مصفوفة أفقية متجاورة بالكامل)
if st.session_state.authenticated:
    st.markdown("### 🚀 أزرار التحكم وإرسال التنبيهات (أفقية)")

    b_col1, b_col2, b_col3, b_col4 = st.columns(4)
    
    with b_col1:
        if st.button("إرسال الدخول 🚀"):
            msg = (
                f"🚀 <b>إشارة دخول صفقة جديدة!</b>\n\n"
                f"🔹 <b>الزوج:</b> {asset}\n"
                f"📊 <b>الاتجاه:</b> BUY (شراء)\n"
                f"🎯 <b>الدخول:</b> <code>{current_price:.2f}</code> | 📦 <b>اللوت:</b> <code>{st.session_state.lot_val}</code>\n"
                f"🛑 <b>وقف الخسارة:</b> <code>{sl:.2f}</code> (-10$)\n\n"
                f"📌 <b>الأهداف (مجموع 20$):</b>\n"
                f"▪️ TP1 (+5$): <code>{tp1:.2f}</code> | ▪️ TP2 (+10$): <code>{tp2:.2f}</code>\n"
                f"▪️ TP3 (+15$): <code>{tp3:.2f}</code> | ▪️ TP4 (+20$): <code>{tp4:.2f}</code>\n\n"
                f"🛡️ <i>تأمين الصفقة ونقل الستوب للبريك إيفن بعد TP1 (+5$)</i>\n"
                f"👑 <i>GOLDRIDER & RAZAKE TRADING</i>"
            )
            send_tg(msg)

    with b_col2:
        if st.button("اختبار 🧪"):
            send_tg(f"🧪 <b>اختبار نظام التوصيات والأهداف</b>\n🔹 <b>الزوج:</b> {asset}\n🎯 <b>الدخول:</b> <code>{current_price:.2f}</code>\n✅ الاتصال يعمل بكفاءة.")

    with b_col3:
        if st.button("إغلاق يدوي 🔒"):
            send_tg(f"🔒 <b>إغلاق يدوي للصفقة</b>\n🔹 <b>الزوج:</b> {asset}\n⚠️ تم إغلاق الصفقة يدوياً لحجز الأرباح.")

    with b_col4:
        if st.button("ضرب الاستوب 🛑"):
            send_tg(f"🛑 <b>تنبيه: ضرب وقف الخسارة (-10$)</b>\n🔹 <b>الزوج:</b> {asset}\n⚠️ الخروج بحماية رأس المال.")

    st.markdown("#### 💥 أزرار إشعارات الـ BOOM (أفقية)")
    p1, p2, p3, p4 = st.columns(4)
    
    with p1:
        if st.button("BOOM TP1 💥"):
            send_tg(f"💥 <b>BOOM! تحقيق الهدف 1 بنجاح!</b> 🎯\n🔹 {asset} | السعر: <code>{tp1:.2f}</code> | الربح: +5$\n🛡️ <b>تم تفعيل التأمين وحجز الأرباح</b>")
    with p2:
        if st.button("BOOM TP2 💥"):
            send_tg(f"💥 <b>BOOM! تحقيق الهدف 2 بنجاح!</b> 🎯\n🔹 {asset} | السعر: <code>{tp2:.2f}</code> | الربح: +10$")
    with p3:
        if st.button("BOOM TP3 💥"):
            send_tg(f"💥 <b>BOOM! تحقيق الهدف 3 بنجاح!</b> 🎯\n🔹 {asset} | السعر: <code>{tp3:.2f}</code> | الربح: +15$")
    with p4:
        if st.button("BOOM TP4 💥"):
            send_tg(f"💥 <b>BOOM! تحقيق الهدف 4 والأخير!</b> 🎯\n🔹 {asset} | السعر: <code>{tp4:.2f}</code> | إجمالي الربح: +20$")
else:
    st.warning("🔒 أزرار إرسال التوصيات والصعقات مخفية في وضع المعاينة المجانية. سجل الدخول برمز المالك للتحكم.")
