from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Email Configuration
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))

# CV file paths
CV_FILES = {
    'junior': 'cv_models/Junior_cv_model.docx',
    'senior': 'cv_models/Senior_cv_model.docx'
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Send a command in the format: email, junior or email, senior')

async def send_cv(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Parse the command
    command = ' '.join(context.args).split(', ')
    if len(command) != 2:
        await update.message.reply_text('Invalid command format. Use: email, junior or email, senior')
        return

    email, cv_type = command
    if cv_type not in CV_FILES:
        await update.message.reply_text('Invalid CV type. Use "junior" or "senior".')
        return

    # Send the email
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = f'{cv_type.capitalize()} CV'

        # Attach the CV
        part = MIMEBase('application', 'octet-stream')
        with open(CV_FILES[cv_type], 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={cv_type}_cv.docx')
        msg.attach(part)

        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, email, msg.as_string())

        await update.message.reply_text(f'{cv_type.capitalize()} CV sent to {email}.')
    except Exception as e:
        await update.message.reply_text(f'Error: {e}')

def main():
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("sendcv", send_cv))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
