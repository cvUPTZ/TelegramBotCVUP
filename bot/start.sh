
#!/bin/bash

# Set up virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/Scripts/activate

# Install required packages
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the bot
echo "Starting the bot..."
python telegram_bot.py
