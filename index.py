# index.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import asyncio
from telegram import Update
from bot.bot import main  # Importing the main function from bot

# Set up logging
logging.basicConfig(level=logging.INFO)

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
        # Respond with method not allowed for GET requests
        logging.warning("Received unsupported GET request.")
        self.send_response(405)  # Method Not Allowed
        self.end_headers()

# Initialize the application globally
application = main()  # This creates the application instance

# Main entry point
if __name__ == "__main__":
    # Start the HTTP server
    server_address = ('', 8000)  # Change to your desired port
    httpd = HTTPServer(server_address, WebhookHandler)
    logging.info('Starting webhook server...')
    httpd.serve_forever()
