from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# معرف قناتك الجديد الذي يجب على الأعضاء الاشتراك فيه
CHANNEL_USERNAME = "@xxxxxxxxxxxxxxxxxxxxxxxxx777777" 

async def welcome_and_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
        
    chat = update.message.chat
    user = update.message.from_user
    
    # استثناء البوت نفسه أو المشرفين من قيود الاشتراك
    if user.is_bot:
        return

    # --- الجزء الأول: الترحيب بالأعضاء الجدد ---
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
                    InlineKeyboardButton(" يوتيوب", url="https://youtube.com/@bacwithmustapha"),
                    InlineKeyboardButton(" انستغرام", url="https://www.instagram.com/benyattoumustapha1")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_html(welcome_text, reply_markup=reply_markup)
        return

    # --- الجزء الثاني: فحص الاشتراك الإجباري في القناة لكل رسالة ---
    try:
        # فحص حالة العضو في القناة الجديدة
        member_status = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user.id)
        
        # إذا كان العضو لم يترك القناة (يعني مشترك فيها)
        if member_status.status in ['left', 'kicked']:
            # حذف رسالته لكي لا يتمكن من التكلم
            await update.message.delete()
            
            # إرسال تنبيه يطلبه بالاشتراك مع زر القناة
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
    except Exception as e:
        # لتجنب توقف البوت إذا حدث خطأ في الصلاحيات
        pass

def main():
    TOKEN = "8505095845:AAH3QdFVOK7jTeb7sds8Fx7Q7rgeb3mQLwo"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # معالج يستمع لكل الرسائل وانضمام الأعضاء الجدد
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, welcome_and_check))
    
    print("البوت يعمل الآن مع معرف القناة الجديد ونظام الحماية...")
    app.run_polling()

if __name__ == '__main__':
    main()