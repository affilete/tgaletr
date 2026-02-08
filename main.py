"""
Main entry point for the Cryptocurrency Density Scanner.
Runs the Telegram bot and scanner concurrently in a single async event loop.
"""

import argparse
import asyncio
import logging
import signal
import sys
from pathlib import Path

from settings_manager import SettingsManager
from scanner import DensityScanner, DensityAlert
from bot import build_bot_app


class GracefulKiller:
    """Handle graceful shutdown on SIGINT and SIGTERM."""
    def __init__(self):
        self.kill_now = False
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
    
    def exit_gracefully(self, signum, frame):
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        self.kill_now = True


def setup_logging():
    """Configure logging to console and file."""
    logger = logging.getLogger()
    if logger.handlers:
        return logger  # Already configured

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler("scanner.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)

    return logger


logger = setup_logging()


async def async_main():
    """Async main entry point."""
    parser = argparse.ArgumentParser(description="Cryptocurrency Density Scanner Bot")
    parser.add_argument("--chat_id", type=str, help="Telegram chat ID for alerts")
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Starting Cryptocurrency Density Scanner")
    logger.info("=" * 60)

    killer = GracefulKiller()

    settings = SettingsManager("settings.json")
    logger.info("Settings loaded")

    if args.chat_id:
        settings.chat_id = args.chat_id
        logger.info(f"Chat ID set from CLI: {args.chat_id}")

    # Log the configured chat ID for debugging
    logger.info(f"Configured Chat ID: {settings.chat_id}")
    logger.info(f"Chat ID type: {type(settings.chat_id).__name__}")

    bot_app = build_bot_app(settings)
    logger.info("Telegram bot initialized")

    alert_queue = asyncio.Queue()

    def alert_callback(alert: DensityAlert):
        """Alert callback with exception handling."""
        try:
            alert_queue.put_nowait(alert)
        except asyncio.QueueFull:
            logger.error(f"Alert queue is full! Dropping alert for {alert.symbol}")
        except Exception as e:
            logger.error(f"Failed to queue alert: {e}")

    async def process_alerts():
        while True:
            alert = await alert_queue.get()
            try:
                message = alert.format_message()
                await bot_app.bot.send_message(
                    chat_id=settings.chat_id,
                    text=message,
                    parse_mode="HTML",
                    disable_web_page_preview=True,
                )
                logger.debug(f"Alert sent: {alert.symbol}")
            except Exception as e:
                logger.error(f"Error sending alert to chat {settings.chat_id}: {e}")
                # Log additional details for debugging
                if "chat not found" in str(e).lower():
                    logger.error(
                        f"Chat {settings.chat_id} not found. "
                        "Please ensure: 1) Bot is added to the chat, "
                        "2) Chat ID is correct (use @userinfobot), "
                        "3) Bot has permission to send messages"
                    )

    scanner = DensityScanner(settings, alert_callback)

    async with bot_app:
        await bot_app.start()
        
        # Validate chat access before starting scanner
        try:
            logger.info(f"Validating access to chat {settings.chat_id}...")
            # Try to get chat info to verify bot has access
            chat = await bot_app.bot.get_chat(settings.chat_id)
            logger.info(f"✅ Successfully connected to chat: {chat.title or chat.id}")
            logger.info(f"   Chat type: {chat.type}")
            
            # Additional check: try to send a test message (optional, commented out by default)
            # await bot_app.bot.send_message(
            #     chat_id=settings.chat_id,
            #     text="✅ Bot started and connected successfully",
            #     parse_mode="HTML"
            # )
            
        except Exception as e:
            logger.error(f"❌ Failed to access chat {settings.chat_id}: {e}")
            logger.error(
                "Please check:\n"
                "  1. Chat ID is correct (use @userinfobot to get it)\n"
                "  2. Bot is added to the chat/group\n"
                "  3. Bot has permission to send messages\n"
                f"  4. For groups, Chat ID should be negative (e.g., -1003892216818)\n"
                f"  Current Chat ID: {settings.chat_id}"
            )
            # Don't exit, allow bot to start but warn user
            logger.warning("Bot will continue but alerts may fail to send")
        
        await bot_app.updater.start_polling(
            allowed_updates=["message", "callback_query"]
        )
        logger.info("Bot is ready! Use /start to begin")

        scanner_task = asyncio.create_task(scanner.run())
        alert_task = asyncio.create_task(process_alerts())

        try:
            # Monitor for shutdown signal
            while not killer.kill_now:
                await asyncio.sleep(1)
                if scanner_task.done():
                    break
            
            if killer.kill_now:
                logger.info("Shutdown requested, stopping tasks...")
        
        except asyncio.CancelledError:
            pass
        finally:
            logger.info("Shutting down...")
            scanner.stop()
            
            scanner_task.cancel()
            alert_task.cancel()
            
            await asyncio.gather(
                scanner_task,
                alert_task,
                return_exceptions=True
            )
            
            await bot_app.updater.stop()
            await bot_app.stop()
            await bot_app.shutdown()
            logger.info("Shutdown complete")


if __name__ == "__main__":
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received, exiting")
