from services.CustomWeatherBot import create_bot
import os
from threading import Thread
from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return "Bot is running!"


def run_bot():
    bot = create_bot()
    bot.run()


if __name__ == '__main__':
    # Start bot in a separate thread
    bot_thread = Thread(target=run_bot)
    bot_thread.start()

    # Start Flask on the port Render provides
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)