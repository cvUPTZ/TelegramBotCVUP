# api/webhook.py

import json
import logging
from telegram import Update
from telegram.ext import Application
# from bot.bot import initialize_bot  # Assume this function creates and returns your bot's Application

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the application
app = initialize_bot()

async def handle_update(update: Update):
    """Process the Telegram update."""
    await app.process_update(update)

async def handler(request):
    """Vercel serverless function handler."""
    try:
        logger.debug("Handler function called")
        
        # Parse the incoming request body
        body = json.loads(request.body)
        logger.debug(f"Received body: {body}")
        
        # Create an Update object
        update = Update.de_json(body, app.bot)
        
        # Process the update
        await handle_update(update)
        
        return {
            'statusCode': 200,
            'body': json.dumps('OK')
        }
    except Exception as e:
        logger.error(f"Error processing update: {e}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps(f'Internal Server Error: {str(e)}')
        }

def main(request):
    """Main function for Vercel."""
    import asyncio
    return asyncio.run(handler(request))