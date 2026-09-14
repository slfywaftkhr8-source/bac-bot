from flask import Flask
import threading
import os
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from apscheduler.schedulers.background import BackgroundScheduler

# معرف قناتك للاشتراك الإجباري
CHANNEL_USERNAME = "@xxxxxxxxxxxxxxxxxxxxxxxxx777777"  

# معرف مجموعتك التي سيتم إرسال الرسائل إليها تلقائياً
GROUP_CHAT_ID = "@rrrrrrrrrrrrrrrrrrrrr1232"  

# --- قائمة الآيات والأحاديث النبوية فقط ---
MOTIVATIONAL_MESSAGES = [
    "﴿ وَأَنْ لَيْسَ لِلْإِنْسَانِ إِلَّا مَا سَعَى ۝ وَأَنَّ سَعْيَهُ سَوْفَ يُرَى ﴾ 📚✨",
    "قال رسول الله ﷺ: «احْرِصْ عَلَى مَا يَنْفَعُكَ، وَاسْتَعِنْ بِاللهِ وَلَا تَعْجَزْ». 💪🔥",
    "﴿ وَمَنْ يَتَوَكَّلْ عَلَى اللهِ فَهُوَ حَسْبُهُ ﴾ 🌿🤍",
    "﴿ إِنَّا لَا نُضِيعُ أَجْرَ مَنْ أَحْسَنَ عَمَلًا ﴾ 🎓🚀",
    "«اللهُمَّ لا سَهْلَ إِلَّا مَا جَعَلْتَهُ سَهْلًا، وَأَنْتَ تَجْعَلُ الحَزْنَ إِذَا شِئْتَ سَهْلًا». 📖✨",
    "﴿ وَمَا تَوْفِيقِي إِلَّا بِاللهِ ۚ عَلَيْهِ تَوَكَّلْتُ وَإِلَيْهِ أُنِيبُ ﴾ 🌟",
    "«أَحَبُّ الأعمالِ أدومُها وإن قلَّ». ⏳💡",
    "﴿ لَا يُكَلِّفُ اللهُ نَفْسًا إِلَّا وُسْعَهَا ﴾ 🕊️",
    "﴿ فَإِنَّ مَعَ الْعُسْرِ يُسْرًا ۝ إِنَّ مَعَ الْعُسْرِ يُسْرًا ﴾ 🌅",
    "﴿ وَالَّذِينَ جَاهَدُوا فِينَا لَنَهْدِيَنَّهُمْ سُبُلَنَا ﴾ 🦅",
    "﴿ فَإِذَا عَزَمْتَ فَتَوَكَّلْ عَلَى اللهِ ﴾ ⏰⚡",
    "﴿ وَقُلْ رَبِّ زِدْنِي عِلْمًا ﴾ 🌌",
    "﴿ وَأُفَوِّضُ أَمْرِي إِلَى اللهِ ﴾ 🕊️",
    "«اللهم انفعني بما علمتني، وعلّمني ما ينفعني، وزدني علماً». 🤲✨"
]

# خادم ويب وهمي لـ Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bac Bot is online and running 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# إرسال الآيات والأحاديث تلقائياً
async def send_scheduled_motivation(bot):
    try:
        message_content = random.choice(MOTIVATIONAL_MESSAGES)
        keyboard = [
            [InlineKeyboardButton("⏳ موعدنا شهر جوان بحول الله 🔥", url="https://t.me/bacwithmostapha")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=message_content,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"خطأ في إرسال الرسالة التلقائية: {e}")

def schedule_jobs(application):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: application.create_task(send_scheduled_motivation(application.bot)), 'interval', hours=2)
    scheduler.start()

# المعالج الأساسي للرسائل والحماية
async def welcome_and_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
        
    chat = update.message.chat
    user = update.message.from_user
    
    if user.is_bot:
        return

    # 1. الترحيب بالأعضاء الجدد
    if update.message.new_chat_members:
        for member in update.message.new_chat_members:
            if member.id == context.bot.id:
                continue
            mention = member.mention_html()
            welcome_text = (
                f"👋 أهلاً بك {mention} في مجموعة أسطورة الباك!\n\n"
                "📚 هنا نراجع، نتناقش، نتعاون ونشارك كل ما يفيدنا في مشوار البكالوريا.\n\n"
                "🤝 احترم غيرك، أفد غيرك، وخلي بصمتك إيجابية.\n\n"
                "🎯 معًا نحو الامتياز بإذن الله. 🔥"
            )
            keyboard = [
                [
                    InlineKeyboardButton("يوتيوب", url="https://youtube.com/@bacwithmustapha"),
                    InlineKeyboardButton("انستغرام", url="https://www.instagram.com/benyattoumustapha1")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_html(welcome_text, reply_markup=reply_markup)
        return

    # 2. التحقق من المشرفين (استثناء تام وسريع للأدمينات)
    is_admin = False
    try:
        member_obj = await chat.get_member(user.id)
        if member_obj.status in ['creator', 'administrator']:
            is_admin = True
    except Exception:
        pass

    if is_admin:
        return

    # 3. فحص الاشتراك الإجباري
    try:
        member_status = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user.id)
        if member_status.status in ['left', 'kicked']:
            await update.message.delete()
            mention = user.mention_html()
            warning_keyboard = [
                [InlineKeyboardButton("📢 اشترك في القناة هنا", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")]
            ]
            warning_markup = InlineKeyboardMarkup(warning_keyboard)
            await chat.send_message(
                text=f"عذراً {mention} ⛔\nلا يمكنك إرسال رسائل في هذه المجموعة حتى تشترك في القناة الرسمية أولاً!",
                reply_markup=warning_markup,
                parse_mode="HTML"
            )
            return
    except Exception:
        pass

    # 4. منع إعادة التوجيه للأعضاء العاديين
    if update.message.forward_date or update.message.forward_from or update.message.forward_from_chat:
        try:
            await update.message.delete()
            mention = user.mention_html()
            await chat.send_message(
                text=f"عذراً {mention} ⛔\nإعادة توجيه الرسائل من خارج المجموعة غير مسموح بها هنا!",
                parse_mode="HTML"
            )
            return
        except Exception:
            pass

    # 5. منع الروابط للأعضاء العاديين
    has_link = False
    if update.message.entities:
        for entity in update.message.entities:
            if entity.type in ["url", "text_link"]:
                has_link = True
                break
    
    if not has_link and update.message.text:
        text_lower = update.message.text.lower()
        if "http://" in text_lower or "https://" in text_lower or "t.me://" in text_lower or "www." in text_lower:
            has_link = True

    if has_link:
        try:
            await update.message.delete()
            mention = user.mention_html()
            await chat.send_message(
                text=f"عذراً {mention} ⛔\nمنع إرسال الروابط الخارجية في المجموعة حفاظاً على تركيز الطلاب!",
                parse_mode="HTML"
            )
            return
        except Exception:
            pass

def main():
    TOKEN = "8505095845:AAH3QdFVOK7jTeb7sds8Fx7Q7rgeb3mQLwo"
    
    app_bot = ApplicationBuilder().token(TOKEN).build()
    
    schedule_jobs(app_bot)
    
    app_bot.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, welcome_and_check))
    
    print("البوت يعمل الآن بالآيات والأحاديث فقط...")
    app_bot.run_polling()

if __name__ == '__main__':
    t = threading.Thread(target=run_web)
    t.start()
    
    main()
