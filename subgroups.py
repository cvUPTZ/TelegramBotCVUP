from telegram import Update, Bot
from telegram.ext import CommandHandler, MessageHandler, filters, Updater, CallbackContext

# Your main group ID and the subgroup IDs
MAIN_GROUP_ID = '-1002197473030_1'
cvup_sendcv_ID= '-1002197473030_3137'
REVIEW_GROUP_ID = '-1002197473030_3130'
INTERVIEW_GROUP_ID = '-1002197473030_3147'
JOB_POSTINGS_GROUP_ID = '-1002197473030_3148'
Q_A_ID = '-1002197473030_3136'

# Create a bot instance
bot = Bot(token='7495077361:AAHDCDdyfUbOzoajombUut_r2k699jEiFWc')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "👋 Welcome to CV_UP! Please choose one of the following options to submit your CV:\n\n"
        "🧑‍💻 /junior - For Junior CVs\n"
        "👨‍💼 /senior - For Senior CVs\n"
        "🔍 /review - For CV Review\n"
        "💡 /tips - For CV Tips & Best Practices\n"
        "🎤 /interview - For Interview Preparation\n"
        "📢 /job_postings - For Job Postings\n"
        "🤝 /networking - For Networking\n"
        "🖼️ /portfolio - For Portfolio Sharing\n"
        "🎓 /skills - For Skills Development\n"
        "🔄 /exchange - For CV Exchange\n"
        "🚀 /job_search - For Job Search Support\n"
        " /question - Q&A"
    )

def handle_cv(update: Update, context: CallbackContext) -> None:
    # Extract the message text and decide which subgroup to send it to
    text = update.message.text.lower()
    
    if text.startswith('/junior'):
        bot.forward_message(chat_id=JUNIOR_GROUP_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        update.message.reply_text("🧑‍💻 Your CV has been forwarded to the Junior CV group.")
        
    elif text.startswith('/senior'):
        bot.forward_message(chat_id=SENIOR_GROUP_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        update.message.reply_text("👨‍💼 Your CV has been forwarded to the Senior CV group.")
        
    elif text.startswith('/review'):
        bot.forward_message(chat_id=REVIEW_GROUP_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        update.message.reply_text("🔍 Your CV has been forwarded to the CV Review group.")
        
    elif text.startswith('/tips'):
        bot.forward_message(chat_id=TIPS_GROUP_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        update.message.reply_text("💡 Your message has been forwarded to the CV Tips group.")
        
    elif text.startswith('/interview'):
        bot.forward_message(chat_id=INTERVIEW_GROUP_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        update.message.reply_text("🎤 Your message has been forwarded to the Interview Preparation group.")
        
    elif text.startswith('/job_postings'):
        bot.forward_message(chat_id=JOB_POSTINGS_GROUP_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        update.message.reply_text("📢 Your message has been forwarded to the Job Postings group.")
        
    elif text.startswith('/networking'):
        bot.forward_message(chat_id=NETWORKING_GROUP_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        update.message.reply_text("🤝 Your message has been forwarded to the Networking group.")
        
    elif text.startswith('/portfolio'):
        bot.forward_message(chat_id=PORTFOLIO_GROUP_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        update.message.reply_text("🖼️ Your portfolio has been forwarded to the Portfolio Sharing group.")
        
    elif text.startswith('/skills'):
        bot.forward_message(chat_id=SKILLS_GROUP_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        update.message.reply_text("🎓 Your message has been forwarded to the Skills Development group.")
        
    elif text.startswith('/exchange'):
        bot.forward_message(chat_id=EXCHANGE_GROUP_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        update.message.reply_text("🔄 Your CV has been forwarded to the CV Exchange group.")
        
    elif text.startswith('/job_search'):
        bot.forward_message(chat_id=JOB_SEARCH_GROUP_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        update.message.reply_text("🚀 Your message has been forwarded to the Job Search Support group.")
        
    else:
        update.message.reply_text("❗ Please use one of the commands to categorize your CV or message.")

def main():
    # Initialize the updater and dispatcher
    updater = Updater("7495077361:AAHDCDdyfUbOzoajombUut_r2k699jEiFWc", use_context=True)
    dispatcher = updater.dispatcher

    # Command and message handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(filters.text & ~filters.command, handle_cv))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
