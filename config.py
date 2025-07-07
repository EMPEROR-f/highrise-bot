"""
Bot Configuration
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class BotConfig:
    """Bot configuration settings"""
    bot_token: str
    room_id: str
    max_message_length: int = 256
    loop_interval: float = 6.0
    command_prefix: str = "!"
    
    def __post_init__(self):
        """Validate configuration after initialization"""
        if not self.bot_token:
            raise ValueError("Bot token is required")
        if not self.room_id:
            raise ValueError("Room ID is required")
        if self.max_message_length <= 0:
            raise ValueError("Max message length must be positive")
        if self.loop_interval <= 0:
            raise ValueError("Loop interval must be positive")
          
