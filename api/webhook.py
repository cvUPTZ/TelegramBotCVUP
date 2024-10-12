from http.server import BaseHTTPRequestHandler
import json
import os
from bot.bot import main

# Initialize the bot
application = main()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        update = Update.de_json(json.loads(post_data), application.bot)

        asyncio.run(webhook(update, None))

        self.send_response(200)
        self.end_headers()
        return