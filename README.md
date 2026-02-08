# 📊 Hyperliquid Orderbook Density Scanner

Telegram бот для мониторинга плотности ордербуков на бирже Hyperliquid.

## ✨ Возможности

- 🔍 Сканирование плотности ордербуков в реальном времени
- 📱 Telegram алерты при обнаружении крупных объёмов
- ⚙️ Гибкие настройки фильтрации
- 🚀 WebSocket для быстрого получения данных
- 🔒 Шифрование настроек
- 💪 Защита от race conditions и memory leaks

## 🚀 Быстрый Старт

### 1. Установка

```bash
git clone https://github.com/affilete/tgaletr.git
cd tgaletr
pip install -r requirements.txt
```

### 2. Настройка

Создайте `.env` файл из примера:

```bash
cp .env.example .env
```

Отредактируйте `.env`:

```env
BOT_TOKEN=your_telegram_bot_token
OWNER_USER_ID=your_telegram_user_id
DEFAULT_CHAT_ID=your_chat_id
```

### 3. Запуск

```bash
python main.py
```

## 📋 Требования

- Python 3.8+
- Telegram Bot Token (получить у [@BotFather](https://t.me/BotFather))
- Интернет соединение

## 🔧 Настройки

Через Telegram бота:
- `/start` - Запустить бота
- `/settings` - Открыть настройки
- `/status` - Статус сканера

### Настройки фильтрации:

- **Минимальный размер**: $100,000 по умолчанию
- **Расстояние от цены**: 0.5% по умолчанию
- **Приоритетные тикеры**: BTC, ETH, SOL

## 🏗️ Архитектура

- `main.py` - Точка входа, запуск сканера и бота
- `scanner.py` - Логика сканирования и расчёта плотности
- `bot.py` - Telegram бот интерфейс
- `config.py` - Конфигурация Hyperliquid
- `settings_manager.py` - Управление настройками

## 📊 Биржа

- **Hyperliquid** - Perpetual Futures

## 🔒 Безопасность

- Шифрование чувствительных данных (Fernet)
- Rate limiting для Telegram команд
- Input validation
- Защита от SQL injection

## 🧪 Тестирование

```bash
python test_scanner.py
```

## 📄 Лицензия

MIT

## 👨‍💻 Автор

affilete

---

# 📊 Hyperliquid Orderbook Density Scanner (English)

Telegram bot for monitoring orderbook density on Hyperliquid exchange.

## ✨ Features

- 🔍 Real-time orderbook density scanning
- 📱 Telegram alerts for large volume detection
- ⚙️ Flexible filtering settings
- 🚀 WebSocket support for fast data retrieval
- 🔒 Settings encryption
- 💪 Protection against race conditions and memory leaks

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/affilete/tgaletr.git
cd tgaletr
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env`:

```env
BOT_TOKEN=your_telegram_bot_token
OWNER_USER_ID=your_telegram_user_id
DEFAULT_CHAT_ID=your_chat_id
```

### 3. Run

```bash
python main.py
```

## 📋 Requirements

- Python 3.8+
- Telegram Bot Token (get from [@BotFather](https://t.me/BotFather))
- Internet connection

## 🔧 Settings

Via Telegram bot:
- `/start` - Start the bot
- `/settings` - Open settings
- `/status` - Scanner status

### Filter Settings:

- **Minimum Size**: $100,000 by default
- **Distance from Price**: 0.5% by default
- **Priority Tickers**: BTC, ETH, SOL

## 🏗️ Architecture

- `main.py` - Entry point, launches scanner and bot
- `scanner.py` - Scanning logic and density calculation
- `bot.py` - Telegram bot interface
- `config.py` - Hyperliquid configuration
- `settings_manager.py` - Settings management

## 📊 Exchange

- **Hyperliquid** - Perpetual Futures

## 🔒 Security

- Sensitive data encryption (Fernet)
- Rate limiting for Telegram commands
- Input validation
- SQL injection protection

## 🧪 Testing

```bash
python test_scanner.py
```

## 📄 License

MIT

## 👨‍💻 Author

affilete