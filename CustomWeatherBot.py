from typing import Optional
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from ErrorLogger import logEvent
from UserRequest import UserRequestLogger
from WeatherService import OpenWeatherMapAPI
from ApiUtils import APIService
from KeyManagerUtils import KeyManager
from models.BotConfig import BotConfig


class WeatherBot:
    """Modern implementation of Weather Bot using python-telegram-bot"""

    def __init__(
            self,
            config: Optional[BotConfig] = None,
            weather_api: Optional[OpenWeatherMapAPI] = None,
            api_service: Optional[APIService] = None,
            key_manager: Optional[KeyManager] = None
    ):
        """Initialize bot with its dependencies"""
        self.config = config or BotConfig()
        self.weather_api = weather_api or OpenWeatherMapAPI()
        self.api_service = api_service or APIService()
        self.key_manager = key_manager or KeyManager()
        self.token = self.key_manager.get_key(self.config.telegram_key_path)
        self.user_logger = UserRequestLogger()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command"""
        await update.message.reply_text(self.config.messages['start'])

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command"""
        await update.message.reply_text(self.config.messages['help'])

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle stop command"""
        await update.message.reply_text(self.config.messages['stop'])

    async def handle_city(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle city messages"""
        self.user_logger.log_request(update)
        try:
            city = update.message.text

            if city.lower() in self.config.preserved_words:
                await update.message.reply_text(self.config.messages['preserved_word'])
                return

            # Get all required information
            weather_info = self.weather_api.get_formatted_weather(city)
            population_info = self.api_service.get_city_population_info(city)
            random_event = self.api_service.get_random_event()

            # Format response using template
            combined_reply = self.config.messages['response_template'].format(
                weather_info=weather_info,
                population_info=population_info,
                random_event=random_event
            )

            # Send text response
            await update.message.reply_text(combined_reply)

            # Get and send random image
            self.api_service.get_random_image()
            await update.message.reply_photo(photo=open("img.jpg", 'rb'))

        except Exception as e:
            await update.message.reply_text(self.config.messages['error'])
            logEvent(e.__cause__, self.handle_city, user_input=update.message.text)

    def run(self) -> None:
        """Run the bot"""
        try:
            # Create application
            application = Application.builder().token(self.token).build()

            # Add handlers
            application.add_handler(CommandHandler("start", self.start))
            application.add_handler(CommandHandler("help", self.help))
            application.add_handler(CommandHandler("stop", self.stop))

            # Handle all non-command messages as city names
            application.add_handler(
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_city)
            )

            # Start the bot
            print("Starting Weather Assistant Bot...")
            application.run_polling()

        except Exception as e:
            print(f"Error starting bot: {e}")


def create_bot() -> WeatherBot:
    """Factory function to create a configured bot instance"""
    return WeatherBot()


if __name__ == '__main__':
    bot = create_bot()
    bot.run()