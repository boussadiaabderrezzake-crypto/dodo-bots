import time
import requests
from datetime import datetime
import zoneinfo  # متاح تلقائياً في Python 3.9+

# ================= ================= =================
#  إعدادات تيليجرام وتوثيق الحساب
# ================= ================= =================
TELEGRAM_TOKEN = "9206676062:AAHkdzTn8zCbk2Of4gmGbr6GvyBasER1gOw"
TELEGRAM_CHAT_ID = "-1003911614530"
OWNER_CODE = "011989"

# ================= ================= =================
#  قائمة الأصول والعملات والبيانات الأساسية
# ================= ================= =================
ASSETS = {
    "XAUUSD": {"name": "الذهب XAU/USD", "base": 4001.79, "dec": 2},
    "XAGUSD": {"name": "الفضة XAG/USD", "base": 31.50, "dec": 3},
    "BTCUSDT": {"name": "BTC/USDT", "base": 95000.00, "dec": 2},
    "ETHUSDT": {"name": "ETH/USDT", "base": 2700.00, "dec": 2},
    "EURUSD": {"name": "EUR/USD", "base": 1.08500, "dec": 5},
    "GBPUSD": {"name": "GBP/USD", "base": 1.27000, "dec": 5},
    "USDJPY": {"name": "USD/JPY", "base": 152.000, "dec": 3},
    "AAPL": {"name": "Apple", "base": 230.00, "dec": 2},
    "TSLA": {"name": "Tesla", "base": 250.00, "dec": 2},
}

# ================= ================= =================
#  الدوال الأساسية للمحرك والتحليل
# ================= ================= =================


def get_algeria_time():
    """إرجاع توقيت الجزائر الحالي بتنسيق دقيق"""
    try:
        dz_tz = zoneinfo.ZoneInfo("Africa/Algiers")
        now = datetime.now(dz_tz)
        return now.strftime("%Y-%m-%d | %H:%M:%S")
    except Exception:
        return datetime.now().strftime("%Y-%m-%d | %H:%M:%S")


def send_telegram_message(text: str) -> bool:
    """إرسال رسالة إلى قناة التيليجرام عبر Bot API"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        res_data = response.json()
        if res_data.get("ok"):
            print("✅ تم إرسال الإشعار إلى قناة التيليجرام بنجاح!")
            return True
        else:
            print(
                f"❌ فشل إرسال الإشعار: {res_data.get('description', 'خطأ غير معروف')}"
            )
            return False
    except Exception as e:
        print(f"❌ خطأ في الاتصال بالشبكة: {e}")
        return False


def calculate_trade_levels(symbol: str, current_price: float, direction: str = "BUY"):
    """حساب سعر الدخول، الستوب لوز (-10$) والأهداف الـ4 (+5$ لكل هدف)"""
    dec = ASSETS.get(symbol, {}).get("dec", 2)

    entry = round(current_price, dec)

    if direction.upper() == "BUY":
        sl = round(entry - 10.00, dec)
        tp1 = round(entry + 5.00, dec)
        tp2 = round(entry + 10.00, dec)
        tp3 = round(entry + 15.00, dec)
        tp4 = round(entry + 20.00, dec)
    else:  # SELL
        sl = round(entry + 10.00, dec)
        tp1 = round(entry - 5.00, dec)
        tp2 = round(entry - 10.00, dec)
        tp3 = round(entry - 15.00, dec)
        tp4 = round(entry - 20.00, dec)

    return {
        "entry": entry,
        "sl": sl,
        "tp1": tp1,
        "tp2": tp2,
        "tp3": tp3,
        "tp4": tp4,
        "direction": direction.upper(),
    }


# ================= ================= =================
#  دوال إرسال التوصيات والتنبيهات
# ================= ================= =================


def send_entry_signal(symbol: str, current_price: float, direction: str = "BUY"):
    """إرسال صفقة جديدة إلى القناة"""
    asset_name = ASSETS.get(symbol, {}).get("name", symbol)
    levels = calculate_trade_levels(symbol, current_price, direction)

    msg = (
        f"🚀 <b>إشارة دخول صفقة جديدة!</b>\n\n"
        f"🔹 <b>الزوج:</b> {asset_name}\n"
        f"📊 <b>الاتجاه:</b> {levels['direction']}\n"
        f"🎯 <b>سعر الدخول:</b> <code>{levels['entry']}</code>\n"
        f"🛑 <b>وقف الخسارة (SL -10$):</b> <code>{levels['sl']}</code>\n\n"
        f"📌 <b>الأهداف المستهدفة (+20$ إجمالي):</b>\n"
        f"▪️ TP1 (+5$): <code>{levels['tp1']}</code>\n"
        f"▪️ TP2 (+10$): <code>{levels['tp2']}</code>\n"
        f"▪️ TP3 (+15$): <code>{levels['tp3']}</code>\n"
        f"▪️ TP4 (+20$): <code>{levels['tp4']}</code>\n\n"
        f"⭐ <b>مصداقية الصفقة:</b> ⭐⭐⭐⭐⭐ (99.8%)\n"
        f"🕒 <b>التوقيت:</b> <code>🇩🇿 {get_algeria_time()}</code>\n"
        f"👑 <i>GOLDRIDER & RAZAKE TRADING</i>"
    )
    return send_telegram_message(msg)


def send_boom_alert(symbol: str, current_price: float, tp_num: int, direction: str = "BUY"):
    """إرسال إشعار BOOM عند تحقيق أحد الأهداف الأربعة"""
    asset_name = ASSETS.get(symbol, {}).get("name", symbol)
    levels = calculate_trade_levels(symbol, current_price, direction)

    tp_price = levels.get(f"tp{tp_num}")
    profit_map = {1: "5$", 2: "10$", 3: "15$", 4: "20$"}
    profit_amount = profit_map.get(tp_num, "5$")

    msg = (
        f"💥 <b>BOOM! تم تحقيق الهدف {tp_num} بنجاح!</b> 🎯\n\n"
        f"🔹 <b>الزوج:</b> {asset_name}\n"
        f"✅ <b>السعر المستهدف:</b> <code>{tp_price}</code>\n"
        f"💰 <b>الربح المحقق:</b> +{profit_amount}\n\n"
        f"⭐ <i>GOLDRIDER & RAZAKE TRADING</i>"
    )
    return send_telegram_message(msg)


def send_sl_alert(symbol: str):
    """إرسال إشعار عند ضرب وقف الخسارة"""
    asset_name = ASSETS.get(symbol, {}).get("name", symbol)
    msg = (
        f"🛑 <b>تنبيه: تم ضرب وقف الخسارة (SL) (-10$)</b>\n\n"
        f"🔹 <b>الزوج:</b> {asset_name}\n"
        f"⚠️ تم الخروج بحماية رأس المال لضمان استمرار الأرباح.\n"
        f"👑 <i>GOLDRIDER & RAZAKE TRADING</i>"
    )
    return send_telegram_message(msg)


def send_manual_close_alert(symbol: str):
    """إرسال إشعار الإغلاق اليدوي"""
    asset_name = ASSETS.get(symbol, {}).get("name", symbol)
    msg = (
        f"🔒 <b>إغلاق يدوي للصفقة</b>\n\n"
        f"🔹 <b>الزوج:</b> {asset_name}\n"
        f"⚠️ تم إغلاق الصفقة يدوياً لحجز الأرباح أو تقليل المخاطر.\n"
        f"👑 <i>GOLDRIDER & RAZAKE TRADING</i>"
    )
    return send_telegram_message(msg)


def test_telegram_connection():
    """دالة اختبار الاتصال بالقناة"""
    msg = (
        f"🤖 <b>اختبار البوت ناجح!</b>\n"
        f"نظام GOLDRIDER & RAZAKE TRADING يعمل الآن بنجاح على سيرفر Python."
    )
    return send_telegram_message(msg)


# ================= ================= =================
#  القائمة الرئيسية والتفاعل عبر الكونسول
# ================= ================= =================
def main():
    print("=" * 60)
    print("   SMART TRADING AI - GOLDRIDER & RAZAKE TRADING (PYTHON)")
    print("=" * 60)

    # التحقق من كود المالك
    password = input("🔑 أدخل كود المالك للدخول: ").strip()
    if password != OWNER_CODE:
        print("❌ كلمة السر غير صحيحة! تم رفض الدخول.")
        return

    print(f"\n✅ مرحباً بك يا مالك البوت! (توقيت الجزائر: {get_algeria_time()})\n")

    current_symbol = "XAUUSD"
    current_price = ASSETS[current_symbol]["base"]

    while True:
        print("\n--------------------------------------------------")
        print(
            f"📌 الزوج الحالي: {ASSETS[current_symbol]['name']} | السعر الحالي: {current_price}"
        )
        print("--------------------------------------------------")
        print("1. إرسال صفقة جديدة (BUY) 🚀")
        print("2. إرسال إشعار BOOM TP1 💥 (+5$)")
        print("3. إرسال إشعار BOOM TP2 💥 (+10$)")
        print("4. إرسال إشعار BOOM TP3 💥 (+15$)")
        print("5. إرسال إشعار BOOM TP4 💥 (+20$)")
        print("6. إرسال إغلاق يدوي 🔒")
        print("7. إرسال إشعار ضرب الاستوب (SL) 🛑 (-10$)")
        print("8. تحديث سعر السوق الحالي ✏️")
        print("9. تغيير زوج التداول 💱")
        print("10. اختبار الاتصال بالقناة 📡")
        print("0. خروج ❌")

        choice = input("\nاختر رقماً من القائمة: ").strip()

        if choice == "1":
            send_entry_signal(current_symbol, current_price, "BUY")
        elif choice in ["2", "3", "4", "5"]:
            tp_index = int(choice) - 1
            send_boom_alert(current_symbol, current_price, tp_index, "BUY")
        elif choice == "6":
            send_manual_close_alert(current_symbol)
        elif choice == "7":
            send_sl_alert(current_symbol)
        elif choice == "8":
            try:
                new_price = float(
                    input("أدخل سعر السوق الحالي المناسب لمنصتك: ").strip()
                )
                current_price = new_price
                print(f"✅ تم تحديث السعر إلى: {current_price}")
            except ValueError:
                print("❌ خطأ: يرجى إدخال رقم صحيح.")
        elif choice == "9":
            print("\nالأصول المتاحة:")
            for k in ASSETS.keys():
                print(f"- {k}")
            sym = input("أدخل رمز الزوج (مثل XAUUSD): ").strip().upper()
            if sym in ASSETS:
                current_symbol = sym
                current_price = ASSETS[sym]["base"]
                print(f"✅ تم التغيير إلى {ASSETS[sym]['name']}")
            else:
                print("❌ الزوج غير موجود في القائمة.")
        elif choice == "10":
            test_telegram_connection()
        elif choice == "0":
            print("تم إغلاق البوت. بالتوفيق!")
            break
        else:
            print("اختيار غير صحيح، حاول مرة أخرى.")


if __name__ == "__main__":
    main()
