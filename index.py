from http.server import BaseHTTPRequestHandler
import json
import logging
import asyncio
from telegram import Update
from bot.bot import main  # Make sure this import is correct and 'main' returns an Application instance.

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the bot application
application = main()  # Ensure this returns an Application instance.

class WebhookHandler(BaseHTTPRequestHandler):
    async def handle_update(self, update: Update):
        # Process the incoming update
        await application.process_update(update)

    def do_POST(self):
        try:
            # Read the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            update = Update.de_json(json.loads(post_data), application.bot)

            # Handle the update asynchronously
            asyncio.run(self.handle_update(update))

            # Send a successful response
            self.send_response(200)
            self.end_headers()
        except Exception as e:
            # Log any error that occurs
            logging.error(f"Error processing update: {e}")
            self.send_response(500)
            self.end_headers()

    def do_GET(self):
        # Handle GET requests gracefully
        logging.info("Received a GET request.")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Webhook server is running, but this endpoint only accepts POST requests.")

# Expose the WebhookHandler as the handler for Vercel
handler = WebhookHandler
