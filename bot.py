import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import random
import os
import threading
from flask import Flask

# --- إعداد خادم الويب لإبقاء البوت مستيقظاً على Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Ruzba Bot is active 24/7! 🚀"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()
# -----------------------------------------------------

TOKEN = "9235998382:AAEG9EUpI9jMn9qewA-i3Ft1Hne5YrkF9Ms"
CREATOR_ID = 5742138769  # رقم الـ ID الخاص بك

bot = telebot.TeleBot(TOKEN)

PUNISHMENT_PHRASE = "أيها التافه.. إن لم يربوك أهلك، أنا استطيع تربيتك!"

BANNED_WORDS = [
    "شرموط", "قحبة", "منيوك", "كس امك", "احا", "خرا", "زبي", 
    "تعال خاص", "كلمني خاص", "عايز تعرفني", "تعال للخاص",
    "ربح المال", "دخل يومي", "عمل وهمي", "توفير دخل", "تداول مضمون",
    "http://", "https://", "t.me/", "www."
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = f"أهلاً بك يا {user_name} في بوت روزبا للحماية. اختر ما يناسبك من القائمة أدناه:"
    
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("معلومات البوت السيادي 🛡️", callback_data="bot_info"),
        InlineKeyboardButton("قائمة الألعاب الشاملة 🎮", callback_data="games_menu")
    )
    bot.reply_to(message, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "bot_info":
        bot.answer_callback_query(call.id, "روزبا: الحماية القصوى.")
        bot.send_message(call.message.chat.id, "🛡️ بوت روزبا يعمل بكامل طاقته وحمايته الصارمة.")
        
    elif call.data == "games_menu":
        bot.answer_callback_query(call.id, "تم فتح قسم الألعاب العريقة 👑")
        games_markup = InlineKeyboardMarkup()
        games_markup.row_width = 1
        games_markup.add(
            InlineKeyboardButton("♟️ لعبة الشطرنج (تحدي التفكير)", callback_data="game_chess"),
            InlineKeyboardButton("🃏 لعبة الشدة (سحب ورقة الحظ)", callback_data="game_cards"),
            InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data="main_menu")
        )
        bot.edit_message_text("🎮 **قائمة الألعاب السيادية:**\nاختر لعبتك المفضلة وابدأ التحدي فوراً:", 
                              call.message.chat.id, 
                              call.message.message_id, 
                              reply_markup=games_markup)
                              
    elif call.data == "game_chess":
        bot.answer_callback_query(call.id, "معركة الشطرنج")
        chess_markup = InlineKeyboardMarkup()
        chess_markup.add(
            InlineKeyboardButton("🎲 العب نقلة عشوائية", callback_data="chess_move"),
            InlineKeyboardButton("📖 شرح اللعبة", callback_data="chess_help"),
            InlineKeyboardButton("🔙 رجوع للألعاب", callback_data="games_menu")
        )
        bot.edit_message_text("♟️ **قاعة الشطرنج الملكية:**\nأهلاً بك في معركة الفكر. هذه أول مرة تدخل هنا؟ اضغط على 'شرح اللعبة' لمعرفة القواعد، أو ابدأ اللعب فوراً يا سيد القصر!", 
                              call.message.chat.id, 
                              call.message.message_id, 
                              reply_markup=chess_markup)

    elif call.data == "chess_help":
        bot.answer_callback_query(call.id, "قواعد الشطرنج")
        chess_markup = InlineKeyboardMarkup()
        chess_markup.add(
            InlineKeyboardButton("🎲 العب الآن", callback_data="game_chess"),
            InlineKeyboardButton("🔙 رجوع للألعاب", callback_data="games_menu")
        )
        bot.edit_message_text("📖 **شرح لعبة الشطرنج:**\n• هي لعبة استراتيجية ملكية تلعب على رقعة مربعة.\n• الهدف الأساسي هو محاصرة ملك الخصم (كش مات).\n• في هذا البوت، يمكنك تجربة نقلات ذكية وتكتيكية بضغطة زر لاختبار حظك وخبرتك!", 
                              call.message.chat.id, 
                              call.message.message_id, 
                              reply_markup=chess_markup)

    elif call.data == "chess_move":
        moves = ["لقد قمت بتحريك الحصان إلى f3 ببراعة! ♞", "نقلة ذكية بالقلعة إلى e1! ♜", "حماية الملك بتبييت ممتاز! ♔", "هجوم بالوزير إلى h5! ♕"]
        bot.answer_callback_query(call.id, "تم تنفيذ النقلة!")
        chess_markup = InlineKeyboardMarkup()
        chess_markup.add(
            InlineKeyboardButton("🎲 نقلة أخرى", callback_data="chess_move"),
            InlineKeyboardButton("📖 شرح اللعبة", callback_data="chess_help"),
            InlineKeyboardButton("🔙 رجوع للألعاب", callback_data="games_menu")
        )
        bot.edit_message_text(f"♟️ **نتيجة المعركة:**\n{random.choice(moves)}", 
                              call.message.chat.id, 
                              call.message.message_id, 
                              reply_markup=chess_markup)
                              
    elif call.data == "game_cards":
        bot.answer_callback_query(call.id, "طاولة الشدة")
        cards_markup = InlineKeyboardMarkup()
        cards_markup.add(
            InlineKeyboardButton("🃏 اسحب ورقة جديدة", callback_data="draw_card"),
            InlineKeyboardButton("📖 شرح اللعبة", callback_data="cards_help"),
            InlineKeyboardButton("🔙 رجوع للألعاب", callback_data="games_menu")
        )
        bot.edit_message_text("🃏 **طاولة الشدة (الورق):**\nمرحباً بك في طاولة الورق! اضغط على 'شرح اللعبة' لتعرف قواعد السحب، أو ابدأ سحب أوراق الحظ فوراً.", 
                              call.message.chat.id, 
                              call.message.message_id, 
                              reply_markup=cards_markup)

    elif call.data == "cards_help":
        bot.answer_callback_query(call.id, "قواعد الشدة")
        cards_markup = InlineKeyboardMarkup()
        cards_markup.add(
            InlineKeyboardButton("🃏 ابدأ السحب", callback_data="game_cards"),
            InlineKeyboardButton("🔙 رجوع للألعاب", callback_data="games_menu")
        )
        bot.edit_message_text("📖 **شرح لعبة الشدة (الورق):**\n• تتكون طاولة الورق من 52 ورقة مقسمة إلى 4 أنواع (سباتي، هارت، ديمن، قبس).\n• في هذه اللعبة، يقوم البوت بسحب ورقة عشوائية لك لاختبار حظك وقوتك في الجولة!", 
                              call.message.chat.id, 
                              call.message.message_id, 
                              reply_markup=cards_markup)

    elif call.data == "draw_card":
        suits = ["القبس ( spades ♠ )", "الديمن ( diamonds ♦ )", "الهارت ( hearts ♥ )", "السباتي ( clubs ♣ )"]
        numbers = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Queen", "King"]
        drawn = f"{random.choice(numbers)} من {random.choice(suits)}"
        bot.answer_callback_query(call.id, "سحبت ورقة!")
        cards_markup = InlineKeyboardMarkup()
        cards_markup.add(
            InlineKeyboardButton("🃏 اسحب ورقة أخرى", callback_data="draw_card"),
            InlineKeyboardButton("📖 شرح اللعبة", callback_data="cards_help"),
            InlineKeyboardButton("🔙 رجوع للألعاب", callback_data="games_menu")
        )
        bot.edit_message_text(f"🃏 **ورقتك المسحوبة:**\nلقد حصلت على: **{drawn}** 🌟", 
                              call.message.chat.id, 
                              call.message.message_id, 
                              reply_markup=cards_markup)
                              
    elif call.data == "main_menu":
        bot.answer_callback_query(call.id, "القائمة الرئيسية")
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(
            InlineKeyboardButton("معلومات البوت السيادي 🛡️", callback_data="bot_info"),
            InlineKeyboardButton("قائمة الألعاب الشاملة 🎮", callback_data="games_menu")
        )
        bot.edit_message_text("أهلاً بك مجدداً في القائمة الرئيسية لـ روزبا:", 
                              call.message.chat.id, 
                              call.message.message_id, 
                              reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def security_and_chat_handler(message):
    if not message.text:
        return
        
    user_id = message.from_user.id
    username = message.from_user.username
    text_lower = message.text.lower()

    is_me = (user_id == CREATOR_ID) or (username and username.lower() == "alone123987")

    is_admin = False
    if message.chat.type in ['group', 'supergroup']:
        try:
            member = bot.get_chat_member(message.chat.id, user_id)
            if member.status in ['creator', 'administrator']:
                is_admin = True
        except:
            pass

    has_violation = any(word in text_lower for word in BANNED_WORDS)
    
    if has_violation:
        if is_me or is_admin:
            return
        else:
            user_mention = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
            punishment_msg = f"{PUNISHMENT_PHRASE} {user_mention}"
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except:
                pass
            bot.send_message(message.chat.id, punishment_msg)
            return

    if "روزبا" in message.text or "rowthba" in text_lower:
        if is_me:
            bot.reply_to(message, "أهلاً بك يا سيد القصر أحمد، أنا في خدمتك دائماً! 👑")
        else:
            bot.reply_to(message, "أهلاً بك، أنا بوت روزبا للحماية.")
        return

if __name__ == '__main__':
    print("🤖 Starting Web Server for 24/7 uptime...")
    keep_alive()  # تشغيل خادم الويب في الخلفية
    
    print("🤖 Ruzba Bot is running...")
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Connection error: {e}")
            time.sleep(5)
