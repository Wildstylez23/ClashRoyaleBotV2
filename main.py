"""
Main script to initialize and run the bot framework.
"""
import logging
import sys
import os

# Configure basic logging for the entire application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Add the project's root directory to the Python path to allow imports from
# 'core', 'vision', 'strategy', 'emulator' as top-level packages.
# This assumes main.py is located directly within the project root (e.g., D:\bot_v2\main.py).
project_root_dir = os.path.dirname(os.path.abspath(__file__))
if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir)

# Import the BotLoop from the core package
from core.bot_loop import BotLoop

def main():
    """
    Initializes and starts the bot loop.
    """
    logging.info("Starting bot application...")
    bot = BotLoop()
    try:
        bot.start()
    except KeyboardInterrupt:
        logging.info("Bot stopped by user (KeyboardInterrupt).")
    finally:
        bot.stop() # Ensure the bot stops cleanly

if __name__ == "__main__":
    main()
