#!/usr/bin/env python3
"""
Highrise Emote Bot - Main Entry Point
"""

import asyncio
import logging
import os
from bot import HighriseEmoteBot
from config import BotConfig
from keep_alive import keep_alive

keep_alive()  # ✅ Call once here

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def main():
    try:
        bot_token = os.getenv("HIGHRISE_BOT_TOKEN", "")
        room_id = os.getenv("HIGHRISE_ROOM_ID", "")

        if not bot_token:
            logger.error("HIGHRISE_BOT_TOKEN environment variable is required")
            return

        if not room_id:
            logger.error("HIGHRISE_ROOM_ID environment variable is required")
            return

        config = BotConfig(
            bot_token=bot_token,
            room_id=room_id
        )

        bot = HighriseEmoteBot(config)
        logger.info("Starting Highrise Emote Bot...")

        await bot.start()

    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        raise e   # ✅ FIXED LINE

if __name__ == "__main__":
    asyncio.run(main())
    
