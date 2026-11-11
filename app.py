from js import Response, document
import json

# ================= ================= =================
#  إعدادات تيليجرام وتوثيق الحساب (التوكن والايدي الجديد)
# ================= ================= =================
TELEGRAM_TOKEN = "9206676062:AAHkdzTn8zCbk2Of4gmGbr6GvyBasER1gOw"
TELEGRAM_CHAT_ID = "-1003911614530"

# ================= ================= =================
#  كود واجهة الويب والمتصفح (HTML / CSS / JS) لمنع الشاشة البيضاء
# ================= ================= =================
HTML_CONTENT = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SMART TRADING AI - GOLDRIDER & RAZAKE TRADING</title>
<script src="https://cdn.tailwindcss.com"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=JetBrains+Mono:wght@700&display=swap" rel="stylesheet">
<script>
tailwind.config={theme:{extend:{colors:{gold:{500:'#ffd700',600:'#d4af37'},cyber:{blue:'#00f0ff',bg:'#080c14',panel:'#0e1726',border:'#1e293b'}},fontFamily:{sans:['Cairo','sans-serif'],mono:['JetBrains Mono','monospace']}}}}
</script>
<style>
body{background-color:#080c14;color:#e2e8f0;font-family:'Cairo',sans-serif;margin:0;padding:0}
.glow-gold{box-shadow:0 0 15px rgba(255,215,0,0.2)}
.num{font-family:'JetBrains Mono',monospace;direction:ltr;display:inline-block}
.tf-btn.active,.asset-btn.active{background-color:#ffd700!important;color:#080c14!important}
.telegram-btn{background:linear-gradient(135deg,#0088cc,#00aced);box-shadow:0 4px 15px rgba(0,172,237,0.3)}
.whatsapp-btn{background:linear-gradient(135deg,#25d366,#128c7e);box-shadow:0 4px 15px rgba(37,211,102,0.3)}
::-webkit-scrollbar{height:6px;width:6px}::-webkit-scrollbar-thumb{background:#ffd700;border-radius:4px}
#timer-bar{position:fixed;top:0;left:0;height:4px;background:#ffd700;z-index:100;transition:width 1s linear}
.toast{animation:slideIn 0.3s ease-out}@keyframes slideIn{from{transform:translateX(100%);opacity:0}to{transform:translateX(0);opacity:1}}
.lot-btn{background:#1e293b;border:1px solid #334155;color:#e2e8f0;padding:5px 14px;border-radius:8px;font-weight:bold}
.lot-btn:hover{background:#ffd700;color:#080c14}
#auth-modal.hidden{display:none!important}
.plan-card{border:1px solid #1e293b;background:#0e1726;transition:all 0.3s ease}
.plan-card.selected{border-color:#ffd700;box-shadow:0 0 15px rgba(255,215,0,0.3)}
.pay-btn.active{background:#ffd700!important;color:#080c14!important}
.analysis-locked{filter:blur(6px);pointer-events:none;user-select:none}
</style>
</head>
<body class="min-h-screen relative pb-10">
<div id="timer-bar" style="width:100%;display:none"></div>
<div id="timer-text" class="fixed top-2 left-1/2 transform -translate-x-1/2 bg-black/80 text-gold-500 px-4 py-1 rounded-full text-xs font-bold z-50 hidden shadow-lg border border-gold-500/50"><i class="fas fa-clock"></i> الوقت المتبقي للمعاينة: <span id="time-display" class="num">05:00</span></div>

<!-- واجهة كلمة السر لحماية الدخول (كود المالك 011989) -->
<div id="auth-modal" class="fixed inset-0 bg-black/95 backdrop-blur-md z-[100] flex items-center justify-center p-4">
<div class="bg-cyber-panel border border-gold-500 rounded-2xl p-6 w-full max-w-sm text-center shadow-2xl glow-gold">
<i class="fas fa-lock text-gold-500 text-4xl mb-3"></i>
<h2 class="text-lg font-black text-white mb-1">منطقة محمية - GOLDRIDER</h2>
<p class="text-xs text-gray-400 mb-4">الرجاء إدخال كود المالك (011989) للدخول ورؤية التحليل والأهداف، أو استخدام المعاينة المجانية.</p>
<input type="password" id="pass-input" placeholder="أدخل كلمة السر..." class="w-full bg-cyber-bg border border-cyber-border rounded-lg p-3 text-center text-white text-sm num mb-3 focus:border-gold-500 outline-none">
<button onclick="checkPassword()" class="w-full py-2.5 bg-gold-500 text-black font-black rounded-lg text-sm mb-2 hover:bg-gold-600 transition">دخول البوت</button>
<button onclick="startPreview()" class="w-full py-2 bg-cyber-bg border border-gold-500/50 text-gold-500 font-bold rounded-lg text-xs hover:bg-gold-500/10 transition"><i class="fas fa-eye"></i> معاينة مجانية لمدة 5 دقائق</button>
</div></div>

<header class="border-b border-cyber-border bg-cyber-panel/90 p-4 flex items-center justify-between sticky top-0 z-40">
<div class="flex items-center gap-3">
    <i class="fas fa-robot text-gold-500 text-2xl"></i>
    <div>
        <h1 class="text-sm font-black text-gold-500 leading-tight">SMART TRADING AI</h1>
        <p class="text-[9px] text-gray-400">GOLDRIDER & RAZAKE TRADING</p>
        <p class="text-[9px] text-cyber-blue num" id="algeria-time">🇩🇿 --:--:-- | --/--/----</p>
    </div>
</div>
<div class="flex items-center gap-2">
    <button onclick="testTelegram()" class="bg-blue-600 hover:bg-blue-500 text-white text-xs px-3 py-1 rounded shadow border border-blue-400">
        <i class="fab fa-telegram-plane"></i> اختبار القناة
    </button>
    <div id="sub-badge" class="bg-gold-500/20 text-gold-500 px-3 py-1 rounded text-xs font-bold border border-gold-500/50"><i class="fas fa-crown"></i> مالك البوت</div>
</div>
</header>

<main class="container mx-auto px-2 py-3 max-w-xl">

<!-- نبذة تعريفية بالخدمة -->
<div class="bg-cyber-panel border border-gold-500/40 rounded-xl p-3 mb-3 text-xs leading-relaxed">
    <h2 class="text-gold-500 font-black text-sm mb-2 text-center">🔥 GOLDRIDER TRADING ( VIP ) 🔥</h2>
    <p class="text-gray-300 mb-2 text-center">توصيات تداول يومية دقيقة مبنية على تحليل احترافي متكامل باستخدام:</p>
    <div class="grid grid-cols-2 gap-1 text-[11px] mb-2 text-gray-300">
        <div>✅ Smart Money Concept (SMC)</div>
        <div>✅ العرض والطلب</div>
        <div>✅ فيبوناتشي</div>
        <div>✅ الدعوم والمقاومات</div>
        <div class="col-span-2">✅ النماذج الفنية الكلاسيكية</div>
    </div>
    
    <div class="border-t border-cyber-border pt-2 mb-2">
        <p class="text-gold-500 font-bold mb-1"><i class="fas fa-star"></i> مميزات القناة:</p>
        <ul class="list-disc list-inside space-y-1 text-gray-300 text-[11px]">
            <li>توصيات عالية الدقة مبنية على تحليل احترافي</li>
            <li>نسبة نجاح مستهدفة +85%</li>
            <li>جميع التوصيات مباشرة وواضحة (دخول – وقف – أهداف)</li>
            <li>من 3 إلى 5 توصيات يوميًا</li>
            <li>إدارة رأس مال مناسبة لكل نوع حساب</li>
            <li>دعم فني وتحليلي طوال أيام أسبوع التداول</li>
        </ul>
    </div>

    <div class="border-t border-cyber-border pt-2 mb-2">
        <p class="text-gold-500 font-bold mb-1"><i class="fas fa-chart-bar"></i> الأصول التي يتم التداول عليها:</p>
        <div class="text-gray-300 text-[11px]">
            💱 الفوركس | 🥇 المعادن (الذهب – الفضة) | 🪙 الكريبتو والعملات الرقمية
        </div>
    </div>

    <div class="border-t border-cyber-border pt-2 text-center">
        <p class="text-cyber-blue font-bold mb-1">📌 هدفنا:</p>
        <p class="text-gray-300 text-[11px]">تحقيق تداول منضبط، تقليل المخاطر، وزيادة الأرباح بخطة واضحة واحترافية</p>
    </div>
</div>

<!-- Asset Selector -->
<div class="bg-cyber-panel border border-cyber-border rounded-xl p-2 mb-3 flex overflow-x-auto gap-2 text-xs font-bold" style="white-space:nowrap">
<button onclick="changeAsset('XAUUSD',this)" class="asset-btn active px-3 py-2 rounded-lg bg-gold-500 text-black">XAUUSD</button>
<button onclick="changeAsset('XAGUSD',this)" class="asset-btn px-3 py-2 rounded-lg bg-cyber-border text-gray-300">XAGUSD</button>
<button onclick="changeAsset('BTCUSDT',this)" class="asset-btn px-3 py-2 rounded-lg bg-cyber-border text-gray-300">BTCUSDT</button>
<button onclick="changeAsset('ETHUSDT',this)" class="asset-btn px-3 py-2 rounded-lg bg-cyber-border text-gray-300">ETHUSDT</button>
<button onclick="changeAsset('EURUSD',this)" class="asset-btn px-3 py-2 rounded-lg bg-cyber-border text-gray-300">EURUSD</button>
<button onclick="changeAsset('GBPUSD',this)" class="asset-btn px-3 py-2 rounded-lg bg-cyber-border text-gray-300">GBPUSD</button>
<button onclick="changeAsset('USDJPY',this)" class="asset-btn px-3 py-2 rounded-lg bg-cyber-border text-gray-300">USDJPY</button>
<button onclick="changeAsset('AAPL',this)" class="asset-btn px-3 py-2 rounded-lg bg-cyber-border text-gray-300">AAPL</button>
<button onclick="changeAsset('TSLA',this)" class="asset-btn px-3 py-2 rounded-lg bg-cyber-border text-gray-300">TSLA</button>
</div>

<!-- Lot Size Controller -->
<div class="bg-cyber-panel border border-cyber-border rounded-xl p-3 mb-3 flex items-center justify-between">
    <span class="text-xs font-bold text-gray-400">حجم اللوت:</span>
    <div class="flex items-center gap-3">
        <button onclick="changeLot(-1)" class="lot-btn"><i class="fas fa-minus"></i></button>
        <span id="lot-display" class="text-base font-black text-gold-500 num">0.01</span>
        <button onclick="changeLot(1)" class="lot-btn"><i class="fas fa-plus"></i></button>
    </div>
</div>

<!-- Chart (TradingView Advanced) -->
<div class="bg-cyber-panel border border-cyber-border rounded-xl overflow-hidden mb-3">
<div class="flex justify-between items-center p-2 border-b border-cyber-border bg-black/20">
<span class="text-xs font-bold text-gold-500" id="chart-title"><i class="fas fa-chart-line"></i> الذهب XAU/USD</span>
<div class="flex gap-1" id="tf-buttons">
<button onclick="changeTF('1',this)" class="tf-btn px-2 py-1 text-[11px] rounded bg-cyber-border text-gray-300">1m</button>
<button onclick="changeTF('5',this)" class="tf-btn active px-2 py-1 text-[11px] rounded bg-gold-500 text-black font-bold">5m</button>
<button onclick="changeTF('15',this)" class="tf-btn px-2 py-1 text-[11px] rounded bg-cyber-border text-gray-300">15m</button>
<button onclick="changeTF('60',this)" class="tf-btn px-2 py-1 text-[11px] rounded bg-cyber-border text-gray-300">1H</button>
<button onclick="changeTF('240',this)" class="tf-btn px-2 py-1 text-[11px] rounded bg-cyber-border text-gray-300">4H</button>
<button onclick="changeTF('D',this)" class="tf-btn px-2 py-1 text-[11px] rounded bg-cyber-border text-gray-300">1D</button>
</div></div>
<div class="h-[350px]" id="tvchart"></div>
</div>

<!-- Analysis Panel -->
<div id="analysis-panel" class="bg-cyber-panel border border-gold-500/30 rounded-xl p-3 glow-gold mb-4 analysis-locked">
<div class="flex justify-between items-center mb-3 border-b border-cyber-border pb-2">
<h2 class="text-xs text-gold-500 font-bold"><i class="fas fa-brain"></i> GOLDRIDER AI - SMC & Price Action Pro</h2>
<div id="signal-badge" class="px-3 py-1 rounded-lg bg-green-500 text-black font-black text-xs">BUY (جاهز)</div>
</div>

<div class="mb-3 bg-black/40 p-2 rounded-lg border border-gold-500/30 flex items-center justify-between">
    <span class="text-[11px] text-gold-500">سعر السوق الحالي (مطابق لمنصتك):</span>
    <div class="flex items-center gap-2">
        <input type="number" id="manual-price" step="0.01" class="bg-cyber-bg border border-cyber-border text-cyan-400 text-xs px-2 py-1 rounded w-24 text-center num" placeholder="4001.79">
        <button onclick="applyManualPrice()" class="bg-gold-500 text-black text-xs px-2 py-1 rounded font-bold hover:bg-gold-600">تحديث الأهداف</button>
    </div>
</div>

<div class="grid grid-cols-2 gap-2 text-xs mb-3">
<div class="bg-black/30 p-2 rounded-lg border border-cyber-blue/30 text-center"><p class="text-gray-400 text-[10px]">سعر الدخول (Entry)</p><p class="text-cyber-blue font-bold num text-sm" id="entry">4001.79</p></div>
<div class="bg-black/30 p-2 rounded-lg border border-red-500/30 text-center"><p class="text-gray-400 text-[10px]">وقف الخسارة (SL -10$)</p><p class="text-red-400 font-bold num text-sm" id="sl">3991.79</p></div>
</div>

<div class="grid grid-cols-4 gap-1 text-center text-[11px] mb-3">
<div class="bg-green-500/10 border border-green-500/20 p-1.5 rounded"><p class="text-gray-400 text-[9px]">TP1 (+5$)</p><p class="text-green-400 font-bold num text-xs" id="tp1">4006.79</p></div>
<div class="bg-green-500/10 border border-green-500/20 p-1.5 rounded"><p class="text-gray-400 text-[9px]">TP2 (+10$)</p><p class="text-green-400 font-bold num text-xs" id="tp2">4011.79</p></div>
<div class="bg-green-500/10 border border-green-500/20 p-1.5 rounded"><p class="text-gray-400 text-[9px]">TP3 (+15$)</p><p class="text-green-400 font-bold num text-xs" id="tp3">4016.79</p></div>
<div class="bg-green-500/10 border border-green-500/20 p-1.5 rounded"><p class="text-gray-400 text-[9px]">TP4 (+20$)</p><p class="text-green-400 font-bold num text-xs" id="tp4">4021.79</p></div>
</div>

<div class="border-t border-cyber-border pt-2 flex flex-col gap-2">
    <div class="flex justify-between items-center text-[11px]">
        <span class="text-gray-400">إثبات مصداقية الصفقة:</span>
        <span class="text-gold-500 text-sm">⭐⭐⭐⭐⭐ (99.8%)</span>
    </div>
    
    <div class="grid grid-cols-3 gap-1 mb-1">
        <button onclick="sendTelegramAlert('ENTRY')" class="bg-blue-600 hover:bg-blue-500 text-white font-bold py-1.5 px-1 rounded text-[10px]">إرسال الدخول 🚀</button>
        <button onclick="closeTradeManual()" class="bg-amber-600 hover:bg-amber-500 text-white font-bold py-1.5 px-1 rounded text-[10px]">إغلاق يدوي 🔒</button>
        <button onclick="sendTelegramAlert('SL')" class="bg-red-600 hover:bg-red-500 text-white font-bold py-1.5 px-1 rounded text-[10px]">ضرب الاستوب 🛑</button>
    </div>

    <div class="grid grid-cols-4 gap-1">
        <button onclick="sendBoomAlert(1)" class="bg-green-600 hover:bg-green-500 text-white font-bold py-1 px-1 rounded text-[10px]">BOOM TP1 💥</button>
        <button onclick="sendBoomAlert(2)" class="bg-green-600 hover:bg-green-500 text-white font-bold py-1 px-1 rounded text-[10px]">BOOM TP2 💥</button>
        <button onclick="sendBoomAlert(3)" class="bg-green-600 hover:bg-green-500 text-white font-bold py-1 px-1 rounded text-[10px]">BOOM TP3 💥</button>
        <button onclick="sendBoomAlert(4)" class="bg-green-600 hover:bg-green-500 text-white font-bold py-1 px-1 rounded text-[10px]">BOOM TP4 💥</button>
    </div>
</div>
</div>

<!-- VIP Plans & Subscriptions Section -->
<div class="bg-cyber-panel border border-cyber-border rounded-xl p-4">
    <h3 class="text-gold-500 font-black text-sm mb-3 text-center"><i class="fas fa-crown"></i> اختر خطتك VIP:</h3>
    
    <div class="grid grid-cols-2 gap-2 mb-3">
        <div onclick="selectPlan('شهر واحد', 30, this)" class="plan-card selected p-3 rounded-xl text-center cursor-pointer relative">
            <span class="text-[10px] text-gray-400">شهر واحد</span>
            <div class="text-gold-500 font-black text-lg num">$30</div>
            <span class="text-[9px] text-gray-500">30 يوم</span>
        </div>
        <div onclick="selectPlan('شهرين', 60, this)" class="plan-card p-3 rounded-xl text-center cursor-pointer relative">
            <span class="text-[10px] text-gray-400">شهرين</span>
            <div class="text-gold-500 font-black text-lg num">$60</div>
            <span class="text-[9px] text-gray-500">60 يوم</span>
        </div>
        <div onclick="selectPlan('3 أشهر', 90, this)" class="plan-card p-3 rounded-xl text-center cursor-pointer relative">
            <span class="absolute top-1 left-1 bg-green-500/20 text-green-400 text-[8px] px-1.5 py-0.5 rounded">وفر 11%</span>
            <span class="text-[10px] text-gray-400">3 أشهر</span>
            <div class="text-gold-500 font-black text-lg num">$90</div>
            <span class="text-[9px] text-gray-500">90 يوم</span>
        </div>
        <div onclick="selectPlan('6 أشهر', 120, this)" class="plan-card p-3 rounded-xl text-center cursor-pointer relative">
            <span class="absolute top-1 left-1 bg-green-500/20 text-green-400 text-[8px] px-1.5 py-0.5 rounded">وفر 33%</span>
            <span class="text-[10px] text-gray-400">6 أشهر</span>
            <div class="text-gold-500 font-black text-lg num">$120</div>
            <span class="text-[9px] text-gray-500">180 يوم</span>
        </div>
        <div onclick="selectPlan('9 أشهر', 150, this)" class="plan-card p-3 rounded-xl text-center cursor-pointer relative">
            <span class="absolute top-1 left-1 bg-green-500/20 text-green-400 text-[8px] px-1.5 py-0.5 rounded">وفر 50%</span>
            <span class="text-[10px] text-gray-400">9 أشهر</span>
            <div class="text-gold-500 font-black text-lg num">$150</div>
            <span class="text-[9px] text-gray-500">270 يوم</span>
        </div>
        <div onclick="selectPlan('سنة كاملة', 180, this)" class="plan-card p-3 rounded-xl text-center cursor-pointer relative">
            <span class="absolute top-1 left-1 bg-gold-500 text-black font-black text-[8px] px-1.5 py-0.5 rounded">الأفضل 🔥</span>
            <span class="text-[10px] text-gray-400">سنة كاملة</span>
            <div class="text-gold-500 font-black text-lg num">$180</div>
            <span class="text-[9px] text-gray-500">365 يوم</span>
        </div>
    </div>

    <div class="bg-black/40 border border-gold-500/50 rounded-xl p-3 text-center mb-3">
        <p class="text-xs text-gray-400">الخطة المختارة: <span id="selected-plan-name" class="text-gold-500 font-bold">شهر واحد</span></p>
        <div id="selected-plan-price" class="text-xl font-black text-green-400 num mt-1">$30</div>
    </div>

    <div class="grid grid-cols-3 gap-1 mb-3 text-xs">
        <button onclick="setPayment('Binance', this)" class="pay-btn active bg-gold-500 text-black font-bold py-2 rounded-lg text-center">Binance</button>
        <button onclick="setPayment('BEP20', this)" class="pay-btn bg-cyber-bg text-gray-300 border border-cyber-border py-2 rounded-lg text-center">BEP20</button>
        <button onclick="setPayment('RedotPay', this)" class="pay-btn bg-cyber-bg text-gray-300 border border-cyber-border py-2 rounded-lg text-center">RedotPay</button>
    </div>

    <div class="bg-black/30 p-3 rounded-xl border border-cyber-border mb-3 text-center">
        <p id="pay-title" class="text-xs text-gray-400 mb-1">:Binance Pay ID</p>
        <div class="flex items-center justify-center gap-2">
            <span id="pay-value" class="text-cyber-blue font-bold num text-sm">823769934</span>
            <button onclick="copyPayInfo()" class="text-gold-500 hover:text-gold-600 px-2 py-1 rounded bg-cyber-bg border border-cyber-border"><i class="fas fa-copy"></i></button>
        </div>
    </div>

    <p class="text-[11px] text-center text-gray-400 mb-2">✅ للانضمام تواصل معي على هذا الرابط 👈 <a href="https://t.me/RazakeRaziko" target="_blank" class="text-cyber-blue underline font-bold">t.me/RazakeRaziko</a></p>

    <p class="text-[11px] text-center text-gray-400 mb-2">بعد الدفع، أرسل الإثبات عبر:</p>
    <div class="grid grid-cols-2 gap-2 mb-3">
        <a href="https://wa.me/213667570565" target="_blank" class="py-2 rounded-lg whatsapp-btn text-white font-bold flex items-center justify-center gap-1 text-xs"><i class="fab fa-whatsapp"></i> واتساب</a>
        <a href="https://t.me/RazakeRaziko" target="_blank" class="py-2 rounded-lg telegram-btn text-white font-bold flex items-center justify-center gap-1 text-xs"><i class="fab fa-telegram-plane"></i> تيليجرام</a>
    </div>

    <div class="bg-cyber-bg p-3 rounded-xl border border-cyber-border mb-3">
        <p class="text-xs text-gray-300 mb-2 text-center"><i class="fas fa-key text-gold-500"></i> لديك كود تفعيل؟</p>
        <div class="flex gap-2">
            <input type="text" id="activation-code" placeholder="أدخل كود التفعيل..." class="w-full bg-black/50 border border-cyber-border rounded-lg p-2 text-center text-white text-xs num outline-none focus:border-gold-500">
            <button onclick="verifyActivationCode()" class="bg-purple-600 hover:bg-purple-500 text-white font-bold px-4 py-2 rounded-lg text-xs">تفعيل</button>
        </div>
    </div>

    <button onclick="startPreview()" class="w-full py-2.5 bg-cyber-bg border border-gold-500 text-gold-500 font-bold rounded-xl text-xs hover:bg-gold-500/10 transition text-center">
        <i class="fas fa-clock"></i> معاينة مجانية لمدة 5 دقائق (لا تظهر الصفقة)
    </button>
</div>
</main>

<script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
<script type="text/javascript">
const TELEGRAM_TOKEN = '9206676062:AAHkdzTn8zCbk2Of4gmGbr6GvyBasER1gOw';
const TELEGRAM_CHAT_ID = '-1003911614530'; 
const OWNER_CODE = '011989';

const ASSETS = {
    'XAUUSD': {tv:'OANDA:XAUUSD', name:'الذهب XAU/USD', base:4001.79, pv:3.00, dec:2},
    'XAGUSD': {tv:'OANDA:XAGUSD', name:'الفضة XAG/USD', base:31.50, pv:0.50, dec:3},
    'BTCUSDT': {tv:'BINANCE:BTCUSDT', name:'BTC/USDT', base:95000, pv:150, dec:2},
    'ETHUSDT': {tv:'BINANCE:ETHUSDT', name:'ETH/USDT', base:2700, pv:25, dec:2},
    'EURUSD': {tv:'FX:EURUSD', name:'EUR/USD', base:1.0850, pv:0.0030, dec:5},
    'GBPUSD': {tv:'FX:GBPUSD', name:'GBP/USD', base:1.2700, pv:0.0030, dec:5},
    'USDJPY': {tv:'FX:USDJPY', name:'USD/JPY', base:152.00, pv:0.30, dec:3},
    'AAPL': {tv:'NASDAQ:AAPL', name:'Apple', base:230.00, pv:2.00, dec:2},
    'TSLA': {tv:'NASDAQ:TSLA', name:'Tesla', base:250.00, pv:3.00, dec:2}
};

let currentSymbol = 'OANDA:XAUUSD', currentInterval = '5', currentAsset = ASSETS['XAUUSD'];

const LOT_VALUES = [
    0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09,
    0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9,
    1, 2, 3, 4, 5, 6, 7, 8, 9
];
let currentLotIndex = 0;

function changeLot(dir){
    currentLotIndex += dir;
    if(currentLotIndex < 0) currentLotIndex = 0;
    if(currentLotIndex >= LOT_VALUES.length) currentLotIndex = LOT_VALUES.length - 1;
    let val = LOT_VALUES[currentLotIndex];
    document.getElementById('lot-display').innerText = val >= 1 ? val.toFixed(0) : val.toFixed(2);
}

function updateAlgeriaTime() {
    const now = new Date();
    const options = { timeZone: 'Africa/Algiers', hour: '2-digit', minute: '2-digit', second: '2-digit', day: '2-digit', month: '2-digit', year: 'numeric' };
    const formatter = new Intl.DateTimeFormat('ar-DZ', options);
    document.getElementById('algeria-time').innerText = '🇩🇿 ' + formatter.format(now).replace(',', ' |');
}
setInterval(updateAlgeriaTime, 1000);
updateAlgeriaTime();

function checkPassword(){
    const val = document.getElementById('pass-input').value.trim();
    if(val === OWNER_CODE){
        document.getElementById('auth-modal').classList.add('hidden');
        document.getElementById('analysis-panel').classList.remove('analysis-locked');
        showToast("مرحباً بك يا مالك البوت! تم كشف التحليل والأهداف.", "green");
    } else {
        alert("كلمة السر غير صحيحة! كود المالك هو 011989");
    }
}

let countdownInterval;
function startPreview(){
    document.getElementById('auth-modal').classList.add('hidden');
    document.getElementById('analysis-panel').classList.add('analysis-locked');
    document.getElementById('timer-bar').style.display = 'block';
    document.getElementById('timer-text').classList.remove('hidden');
    let timeLeft = 300;
    countdownInterval = setInterval(()=>{
        timeLeft--;
        let m = Math.floor(timeLeft / 60);
        let s = timeLeft % 60;
        document.getElementById('time-display').innerText = (m < 10 ? '0'+m : m) + ':' + (s < 10 ? '0'+s : s);
        document.getElementById('timer-bar').style.width = (timeLeft / 300 * 100) + '%';
        if(timeLeft <= 0){ 
            clearInterval(countdownInterval); 
            document.getElementById('auth-modal').classList.remove('hidden'); 
            document.getElementById('timer-bar').style.display = 'none';
            document.getElementById('timer-text').classList.add('hidden');
        }
    }, 1000);
}

function selectPlan(name, price, el){
    document.querySelectorAll('.plan-card').forEach(c => c.classList.remove('selected'));
    el.classList.add('selected');
    document.getElementById('selected-plan-name').innerText = name;
    document.getElementById('selected-plan-price').innerText = '$' + price;
}

function setPayment(method, btn){
    document.querySelectorAll('.pay-btn').forEach(b => {
        b.classList.remove('active', 'bg-gold-500', 'text-black');
        b.classList.add('bg-cyber-bg', 'text-gray-300', 'border', 'border-cyber-border');
    });
    btn.classList.remove('bg-cyber-bg', 'text-gray-300', 'border', 'border-cyber-border');
    btn.classList.add('active', 'bg-gold-500', 'text-black');

    let titleEl = document.getElementById('pay-title');
    let valEl = document.getElementById('pay-value');
    if(method === 'Binance'){
        titleEl.innerText = ':Binance Pay ID';
        valEl.innerText = '823769934';
    } else if(method === 'BEP20'){
        titleEl.innerText = ':USDT (BEP20 Address)';
        valEl.innerText = '0xea5dbf7b72f2fb088c10af3ecd03324909961da5';
    } else if(method === 'RedotPay'){
        titleEl.innerText = ':RedotPay ID';
        valEl.innerText = '1862751973';
    }
}

function copyPayInfo(){
    let val = document.getElementById('pay-value').innerText;
    navigator.clipboard.writeText(val);
    showToast("✅ تم نسخ معلومات الدفع بنجاح!", "green");
}

function verifyActivationCode(){
    let code = document.getElementById('activation-code').value.trim();
    if(code === OWNER_CODE){
        document.getElementById('auth-modal').classList.add('hidden');
        document.getElementById('analysis-panel').classList.remove('analysis-locked');
        showToast("✅ تم تفعيل الحساب وكشف التحليل بنجاح!", "green");
    } else {
        alert("كود التفعيل غير صحيح!");
    }
}

function initChart(){
    try{
        document.getElementById('tvchart').innerHTML = '';
        new TradingView.widget({
            "width": "100%",
            "height": 350,
            "symbol": currentSymbol,
            "interval": currentInterval,
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "1",
            "locale": "ar",
            "hide_side_toolbar": false,
            "allow_symbol_change": true,
            "studies": [
                "MASimple@tv-basicstudies", 
                "RSI@tv-basicstudies", 
                "MACD@tv-basicstudies"
            ],
            "container_id": "tvchart"
        });
    }catch(e){}
}

function changeTF(interval, btn){
    document.querySelectorAll('.tf-btn').forEach(b=>{
        b.classList.remove('active', 'bg-gold-500', 'text-black');
        b.classList.add('bg-cyber-border', 'text-gray-300');
    });
    btn.classList.remove('bg-cyber-border', 'text-gray-300');
    btn.classList.add('active', 'bg-gold-500', 'text-black');
    currentInterval = interval;
    initChart();
}

function changeAsset(symbolKey, btn){
    const cfg = ASSETS[symbolKey];
    if(!cfg) return;
    document.querySelectorAll('.asset-btn').forEach(b=>{
        b.classList.remove('active', 'bg-gold-500', 'text-black');
        b.classList.add('bg-cyber-border', 'text-gray-300');
    });
    btn.classList.remove('bg-cyber-border', 'text-gray-300');
    btn.classList.add('active', 'bg-gold-500', 'text-black');
    currentSymbol = cfg.tv;
    currentAsset = cfg;
    document.getElementById('chart-title').innerHTML = '<i class="fas fa-chart-line"></i> ' + cfg.name;
    initChart();
    updateTradeData();
}

function updateTradeData(){
    let p = currentAsset.base;
    let dec = currentAsset.dec;
    document.getElementById('manual-price').value = p.toFixed(dec);
    document.getElementById('entry').innerText = p.toFixed(dec);
    document.getElementById('sl').innerText = (p - 10.00).toFixed(dec);
    document.getElementById('tp1').innerText = (p + 5.00).toFixed(dec);
    document.getElementById('tp2').innerText = (p + 10.00).toFixed(dec);
    document.getElementById('tp3').innerText = (p + 15.00).toFixed(dec);
    document.getElementById('tp4').innerText = (p + 20.00).toFixed(dec);
}

function applyManualPrice(){
    let val = parseFloat(document.getElementById('manual-price').value);
    if(isNaN(val)) return;
    currentAsset.base = val;
    let dec = currentAsset.dec;
    document.getElementById('entry').innerText = val.toFixed(dec);
    document.getElementById('sl').innerText = (val - 10.00).toFixed(dec);
    document.getElementById('tp1').innerText = (val + 5.00).toFixed(dec);
    document.getElementById('tp2').innerText = (val + 10.00).toFixed(dec);
    document.getElementById('tp3').innerText = (val + 15.00).toFixed(dec);
    document.getElementById('tp4').innerText = (val + 20.00).toFixed(dec);
    showToast("✅ تم تحديث السعر والأهداف بدقة مطابقة لمنصتك!", "green");
}

function showToast(msg, color='gold'){
    const toast = document.createElement('div');
    toast.className = 'toast fixed top-20 right-4 bg-' + color + '-500 text-white px-4 py-2 rounded-lg shadow-lg z-[110] text-sm font-bold';
    toast.innerText = msg;
    document.body.appendChild(toast);
    setTimeout(()=>toast.remove(), 3000);
}

async function testTelegram() {
    showToast("جاري إرسال رسالة اختبار...", 'gold');
    try {
        let res = await fetch('https://api.telegram.org/bot' + TELEGRAM_TOKEN + '/sendMessage', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({chat_id: TELEGRAM_CHAT_ID, text: '🤖 <b>اختبار البوت ناجح!</b>', parse_mode: 'HTML'})
        });
        let data = await res.json();
        if(data.ok) showToast("✅ تم الاتصال بنجاح!", "green");
        else showToast("❌ فشل الاتصال بتيليجرام", "red");
    } catch(e) {
        showToast("❌ خطأ بالشبكة", "red");
    }
}

async function sendTelegramAlert(type) {
    let assetName = currentAsset.name;
    let entry = document.getElementById('entry').innerText;
    let sl = document.getElementById('sl').innerText;
    let tp1 = document.getElementById('tp1').innerText;
    let tp2 = document.getElementById('tp2').innerText;
    let tp3 = document.getElementById('tp3').innerText;
    let tp4 = document.getElementById('tp4').innerText;

    let msg = '';
    if(type === 'ENTRY'){
        msg = `🚀 <b>إشارة دخول صفقة جديدة!</b>\\n\\n` +
              `🔹 <b>الزوج:</b> ${assetName}\\n` +
              `📊 <b>الاتجاه:</b> BUY (شراء)\\n` +
              `🎯 <b>سعر الدخول:</b> <code>${entry}</code>\\n` +
              `🛑 <b>وقف الخسارة (SL -10$):</b> <code>${sl}</code>\\n\\n` +
              `📌 <b>الأهداف المستهدفة (+20$ إجمالي):</b>\\n` +
              `▪️ TP1 (+5$): <code>${tp1}</code>\\n` +
              `▪️ TP2 (+10$): <code>${tp2}</code>\\n` +
              `▪️ TP3 (+15$): <code>${tp3}</code>\\n` +
              `▪️ TP4 (+20$): <code>${tp4}</code>\\n\\n` +
              `⭐ <b>مصداقية الصفقة:</b> ⭐⭐⭐⭐⭐ (99.8%)\\n` +
              `👑 <i>GOLDRIDER & RAZAKE TRADING</i>`;
    } else if(type === 'SL'){
        msg = `🛑 <b>تنبيه: تم ضرب وقف الخسارة (SL) (-10$)</b>\\n\\n` +
              `🔹 <b>الزوج:</b> ${assetName}\\n` +
              `⚠️ تم الخروج بحماية رأس المال لضمان استمرار الأرباح.\\n` +
              `👑 <i>GOLDRIDER & RAZAKE TRADING</i>`;
    }

    await postToTelegram(msg);
}

async function sendBoomAlert(tpNum) {
    let assetName = currentAsset.name;
    let targetPrice = document.getElementById('tp' + tpNum).innerText;
    let profitAmount = tpNum === 1 ? '5$' : (tpNum === 2 ? '10$' : (tpNum === 3 ? '15$' : '20$'));
    
    let msg = `💥 <b>BOOM! تم تحقيق الهدف ${tpNum} بنجاح!</b> 🎯\\n\\n` +
              `🔹 <b>الزوج:</b> ${assetName}\\n` +
              `✅ <b>السعر المستهدف:</b> <code>${targetPrice}</code>\\n` +
              `💰 <b>الربح المحقق:</b> +${profitAmount}\\n\\n` +
              `⭐ <i>GOLDRIDER & RAZAKE TRADING</i>`;

    await postToTelegram(msg);
}

async function closeTradeManual(){
    let assetName = currentAsset.name;
    let msg = `🔒 <b>إغلاق يدوي للصفقة</b>\\n\\n` +
              `🔹 <b>الزوج:</b> ${assetName}\\n` +
              `⚠️ تم إغلاق الصفقة يدوياً لحجز الأرباح أو تقليل المخاطر.\\n` +
              `👑 <i>GOLDRIDER & RAZAKE TRADING</i>`;

    await postToTelegram(msg);
}

async function postToTelegram(text){
    showToast("جاري إرسال الإشعار للقناة...", "gold");
    try {
        let res = await fetch('https://api.telegram.org/bot' + TELEGRAM_TOKEN + '/sendMessage', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({chat_id: TELEGRAM_CHAT_ID, text: text, parse_mode: 'HTML'})
        });
        let data = await res.json();
        if(data.ok) showToast("✅ تم إرسال الإشعار بنجاح!", "green");
        else showToast("❌ فشل إرسال الإشعار", "red");
    } catch(e) {
        showToast("❌ خطأ بالشبكة", "red");
    }
}

window.onload = function(){
    initChart();
    updateTradeData();
};
</script>
</body>
</html>"""

# ================= ================= =================
#  معالج الطلب السحابي لعرض الصفحة ومنع الشاشة البيضاء
# ================= ================= =================
async def on_fetch(request):
    return Response.new(
        HTML_CONTENT,
        headers={"Content-Type": "text/html;charset=UTF-8"}
    )
