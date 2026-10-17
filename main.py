import os, random
from flask import Flask
from threading import Thread
import telebot
from telebot import types

app = Flask(__name__)
@app.route('/')
def home(): return "Bot OK - 40 Buttons Working"
@app.route('/health')
def health(): return "OK", 200

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = 7145036494
CHANNEL = "pkwbiwjwbekeekkw"
LINK = "https://t.me/pkwbiwjwbekeekkw"

bot = telebot.TeleBot(TOKEN, threaded=False)
os.makedirs("database", exist_ok=True)

def get_pts(uid):
    try:
        with open(f"database/{uid}.txt","r",encoding="utf-8") as f:
            return int(f.read() or 0)
    except: return 0

def add_pts(uid,n):
    open(f"database/{uid}.txt","w",encoding="utf-8").write(str(get_pts(uid)+n))

def is_sub(uid):
    try:
        s = bot.get_chat_member(f"@{CHANNEL}", uid).status
        return s in ['member','administrator','creator']
    except:
        return True

@bot.message_handler(commands=['start'])
def start(m):
    uid = m.from_user.id
    if not is_sub(uid):
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("اشترك", url=LINK))
        kb.add(types.InlineKeyboardButton("تحققت", callback_data="check"))
        bot.send_message(uid, f"اشترك اولا\n{LINK}", reply_markup=kb)
        return
    pts = get_pts(uid)
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton("القناة", url=LINK))
    kb.add(types.InlineKeyboardButton("ضمان متجر 5", callback_data="daman_s"), types.InlineKeyboardButton("ضمان حساب 5", callback_data="daman_a"))
    kb.add(types.InlineKeyboardButton("ضمان ارقام 5", callback_data="daman_n"), types.InlineKeyboardButton("ضمان ايميل 5", callback_data="daman_e"))
    kb.add(types.InlineKeyboardButton("ضمان شحن 5", callback_data="daman_sh"), types.InlineKeyboardButton("ضمان متابعين 5", callback_data="daman_f"))
    kb.add(types.InlineKeyboardButton("ايميل وهمي 5", callback_data="fake"), types.InlineKeyboardButton("تفعيل 5", callback_data="active"))
    kb.add(types.InlineKeyboardButton("كود 5", callback_data="code"), types.InlineKeyboardButton("10 دقايق 5", callback_data="temp10"))
    kb.add(types.InlineKeyboardButton("دائم 15", callback_data="perm"), types.InlineKeyboardButton("مشفر 10", callback_data="secure"))
    kb.add(types.InlineKeyboardButton("شحن 5", callback_data="charge"), types.InlineKeyboardButton("تتبع 5", callback_data="track"))
    kb.add(types.InlineKeyboardButton("خصم 5", callback_data="coupon"), types.InlineKeyboardButton("فاتورة 5", callback_data="invoice"))
    kb.add(types.InlineKeyboardButton("متابعين 15", callback_data="follow"), types.InlineKeyboardButton("لايكات 15", callback_data="like"))
    kb.add(types.InlineKeyboardButton("مشاهدات 15", callback_data="view"), types.InlineKeyboardButton("اعضاء 15", callback_data="member"))
    kb.add(types.InlineKeyboardButton("فك حظر شامل 15", callback_data="unban_all"), types.InlineKeyboardButton("رقم وهمي 15", callback_data="num"))
    kb.add(types.InlineKeyboardButton("امريكي 25", callback_data="usnum"), types.InlineKeyboardButton("واتس شامل 15", callback_data="whats"))
    kb.add(types.InlineKeyboardButton("تصميم 5", callback_data="design"), types.InlineKeyboardButton("فلتر 5", callback_data="filter"))
    kb.add(types.InlineKeyboardButton("كتابة 5", callback_data="textpic"), types.InlineKeyboardButton("جودة 5", callback_data="hd"))
    kb.add(types.InlineKeyboardButton("لوجو 10", callback_data="logo"), types.InlineKeyboardButton("بطاقة 10", callback_data="card"))
    kb.add(types.InlineKeyboardButton("بانر 10", callback_data="banner"), types.InlineKeyboardButton("بوستر 10", callback_data="poster"))
    kb.add(types.InlineKeyboardButton("سيفي 10", callback_data="cv"), types.InlineKeyboardButton("QR 5", callback_data="qr"))
    kb.add(types.InlineKeyboardButton("نشر 20", callback_data="ad_post"), types.InlineKeyboardButton("تثبيت 30", callback_data="ad_pin"))
    kb.add(types.InlineKeyboardButton("ممول 50", callback_data="ad_spon"), types.InlineKeyboardButton("بث 100", callback_data="ad_all"))
    kb.add(types.InlineKeyboardButton(f"رصيدك {pts}", callback_data="bal"))
    kb.add(types.InlineKeyboardButton("شراء نقاط", callback_data="buy"))
    bot.send_message(uid, f"متجر زيده - 40 زر - كل شي ينفذ\nرصيدك {pts}\n{LINK}", reply_markup=kb)

@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    try:
        bot.answer_callback_query(c.id)
        d = c.data
        uid = c.from_user.id
        chat = c.message.chat.id

        if d == "check":
            if is_sub(uid):
                try: bot.delete_message(chat, c.message.message_id)
                except: pass
                start(c.message)
            else:
                bot.send_message(chat, f"ما اشتركت\n{LINK}")
            return

        if d == "bal":
            bot.send_message(chat, f"رصيدك: {get_pts(uid)}")
            return
        if d == "buy":
            bot.send_message(chat, f"شراء نقاط:\n5=1000 يمني\n15=2500\n30=5000\n100=15000\nالكريمي جعار\nايدك {uid}")
            return

        prices = {"daman_s":5,"daman_a":5,"daman_n":5,"daman_e":5,"daman_sh":5,"daman_f":5,"fake":5,"active":5,"code":5,"temp10":5,"perm":15,"secure":10,"charge":5,"track":5,"coupon":5,"invoice":5,"follow":15,"like":15,"view":15,"member":15,"unban_all":15,"num":15,"usnum":25,"whats":15,"design":5,"filter":5,"textpic":5,"hd":5,"logo":10,"card":10,"banner":10,"poster":10,"cv":10,"qr":5,"ad_post":20,"ad_pin":30,"ad_spon":50,"ad_all":100}
        price = prices.get(d,5)

        if get_pts(uid) < price:
            bot.send_message(chat, f"تحتاج {price} رصيدك {get_pts(uid)}")
            return

        if d in ["unban_all","whats"]:
            bot.send_message(chat, f"ارسل الرقم مع رمز البلد +967\nالسعر {price}")
            bot.register_next_step_handler_by_chat_id(chat, lambda m: do_unban(m,price))
            return

        if d in ["design","logo","card","banner","poster","cv","filter","hd","textpic"]:
            bot.send_message(chat, f"ارسل الصورة لـ {d} - السعر {price}")
            bot.register_next_step_handler_by_chat_id(chat, lambda m: do_photo(m,d,price))
            return

        if d.startswith("daman_"):
            bot.send_message(chat, "ارسل اسم متجرك")
            bot.register_next_step_handler_by_chat_id(chat, lambda m: do_daman(m,d,price))
            return

        add_pts(uid,-price)
        bot.send_message(chat, f"✅ تم تنفيذ {d}\nخصم {price} - رصيدك {get_pts(uid)}\n/start")

    except Exception as e:
        print(e)
        try: bot.answer_callback_query(c.id)
        except: pass

def do_photo(m,typ,price):
    try:
        if m.content_type != 'photo':
            bot.send_message(m.chat.id, "ارسل صورة فقط")
            return
        add_pts(m.from_user.id,-price)
        bot.send_photo(m.chat.id, m.photo[-1].file_id, caption=f"✅ تم تنفيذ {typ}\nخصم {price} رصيدك {get_pts(m.from_user.id)}\n{LINK}\n/start")
    except Exception as e:
        bot.send_message(m.chat.id, f"خطا {e}")

def do_daman(m,typ,price):
    try:
        add_pts(m.from_user.id,-price)
        bot.send_message(m.chat.id, f"✅ ضمان {typ} منفذ\nالمتجر: {m.text}\nذهبي 7 ايام\n{random.randint(1000,9999)}-WARRANTY\n{LINK}\nرصيدك {get_pts(m.from_user.id)}")
    except: pass

def do_unban(m,price):
    try:
        add_pts(m.from_user.id,-price)
        bot.send_message(m.chat.id, f"🔓 فك حظر شامل منفذ\nالرقم: {m.text}\n✅ واتس + تليجرام + ايمو + فايبر + سيجنال\nاحذف وثبت الرسمي وانتظر 12 ساعة\n{LINK}\nرصيدك {get_pts(m.from_user.id)}\n/start")
    except: pass

@bot.message_handler(content_types=['photo'])
def photo_any(m):
    bot.send_message(m.chat.id, "الصورة وصلت ✅ اضغط /start")

@bot.message_handler(commands=['add'])
def add_cmd(m):
    if m.from_user.id != ADMIN_ID: return
    try:
        _, uid, pts = m.text.split()
        add_pts(int(uid), int(pts))
        bot.send_message(int(uid), f"تم شحن {pts} رصيدك {get_pts(int(uid))}")
        bot.send_message(m.chat.id, "تم")
    except: pass

def run_bot():
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except:
            continue

if __name__ == "__main__":
    Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))