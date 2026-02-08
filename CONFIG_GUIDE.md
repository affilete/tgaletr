# Configuration Guide

## Overview

The bot now uses a simplified configuration system that reads all settings from the `.env` file only. No more JSON files or encryption complexity!

## Setup

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your values:**
   ```env
   BOT_TOKEN=your_bot_token_from_botfather
   OWNER_USER_ID=your_telegram_user_id
   CHAT_ID=-5017751590  # For groups: negative number
   DISTANCE_PCT=3.0
   MIN_SIZE=1000000
   ALERTS_ENABLED=true
   ```

## Required Configuration

### BOT_TOKEN
- Get from [@BotFather](https://t.me/BotFather) on Telegram
- Format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### OWNER_USER_ID
- Your Telegram user ID
- Get from [@userinfobot](https://t.me/userinfobot)
- Format: positive integer (e.g., `8329204739`)

### CHAT_ID
- **CRITICAL**: This is where alerts are sent
- **For groups/supergroups**: Use negative number (e.g., `-5017751590`)
- **For private chats**: Use positive number (e.g., `123456789`)
- How to get:
  1. Add [@userinfobot](https://t.me/userinfobot) to your group
  2. It will show the group's Chat ID
  3. Use this exact number in your `.env` file

## Optional Configuration

### DISTANCE_PCT
- Distance from current price to look for density (percentage)
- Default: `3.0`

### MIN_SIZE
- Minimum cumulative volume to trigger an alert (USDT)
- Default: `1000000`

### ALERTS_ENABLED
- Enable or disable alerts
- Values: `true` or `false`
- Default: `true`

## Startup Verification

When you start the bot with `python main.py`, you should see:

```
============================================================
Starting Cryptocurrency Density Scanner
============================================================
Settings loaded from .env
Configured Chat ID: -5017751590 (type: int)
Bot Token: 8397626686:AAF... (truncated)
Owner ID: 8329204739
Alerts Enabled: True
Telegram bot initialized
Validating access to chat -5017751590...
✅ Successfully connected to chat: [Your Group Name]
   Chat type: supergroup
Bot is ready! Use /start to begin
```

## Troubleshooting

### "Chat not found" error
1. **Verify Chat ID is correct**: Use [@userinfobot](https://t.me/userinfobot) to get the exact ID
2. **For groups**: Chat ID must be negative (e.g., `-5017751590`)
3. **Bot must be in the chat**: Add your bot to the group/channel
4. **Bot needs permissions**: Ensure bot can send messages

### Bot doesn't start
1. Check `.env` file exists in the project root
2. Verify all required variables are set
3. Make sure Chat ID is an integer (no quotes)
4. Check bot token is valid

## Migration from Old System

If you're upgrading from the old system with `settings.json`:

1. The bot no longer uses `settings.json` - all settings are in `.env`
2. No encryption key needed - removed for simplicity
3. CLI arguments for chat_id are removed - use `.env` only
4. Settings changes via bot commands are in-memory only (not persisted)

## Security Notes

- `.env` file is in `.gitignore` - never commit it
- Bot token and Chat ID are sensitive - keep them private
- Share `.env.example` but never `.env` itself
