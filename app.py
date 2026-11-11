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

# تخصيص التصميم والألوان والتحكم بالأزرار الأفقية (Dark Cyber Theme)
st.markdown("""
<style>
    .stApp { background-color: #080c14; color: #e2e8f0; }
    h1, h2, h3, h4 { color: #ffd700 !important; text-align: center; }
    .stButton>button { background-color: #ffd700; color: #080c14; font-weight: bold; border-radius: 8px; width: 100%; }
    .stButton>button:hover { background-color: #d4af37; color: #000; }
    div.stMetric { background-color: #0e1726; border: 1px solid #1e293b; padding: 10px; border-radius: 10px; text-align: center; }
    .gold-box { background-color: #0e1726; border: 1px solid #ffd700; padding: 15px; border-radius: 12px; margin-bottom: 15px; }
    .info-card { background-color: #0e1726; border: 1px solid #1e293b; padding: 15px; border-radius: 12px; margin-bottom: 15px; font-size: 13px; }
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
    st.markdown("<p style='text-align: center; color: #94a3b8;'>المنطقة محمية لمالك البوت حصراً. يرجى إدخال رمز التحقق أو البدء بمعاينة مجانية.</p>", unsafe_allow_html=True)
    
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
st.markdown(f"<p style='text-align: center; color: #00f0ff; font-weight: bold;'>🇩🇿 التوقيت المحلي بالجزائر: {time_str} | التاريخ: {date_str}</p>", unsafe_allow_html=True)

# تذكير بوضع المعاينة النشطة إن وجد
if st.session_state.preview_start and not st.session_state.authenticated:
    remaining = int(300 - (time.time() - st.session_state.preview_start))
    st.info(f"⏳ أنت في وضع المعاينة المجانية. الوقت المتبقي: {remaining // 60} دقيقة و {remaining % 60} ثانية. (أزرار التوصيات وإدارة الصفقات مخفية في المعاينة)")

# نبذة تعريفية بالخدمة ومميزات القناة الاحترافية
with st.expander("📌 اضغط هنا لعرض مميزات القناة والأصول المتاحة"):
    st.markdown("""
    <div class="info-card">
    <b>توصيات تداول يومية دقيقة مبنية على تحليل احترافي متكامل باستخدام:</b><br>
    ✅ Smart Money Concept (SMC)<br>
    ✅ العرض والطلب (Supply & Demand)<br>
    ✅ فيبوناتشي (Fibonacci)<br>
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
    💱 الفوركس | 🥇 المعادن (الذهب – الفضة) | 🪙 الكريبتو والعملات الرقمية<br><br>
    📌 <b>هدفنا:</b> تحقيق تداول منضبط، تقليل المخاطر، وزيادة الأرباح بخطة واضحة واحترافية.<br>
    ✅ <b>للانضمام تواصل معي على تيليجرام:</b> <a href="https://t.me/RazakeRaziko" target="_blank">t.me/RazakeRaziko</a>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# حاسبة إدارة اللوت (من 0.01 إلى 0.09 ثم 0.1 إلى 0.9 ثم 1 إلى 10 مع أزرار الزائد والناقص)
st.markdown("### 🎛️ لوحة التحكم بحجم اللوت (Lot Size Controller)")
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
    if st.button("➖ خفض اللوت"):
        if current_lot_idx > 0:
            st.session_state.lot_val = lot_steps[current_lot_idx - 1]
with l_col2:
    st.markdown(f"<h3 style='text-align: center; color: #ffd700; margin:0;'>حجم اللوت: {st.session_state.lot_val}</h3>", unsafe_allow_html=True)
with l_col3:
    if st.button("➕ رفع اللوت"):
        if current_lot_idx < len(lot_steps) - 1:
            st.session_state.lot_val = lot_steps[current_lot_idx + 1]

st.divider()

# اختيار الزوج وسعر السوق
col1, col2 = st.columns(2)
with col1:
    asset = st.selectbox("اختر زوج التداول:", ["XAUUSD (الذهب)", "XAGUSD (الفضة)", "BTCUSDT", "ETHUSDT", "EURUSD"])
with col2:
    current_price = st.number_input("سعر السوق الحالي:", value=4001.79, step=0.01)

# منطقة استخراج مؤشرات TradingView الاحترافية وتحليل السوق (GOLDRIDER OBV & SMC Confluence)
st.markdown("### 📊 منصة TradingView وتحليل السوق (GOLDRIDER OBV & SMC)")
st.markdown("""
<div class="gold-box">
    <h4>⚙️ تفاصيل استخراج المؤشرات المؤسسية (Pine Script v6):</h4>
    <ul>
        <li>📈 <b>مؤشر العزم الحجمي (OBV + MA):</b> فلترة السيولة الحقيقية المضافة أو المسحوبة من السوق.</li>
        <li>⚡ <b>الزيج زاق (ZigZag Depth):</b> تحديد القمم والقيعان الحقيقية وهيكلة الاتجاه العام.</li>
        <li>🔄 <b>BOS & CHoCH:</b> رصد كسر الهيكل وتغيير الشخصية والانعكاس اللحظي.</li>
        <li>📦 <b>الأوردر بلوك والفجوات (OB & FVG):</b> تحديد الشموع المؤسسية والاختلالات السعرية لإعادة الاختبار.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# تضمين شارت TradingView تفاعلي دون إخفاء
tv_symbol = "OANDA:XAUUSD" if "XAUUSD" in asset else ("OANDA:XAGUSD" if "XAGUSD" in asset else "BINANCE:BTCUSDT")
tv_html = f"""
<div class="tradingview-widget-container" style="height:420px;width:100%;">
  <div id="tradingview_widget" style="height:100%;width:100%"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget(
  {{
    "width": "100%",
    "height": 420,
    "symbol": "{tv_symbol}",
    "interval": "5",
    "timezone": "Etc/UTC",
    "theme": "dark",
    "style": "1",
    "locale": "ar",
    "toolbar_bg": "#f1f3f6",
    "enable_publishing": false,
    "allow_symbol_change": true,
    "container_id": "tradingview_widget"
  }});
  </script>
</div>
"""
st.components.v1.html(tv_html, height=430)

st.divider()

# حاسبة المخاطر وإدارة الأهداف (كل هدف 5$, إجمالي الأهداف 20$, وقف الخسارة 10$, وتأمين الأرباح بعد 5$)
st.markdown("### 🧮 حاسبة المخاطر وإدارة الأهداف الأربعة (Risk Management & 4 TPs)")
sl = current_price - 10.00
tp1 = current_price + 5.00
tp2 = current_price + 10.00
tp3 = current_price + 15.00
tp4 = current_price + 20.00

m1, m2, m3 = st.columns(3)
m1.metric("سعر الدخول (Entry)", f"{current_price:.2f}")
m2.metric("وقف الخسارة (SL -10$)", f"{sl:.2f}")
m3.metric("الهدف النهائي (TP4 - مجموع 20$)", f"{tp4:.2f}")

c1, c2, c3, c4 = st.columns(4)
c1.info(f"TP1 (+5$)\n\n{tp1:.2f}")
c2.info(f"TP2 (+10$)\n\n{tp2:.2f}")
c3.info(f"TP3 (+15$)\n\n{tp3:.2f}")
c4.info(f"TP4 (+20$)\n\n{tp4:.2f}")

st.info("🛡️ **خاصية تأمين الأرباح:** يتم نقل وقف الخسارة إلى نقطة الدخول (Break-Even / تأمين البريك إيفن) فور تحقيق الهدف الأول (+5$) لحجز الأرباح وضمان صفر مخاطرة.")

st.divider()

# وظيفة إرسال الرسائل إلى تيليجرام
def send_tg(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        res = requests.post(url, json=payload, timeout=10)
        if res.json().get("ok"):
            st.success("✅ تم إرسال الإشعار إلى القناة بنجاح!")
        else:
            st.error("❌ فشل إرسال الإشعار عبر التيليجرام.")
    except Exception as e:
        st.error(f"❌ خطأ في الاتصال: {e}")

# أزرار التحكم وإرسال الإشعارات للقناة (متاحة لمالك النظام المتحقق فقط)
if st.session_state.authenticated:
    st.markdown("### 🚀 أزرار التحكم وإرسال التنبيهات للقناة (أفقية)")

    # الصف الأول: أزرار التحكم الرئيسية (إرسال الدخول، إغلاق يدوي، ضرب الاستوب، اختبار الصفقة)
    b_col1, b_col2, b_col3, b_col4 = st.columns(4)
    
    with b_col1:
        if st.button("إرسال الدخول 🚀"):
            msg = (
                f"🚀 <b>إشارة دخول صفقة جديدة!</b>\n\n"
                f"🔹 <b>الزوج:</b> {asset}\n"
                f"📊 <b>الاتجاه:</b> BUY (شراء)\n"
                f"🎯 <b>نقطة الدخول:</b> <code>{current_price:.2f}</code>\n"
                f"📦 <b>حجم اللوت:</b> <code>{st.session_state.lot_val}</code>\n"
                f"🛑 <b>وقف الخسارة (SL):</b> <code>{sl:.2f}</code> (-10$)\n\n"
                f"📌 <b>الأهداف المستهدفة (مجموع 20$):</b>\n"
                f"▪️ TP1 (+5$): <code>{tp1:.2f}</code>\n"
                f"▪️ TP2 (+10$): <code>{tp2:.2f}</code>\n"
                f"▪️ TP3 (+15$): <code>{tp3:.2f}</code>\n"
                f"▪️ TP4 (+20$): <code>{tp4:.2f}</code>\n\n"
                f"🛡️ <i>سيتم تأمين الصفقة ونقل الستوب للبريك إيفن بعد تحقيق الهدف الأول (+5$)</i>\n"
                f"⭐ <b>مصداقية الصفقة:</b> ⭐⭐⭐⭐⭐ (99.8%)\n"
                f"🇩🇿 <b>التوقيت المحلي:</b> {time_str} | {date_str}\n"
                f"👑 <i>GOLDRIDER & RAZAKE TRADING</i>"
            )
            send_tg(msg)

    with b_col2:
        if st.button("اختبار الصفقة 🧪"):
            test_msg = (
                f"🧪 <b>اختبار نظام التوصيات والأهداف</b>\n\n"
                f"🔹 <b>الزوج:</b> {asset}\n"
                f"🎯 <b>نقطة الدخول التجريبية:</b> <code>{current_price:.2f}</code>\n"
                f"✅ الاتصال بقناة التيليجرام يعمل بكفاءة تامة.\n"
                f"👑 <i>GOLDRIDER VIP BOT</i>"
            )
            send_tg(test_msg)

    with b_col3:
        if st.button("إغلاق يدوي 🔒"):
            msg = (
                f"🔒 <b>إغلاق يدوي للصفقة</b>\n\n"
                f"🔹 <b>الزوج:</b> {asset}\n"
                f"⚠️ تم إغلاق الصفقة يدوياً لحجز الأرباح أو تقليل المخاطر.\n"
                f"👑 <i>GOLDRIDER & RAZAKE TRADING</i>"
            )
            send_tg(msg)

    with b_col4:
        if st.button("ضرب الاستوب 🛑"):
            msg = (
                f"🛑 <b>تنبيه: تم ضرب وقف الخسارة (SL) (-10$)</b>\n\n"
                f"🔹 <b>الزوج:</b> {asset}\n"
                f"⚠️ تم الخروج بحماية رأس المال لضمان استمرار الأرباح.\n"
                f"👑 <i>GOLDRIDER & RAZAKE TRADING</i>"
            )
            send_tg(msg)

    st.markdown("#### 💥 أزرار إشعارات تحقيق الأهداف (BOOM - أفقية)")
    p1, p2, p3, p4 = st.columns(4)
    
    with p1:
        if st.button("BOOM TP1 💥"):
            send_tg(f"💥 <b>BOOM! تم تحقيق الهدف الأول (TP1) بنجاح!</b> 🎯\n🔹 <b>الزوج:</b> {asset}\n✅ <b>السعر:</b> <code>{tp1:.2f}</code>\n💰 <b>الربح المحقق:</b> +5$\n🛡️ <b>تم تفعيل التأمين وحجز الأرباح (نقل الستوب لنقطة الدخول)</b>\n👑 <i>GOLDRIDER</i>")
    with p2:
        if st.button("BOOM TP2 💥"):
            send_tg(f"💥 <b>BOOM! تم تحقيق الهدف الثاني (TP2) بنجاح!</b> 🎯\n🔹 <b>الزوج:</b> {asset}\n✅ <b>السعر:</b> <code>{tp2:.2f}</code>\n💰 <b>الربح المحقق:</b> +10$\n👑 <i>GOLDRIDER</i>")
    with p3:
        if st.button("BOOM TP3 💥"):
            send_tg(f"💥 <b>BOOM! تم تحقيق الهدف الثالث (TP3) بنجاح!</b> 🎯\n🔹 <b>الزوج:</b> {asset}\n✅ <b>السعر:</b> <code>{tp3:.2f}</code>\n💰 <b>الربح المحقق:</b> +15$\n👑 <i>GOLDRIDER</i>")
    with p4:
        if st.button("BOOM TP4 💥"):
            send_tg(f"💥 <b>BOOM! تم تحقيق الهدف الرابع والأخير (TP4) بنجاح!</b> 🎯\n🔹 <b>الزوج:</b> {asset}\n✅ <b>السعر:</b> <code>{tp4:.2f}</code>\n💰 <b>إجمالي الربح:</b> +20$\n👑 <i>GOLDRIDER</i>")
else:
    st.warning("🔒 أزرار إرسال التوصيات وإدارة الصفقات مخفية في وضع المعاينة المجانية. يرجى تسجيل الدخول برمز المالك للتحكم الكامل.")
