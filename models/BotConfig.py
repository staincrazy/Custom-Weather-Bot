from dataclasses import dataclass


@dataclass
class BotConfig:
    """Configuration settings for the WeatherBot"""
    telegram_key_file: str = 'private_telegram_key.txt'
    preserved_words: list[str] = None
    messages: dict[str, str] = None

    @property
    def telegram_key_path(self) -> str:
        return self.telegram_key_file

    def __post_init__(self):
        if self.preserved_words is None:
            self.preserved_words = [
                'orgrimar', 'Orgrimmar', 'orgrimmar', 'Orgri', 'Orgrimar',
                'лампочка', 'lampo4ka', 'lampochka', 'deepthroatovo'
                'assenburg', 'assachussats', 'missititty'
            ]

        if self.messages is None:
            self.messages = {
                'start': (
                    "👋 Hi! I'm your Weather Assistant Bot!\n\n"
                    "I can help you with:\n"
                    "🌤️ Current weather in any city\n"
                    "📊 City population information\n"
                    "📚 Random historical facts\n"
                    "🖼️ Random images\n\n"
                    "Just type any city name to get started!"
                ),
                'help': (
                    "🤖 Here's what I can do:\n\n"
                    "1️⃣ Get weather - just type a city name\n"
                    "2️⃣ View population stats - included with weather\n"
                    "3️⃣ Learn history - random event with each request\n"
                    "4️⃣ See images - automatic with each weather request\n\n"
                    "Commands:\n"
                    "/start - Start the bot\n"
                    "/help - Show this help message\n"
                    "/stop - Stop the bot"
                ),
                'stop': (
                    "🌟 Thanks for using Weather Assistant Bot!\n"
                    "Come back anytime - just type /start to begin again."
                ),
                'error': (
                    "⚠️ Oops! Something went wrong...\n"
                    "Please make sure to:\n"
                    "- Use English characters only\n"
                    "- Type a valid city name\n"
                    "Try again or type /help for assistance."
                ),
                'preserved_word': (
                    "⛔ This word is no longer supported.\n"
                    "Please use regular city names instead."
                ),
                'response_template': (
                    "🌍 Weather section:\n{weather_info}\n\n"
                    "👥 City population info:\n{population_info}\n\n"
                    "📜 Random historical event:\n{random_event}\n\n"
                    "🖼️ Below we have a random image for you. Enjoy!"
                )
            }
