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
    .stApp { background-color: #080c14; color: #e2e8f0; font-size: 11px; }
    h1 { color: #ffd700 !important; text-align: center; font-size: 16px !important; margin-bottom: 2px; }
    h2 { color: #ffd700 !important; text-align: center; font-size: 14px !important; }
    h3, h4 { color: #ffd700 !important; text-align: center; font-size: 12px !important; }
    .stButton>button { background-color: #ffd700; color: #080c14; font-weight: bold; border-radius: 6px; width: 100%; font-size: 10px; padding: 3px; min-height: 28px; }
    .stButton>button:hover { background-color: #d4af37; color: #000; }
    div.stMetric { background-color: #0e1726; border: 1px solid #1e293b; padding: 3px; border-radius: 6px; text-align: center; font-size: 10px; }
    .gold-box { background-color: #0e1726; border: 1px solid #ffd700; padding: 6px; border-radius: 8px; margin-bottom: 6px; font-size: 10px; }
    .info-card { background-color: #0e1726; border: 1px solid #1e293b; padding: 6px; border-radius: 8px; margin-bottom: 6px; font-size: 10px; }
    p, li, span, label { font-size: 10px !important; }
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
    st.info(f"⏳ معاينة مجانية متبقي: {remaining // 60}د و {remaining % 60}ث. (الصفقات وأزرار الإرسال مخفية في وضع المعاينة)")

# نبذة تعريفية ومميزات القناة
with st.expander("📌 مميزات القناة والأصول المتاحة"):
    st.markdown("""
    <div class="info-card">
    <b>توصيات يومية دقيقة باستخدام:</b> Smart Money Concept (SMC) | العرض والطلب | فيبوناتشي | الدعوم والمقاومات.<br>
    ⭐ <b>المميزات:</b> دقة +85% | توصيات مباشرة | 3-5 توصيات يومياً | إدارة رأس مال ودعم طوال الأسبوع.<br>
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

# خريطة الأصول المستخرجة من صورتك مع رموز TradingView
assets_dict = {
    "BTCUSD (بتكوين / دولار أمريكي)": {"tv": "BINANCE:BTCUSDT", "price": 74445.0},
    "GOLD (الذهب / دولار أمريكي / أونصة)": {"tv": "OANDA:XAUUSD", "price": 3996.99},
    "EURUSD (يورو / دولار أمريكي)": {"tv": "FX:EURUSD", "price": 1.1092},
    "GBPUSD (جنيه إسترليني / دولار أمريكي)": {"tv": "FX:GBPUSD", "price": 1.3274},
    "USOIL (عقود الفروقات للنفط الخام)": {"tv": "TVC:USOIL", "price": 87.17},
    "USDJPY (دولار أمريكي / ين ياباني)": {"tv": "FX:USDJPY", "price": 159.87},
    "AAPL (Apple Inc)": {"tv": "NASDAQ:AAPL", "price": 354.66},
    "TSLA (Tesla, Inc.)": {"tv": "NASDAQ:TSLA", "price": 392.51},
    "SPX500 (مؤشر ستاندرد آند بورز 500)": {"tv": "OANDA:SPX500USD", "price": 7634.8},
    "SPX (ستاندرد آند بورز 500)": {"tv": "FOREXCOM:SPXUSD", "price": 7634.81}
}

# اختيار الزوج وسعر السوق بشكل أفقي
col_a1, col_a2 = st.columns(2)
with col_a1:
    asset = st.selectbox("اختر الزوج:", list(assets_dict.keys()))
with col_a2:
    default_p = assets_dict[asset]["price"]
    current_price = st.number_input("السعر الحالي:", value=default_p, step=0.01)

st.divider()

# خاصية تحليل السوق وتحليل الصفقة (أفقية ومضغوطة)
st.markdown("### 🔍 تحليل السوق وتحليل الصفقة")
col_ana1, col_ana2 = st.columns(2)
with col_ana1:
    market_trend = st.selectbox("الاتجاه العام:", ["صاعد قوي (Bullish)", "هابط قوي (Bearish)", "عرضي (Consolidation)"])
with col_ana2:
    strategy_mode = st.selectbox("استراتيجية الدخول:", ["SMC & Order Block", "العرض والطلب", "كلاسيكي ودعوم"])

ana_btn1, ana_btn2 = st.columns(2)
with ana_btn1:
    if st.button("📊 فحص السوق"):
        st.success(f"✅ الاتجاه ({market_trend}) يدعم الصفقات إيجابياً.")
with ana_btn2:
    if st.button("🔬 فحص الصفقة"):
        st.info(f"🔍 نسبة المخاطرة ممتازة مع اللوت ({st.session_state.lot_val}).")

st.divider()

# منصة TradingView
st.markdown("### 📊 منصة TradingView")
tv_symbol = assets_dict[asset]["tv"]
tv_html = f"""
<div class="tradingview-widget-container" style="height:300px;width:100%;">
  <div id="tradingview_widget" style="height:100%;width:100%"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget({{
    "width": "100%", "height": 300, "symbol": "{tv_symbol}", "interval": "5",
    "timezone": "Etc/UTC", "theme": "dark", "style": "1", "locale": "ar",
    "toolbar_bg": "#f1f3f6", "enable_publishing": false, "allow_symbol_change": true,
    "container_id": "tradingview_widget"
  }});
  </script>
</div>
"""
st.components.v1.html(tv_html, height=310)

st.divider()

# 🔒 قسم الصفقات وتحليل المخاطر (مخفي للزوار في وضع المعاينة ويظهر للمالك فقط)
if st.session_state.authenticated:
    st.markdown("### 🧮 حاسبة المخاطر والأهداف الأربعة (خاص بالمالك)")
    sl = current_price - 10.00
    tp1 = current_price + 5.00
    tp2 = current_price + 10.00
    tp3 = current_price + 15.00
    tp4 = current_price + 20.00

    m1, m2, m3 = st.columns(3)
    m1.metric("دخول", f"{current_price:.2f}")
    m2.metric("وقف (-10$)", f"{sl:.2f}")
    m3.metric("الهدف النهائي (20$)", f"{tp4:.2f}")

    c1, c2, c3, c4 = st.columns(4)
    c1.info(f"TP1 (+5$)\n{tp1:.2f}")
    c2.info(f"TP2 (+10$)\n{tp2:.2f}")
    c3.info(f"TP3 (+15$)\n{tp3:.2f}")
    c4.info(f"TP4 (+20$)\n{tp4:.2f}")

    st.info("🛡️ **التأمين:** يتم نقل الستوب لنقطة الدخول فور تحقيق الهدف الأول (+5$).")

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

    # أزرار التحكم وإرسال التنبيهات (أفقية متجاورة بالكامل)
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
                f"🛡️ <i>تأمين الصفقة بعد TP1 (+5$)</i>\n"
                f"👑 <i>GOLDRIDER & RAZAKE TRADING</i>"
            )
            send_tg(msg)

    with b_col2:
        if st.button("اختبار 🧪"):
            send_tg(f"🧪 <b>اختبار النظام</b>\n🔹 <b>الزوج:</b> {asset}\n🎯 <b>السعر:</b> <code>{current_price:.2f}</code>")

    with b_col3:
        if st.button("إغلاق يدوي 🔒"):
            send_tg(f"🔒 <b>إغلاق يدوي</b>\n🔹 <b>الزوج:</b> {asset}")

    with b_col4:
        if st.button("ضرب الاستوب 🛑"):
            send_tg(f"🛑 <b>تنبيه وقف الخسارة (-10$)</b>\n🔹 <b>الزوج:</b> {asset}")

    st.markdown("#### 💥 أزرار الـ BOOM (أفقية)")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        if st.button("BOOM TP1 💥"):
            send_tg(f"💥 <b>تحقيق الهدف 1!</b> 🎯\n🔹 {asset} | السعر: <code>{tp1:.2f}</code> | الربح: +5$\n🛡️ <b>تم تفعيل التأمين</b>")
    with p2:
        if st.button("BOOM TP2 💥"):
            send_tg(f"💥 <b>تحقيق الهدف 2!</b> 🎯\n🔹 {asset} | السعر: <code>{tp2:.2f}</code> | الربح: +10$")
    with p3:
        if st.button("BOOM TP3 💥"):
            send_tg(f"💥 <b>تحقيق الهدف 3!</b> 🎯\n🔹 {asset} | السعر: <code>{tp3:.2f}</code> | الربح: +15$")
    with p4:
        if st.button("BOOM TP4 💥"):
            send_tg(f"💥 <b>تحقيق الهدف 4 والأخير!</b> 🎯\n🔹 {asset} | السعر: <code>{tp4:.2f}</code> | الإجمالي: +20$")
else:
    st.info("🔒 **حاسبة الصفقات وأزرار الإرسال مخفية في وضع المعاينة المجانية.** تظهر هذه الخيارات حصرياً لمالك البوت بعد تسجيل الدخول بررمز المرور.")
