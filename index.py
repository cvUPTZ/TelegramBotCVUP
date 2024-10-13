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

# import asyncio

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        update = Update.de_json(json.loads(post_data), application.bot)
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.handle_update(update))
        loop.close()

        self.send_response(200)
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
