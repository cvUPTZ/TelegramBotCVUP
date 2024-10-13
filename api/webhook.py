import json
import logging
from telegram import Update
from bot.bot import main  # Make sure this import is correct

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the application
app = main()

async def handler(request):
    """Vercel serverless function handler."""
    try:
        logger.debug("Handler function called")
        
        # Parse the incoming request body
        body = await request.json()
        logger.debug(f"Received body: {body}")
        
        # Create an Update object
        update = Update.de_json(body, app.bot)
        
        # Process the update
        await app.process_update(update)
        
        return {
            'statusCode': 200,
            'body': 'OK'
        }
    except Exception as e:
        logger.error(f"Error processing update: {e}")
        return {
            'statusCode': 500,
            'body': f'Internal Server Error: {str(e)}'
        }

def entrypoint(request):
    """Entry point for Vercel."""
    return handler(request)