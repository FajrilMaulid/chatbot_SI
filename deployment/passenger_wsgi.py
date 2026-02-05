import sys
import os

# Path to Python interpreter in virtual environment
# IMPORTANT: Update this path based on your actual cPanel environment
# You can find the correct path in cPanel → Setup Python App
INTERP = os.path.expanduser("~/virtualenv/chatbot_si/3.9/bin/python3")

# Restart interpreter if not using virtualenv
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Add project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Import Flask app
# The 'application' variable name is required by Passenger
from app import app as application

# Passenger compatibility
if __name__ == '__main__':
    application.run()
