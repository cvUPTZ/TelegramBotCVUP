from http.server import BaseHTTPRequestHandler
import json
import logging
import asyncio
from telegram import Update
from bot.bot import main

logging.basicConfig(level=logging.DEBUG)  # Changed to DEBUG for more detailed logs
application = main()

class WebhookHandler(BaseHTTPRequestHandler):
    async def handle_update(self, update: Update):
        await application.process_update(update)

    def do_POST(self):
        try:
            # Verify the request
            secret_token = self.headers.get('X-Telegram-Bot-Api-Secret-Token')
            if secret_token != 'YOUR_SECRET_TOKEN':  # Replace with your actual secret token
                logging.warning("Unauthorized request attempt")
                self.send_error(403, "Unauthorized")
                return

            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            logging.debug(f"Received data: {post_data}")  # Log the received data
            
            update = Update.de_json(json.loads(post_data), application.bot)
            asyncio.run(self.handle_update(update))
        except Exception as e:
            logging.error(f"Error processing update: {e}", exc_info=True)
        finally:
            self.send_response(200)
            self.end_headers()

    def do_GET(self):
        logging.info("Received GET request.")
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Webhook is active. POST requests are required for Telegram updates.")

handler = WebhookHandler