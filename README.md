# Weather Assistant Bot 🌤️

A Telegram bot that provides weather information, city population data, random historical facts, and images. Built with Python using modern programming practices and OOP principles.

## Features

- 🌍 Current weather information for any city
- 📊 City population statistics
- 📚 Random historical facts with each request
- 🖼️ Random images with each response
- 🔒 Secure key management
- 📝 User request logging

## Prerequisites

- Python 3.11 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- OpenWeatherMap API key
- API Ninjas key

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd customTeleBot
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your private keys:
   - Create a `private_keys` directory
   - Add your API keys in separate files:
     - `private_telegram_key.txt`: Your Telegram Bot Token
     - `private_owm_key.txt`: OpenWeatherMap API key
     - `private_api_ninjas_key.txt`: API Ninjas key

## Project Structure

```
customTeleBot/
├── private_keys/
│   ├── private_telegram_key.txt
│   ├── private_owm_key.txt
│   └── private_api_ninjas_key.txt
├── CustomWeatherBot.py      # Main bot implementation
├── open_weather_map.py      # Weather API integration
├── api_utils.py            # API utilities
├── error_logger.py         # Error logging
├── KeyManagerUtils.py      # Secure key management
└── requirements.txt
```

## Usage

1. Start the bot:
```bash
python CustomWeatherBot.py
```

2. In Telegram, find your bot and start interaction:
   - `/start` - Begin interaction with the bot
   - `/help` - Show available commands
   - Type any city name to get weather information
   - `/stop` - Stop the bot

## Bot Commands

- `/start` - Initialize the bot and get welcome message
- `/help` - Display help information
- `/stop` - Stop the bot
- Any city name - Get weather, population, and historical fact

## Features in Detail

### Weather Information
- Current temperature (Celsius and Fahrenheit)
- Weather condition description
- "Feels like" temperature

### City Information
- Population statistics
- Country information

### Additional Features
- Random historical facts with each weather request
- Random images to accompany responses
- Preserved word filtering
- Error handling and logging

## Security

- Secure key management with proper file permissions
- Private keys stored separately
- Input validation and sanitization

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

[LGPLv3 (?)]

## Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [API Ninjas](https://api-ninjas.com/)