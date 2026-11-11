import streamlit as st
import requests

# إعداد الصفحة وتصميم الواجهة
st.set_page_config(
    page_title="SMART TRADING AI - GOLDRIDER", 
    page_icon="📈", 
    layout="centered"
)

# تخصيص التصميم والألوان (Dark Cyber Theme)
st.markdown("""
<style>
    .stApp { background-color: #080c14; color: #e2e8f0; }
    h1, h2, h3 { color: #ffd700 !important; }
    .stButton>button { background-color: #ffd700; color: #080c14; font-weight: bold; border-radius: 8px; width: 100%; }
    .stButton>button:hover { background-color: #d4af37; color: #000; }
    div.stMetric { background-color: #0e1726; border: 1px solid #1e293b; padding: 10px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# بيانات التوكن والمعرف (Chat ID) الجديدة الخاصة بك
TELEGRAM_TOKEN = "9206676062:AAHkdzTn8zCbk2Of4gmGbr6GvyBasER1gOw"
TELEGRAM_CHAT_ID = "-1003911614530"
OWNER_CODE = "011989"

# التحقق من تسجيل الدخول (كود المالك)
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align: center;'>🔐 منطقة محمية - GOLDRIDER</h2>", unsafe_allow_html=True)
    pass_input = st.text_input("أدخل كود المالك (011989):", type="password")
    if st.button("دخول البوت"):
        if pass_input == OWNER_CODE:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ كلمة السر غير صحيحة!")
    st.stop()

# الواجهة الرئيسية بعد تسجيل الدخول
st.markdown("<h1 style='text-align: center;'>🔥 SMART TRADING AI - GOLDRIDER & RAZAKE TRADING 🔥</h1>", unsafe_allow_html=True)
st.success("✅ مرحباً بك يا مالك البوت! لوحة التحكم جاهزة لإرسال التوصيات.")

# اختيار الزوج وسعر السوق
col1, col2 = st.columns(2)
with col1:
    asset = st.selectbox("اختر الزوج:", ["XAUUSD (الذهب)", "XAGUSD (الفضة)", "BTCUSDT", "ETHUSDT", "EURUSD"])
with col2:
    current_price = st.number_input("سعر السوق الحالي:", value=4001.79, step=0.01)

st.divider()

# حساب الأهداف ووقف الخسارة
st.markdown("### 📊 مستويات الصفقة والأهداف")
sl = current_price - 10.00
tp1 = current_price + 5.00
tp2 = current_price + 10.00
tp3 = current_price + 15.00
tp4 = current_price + 20.00

m1, m2, m3 = st.columns(3)
m1.metric("سعر الدخول (Entry)", f"{current_price:.2f}")
m2.metric("وقف الخسارة (SL -10$)", f"{sl:.2f}")
m3.metric("الهدف النهائي (+20$)", f"{tp4:.2f}")

c1, c2, c3, c4 = st.columns(4)
c1.info(f"TP1 (+5$)\n\n{tp1:.2f}")
c2.info(f"TP2 (+10$)\n\n{tp2:.2f}")
c3.info(f"TP3 (+15$)\n\n{tp3:.2f}")
c4.info(f"TP4 (+20$)\n\n{tp4:.2f}")

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

# أزرار التحكم وإرسال الإشعارات
st.markdown("### 🚀 أزرار التحكم وإرسال التنبيهات للقناة")

b1, b2, b3 = st.columns(3)
if b1.button("إرسال الدخول 🚀"):
    msg = (
        f"🚀 <b>إشارة دخول صفقة جديدة!</b>\n\n"
        f"🔹 <b>الزوج:</b> {asset}\n"
        f"📊 <b>الاتجاه:</b> BUY (شراء)\n"
        f"🎯 <b>سعر الدخول:</b> <code>{current_price:.2f}</code>\n"
        f"🛑 <b>وقف الخسارة (SL -10$):</b> <code>{sl:.2f}</code>\n\n"
        f"📌 <b>الأهداف المستهدفة (+20$ إجمالي):</b>\n"
        f"▪️ TP1 (+5$): <code>{tp1:.2f}</code>\n"
        f"▪️ TP2 (+10$): <code>{tp2:.2f}</code>\n"
        f"▪️ TP3 (+15$): <code>{tp3:.2f}</code>\n"
        f"▪️ TP4 (+20$): <code>{tp4:.2f}</code>\n\n"
        f"⭐ <b>مصداقية الصفقة:</b> ⭐⭐⭐⭐⭐ (99.8%)\n"
        f"👑 <i>GOLDRIDER & RAZAKE TRADING</i>"
    )
    send_tg(msg)

if b2.button("إغلاق يدوي 🔒"):
    msg = (
        f"🔒 <b>إغلاق يدوي للصفقة</b>\n\n"
        f"🔹 <b>الزوج:</b> {asset}\n"
        f"⚠️ تم إغلاق الصفقة يدوياً لحجز الأرباح أو تقليل المخاطر.\n"
        f"👑 <i>GOLDRIDER & RAZAKE TRADING</i>"
    )
    send_tg(msg)

if b3.button("ضرب الاستوب 🛑"):
    msg = (
        f"🛑 <b>تنبيه: تم ضرب وقف الخسارة (SL) (-10$)</b>\n\n"
        f"🔹 <b>الزوج:</b> {asset}\n"
        f"⚠️ تم الخروج بحماية رأس المال لضمان استمرار الأرباح.\n"
        f"👑 <i>GOLDRIDER & RAZAKE TRADING</i>"
    )
    send_tg(msg)

st.markdown("#### 💥 إشعارات تحقيق الأهداف (BOOM)")
p1, p2, p3, p4 = st.columns(4)
if p1.button("BOOM TP1 💥"):
    send_tg(f"💥 <b>BOOM! تم تحقيق الهدف 1 بنجاح!</b> 🎯\n🔹 <b>الزوج:</b> {asset}\n✅ <b>السعر:</b> <code>{tp1:.2f}</code>\n💰 <b>الربح:</b> +5$\n👑 <i>GOLDRIDER</i>")
if p2.button("BOOM TP2 💥"):
    send_tg(f"💥 <b>BOOM! تم تحقيق الهدف 2 بنجاح!</b> 🎯\n🔹 <b>الزوج:</b> {asset}\n✅ <b>السعر:</b> <code>{tp2:.2f}</code>\n💰 <b>الربح:</b> +10$\n👑 <i>GOLDRIDER</i>")
if p3.button("BOOM TP3 💥"):
    send_tg(f"💥 <b>BOOM! تم تحقيق الهدف 3 بنجاح!</b> 🎯\n🔹 <b>الزوج:</b> {asset}\n✅ <b>السعر:</b> <code>{tp3:.2f}</code>\n💰 <b>الربح:</b> +15$\n👑 <i>GOLDRIDER</i>")
if p4.button("BOOM TP4 💥"):
    send_tg(f"💥 <b>BOOM! تم تحقيق الهدف 4 بنجاح!</b> 🎯\n🔹 <b>الزوج:</b> {asset}\n✅ <b>السعر:</b> <code>{tp4:.2f}</code>\n💰 <b>الربح:</b> +20$\n👑 <i>GOLDRIDER</i>")
