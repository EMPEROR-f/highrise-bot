"""
Highrise Emote Bot - Main Bot Class
"""

import asyncio
import logging
from typing import Dict, Optional, List
from highrise import BaseBot, User, Position, AnchorPosition
from highrise.__main__ import *
from emotes import EmoteManager
from config import BotConfig
from utils import MessageSplitter, CommandParser

logger = logging.getLogger(__name__)

class HighriseEmoteBot(BaseBot):
    """Main bot class handling Highrise room interactions"""
    
    def __init__(self, config: BotConfig):
        super().__init__()
        self.config = config
        self.emote_manager = EmoteManager()
        self.message_splitter = MessageSplitter(max_length=config.max_message_length)
        self.command_parser = CommandParser(prefix=config.command_prefix)
        
        # Loop management
        self.active_loops: Dict[str, Dict] = {}  # user_id -> loop_info
        self.loop_tasks: Dict[str, asyncio.Task] = {}  # user_id -> task
        
        # Repeat message system
        self.repeat_message = ""
        self.repeat_interval = 120  # default 120 seconds
        self.repeat_task: Optional[asyncio.Task] = None
        self.repeat_active = False
        
        # Room info
        self.room_name = ""
        
        # Moderation system
        self.moderators = set()  # Store moderator usernames
        self.super_admins = {"SHIVAM_00", "intothesky"}  # Super admin usernames
        
        # Teleport positions (set by mods using !setf1, !setf2, etc)
        self.teleport_positions = {
            'f1': None, 'f2': None, 'f3': None, 'f4': None, 'f5': None,
            'f6': None, 'f7': None, 'f8': None, 'f9': None, 'f10': None,
            'vip': None
        }
        
        # Fun command data
        self.rizz_lines = [
            "I'd like to take you to the movies but they don't let you bring your own snacks in.",
            "No pen, no paper but you still draw my attention.",
            "All the good pick up lines are taken but you aren't.",
            "Excuse me while I delete my dating apps.",
            "This must be a museum because you're a work of art.",
            "Are you WiFi? Because I feel a connection.",
            "I'm not even playing cards but somehow I pulled a Queen.",
            "You must be a dog person because you look fetching.",
            "I didn't even have to run to catch these butterflies.",
            "I'm lost. Can you give me directions to your heart?",
            "Well, here I am. What are your other two wishes?",
            "Hey, how was heaven when you left it?"
        ]
        
        self.roast_lines = [
            "I look at you and think, 'Two billion years of evolution, for this?'",
            "I am jealous of all the people that have never met you.",
            "I consider you my sun. Now please get 93 million miles away from here.",
            "If laughter is the best medicine, your face must be curing the world.",
            "You're not simply a drama queen/king. You're the whole royal family.",
            "I was thinking about you today. It reminded me to take out the trash.",
            "You are the human version of cramps.",
            "You haven't changed since the last time I saw you. You really should.",
            "If ignorance is bliss, you must be the happiest person on Earth.",
            "Oh, sorry, did the middle of my sentence interrupt the beginning of yours?"
        ]
        
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "Why don't skeletons fight each other? They don't have the guts.",
            "What do you call a fake noodle? An impasta!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "What do you call a fish wearing a bowtie? Sofishticated!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What's the best thing about Switzerland? I don't know, but the flag is a big plus.",
            "Why did the math book look so sad? Because it had too many problems!",
            "What do you call a sleeping bull? A bulldozer!",
            "Why don't oysters share? Because they're shellfish!",
            "What did one wall say to the other wall? I'll meet you at the corner!",
            "Why don't scientists trust stairs? Because they're always up to something!",
            "What do you call cheese that isn't yours? Nacho cheese!",
            "Why did the coffee file a police report? It got mugged!",
            "What's orange and sounds like a parrot? A carrot!",
            "Why don't programmers like nature? It has too many bugs!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why did the bicycle fall over? Because it was two tired!",
            "What's the difference between a fish and a piano? You can't tuna fish!"
        ]
        
    async def on_start(self, session_metadata):
        """Called when bot starts"""
        logger.info("Bot connected to Highrise")
        try:
            # Try to get room information
            room_info = await self.highrise.get_room_users()
            
            # Try to get the actual room name from session metadata
            try:
                if hasattr(session_metadata, 'room_info') and hasattr(session_metadata.room_info, 'room_name'):
                    self.room_name = session_metadata.room_info.room_name
                else:
                    # Get room name from session metadata
                    self.room_name = getattr(session_metadata, 'room_name', None) or "this amazing room"
            except:
                self.room_name = "this amazing room"
            
            logger.info(f"Connected to room: {self.room_name}")
        except Exception as e:
            logger.error(f"Error on bot start: {e}")
            self.room_name = "this amazing room"
    
    async def on_user_join(self, user: User, position: Position | AnchorPosition):
        """Called when a user joins the room"""
        try:
            welcome_message = f"Welcome to the {self.room_name} @{user.username}"
            await self.highrise.chat(welcome_message)
            logger.info(f"Welcomed user: {user.username}")
        except Exception as e:
            logger.error(f"Error sending welcome message: {e}")
    
    async def on_chat(self, user: User, message: str):
        """Called when a user sends a message"""
        try:
            message = message.strip()
            
            # Check for direct teleport commands (f1-f10) without !
            teleport_commands = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10']
            if message.lower() in teleport_commands:
                await self.handle_teleport_command(user, message.lower())
                return
            
            # Check for VIP teleport (only for moderators)
            if message.lower() == 'vip':
                if self.is_moderator(user.username):
                    await self.handle_teleport_command(user, 'vip')
                else:
                    await self.send_error_message("Only moderators can use VIP teleport!")
                return
            
            # Check for direct emote commands (without !)
            message_parts = message.split()
            
            # Check if it's a number (for numbered emotes)
            if message.strip().isdigit():
                emote_number = int(message.strip())
                emote_info = self.emote_manager.find_emote_by_number(emote_number)
                if emote_info:
                    await self.play_emote(user, emote_info)
                    return
            
            # Check for mod-controlled emotes (number @username)
            if len(message_parts) == 2 and message_parts[1].startswith('@') and self.is_moderator(user.username):
                emote_identifier = message_parts[0]
                target_username = message_parts[1].replace('@', '')
                
                # Only try by number for mod emotes
                if emote_identifier.isdigit():
                    emote_info = self.emote_manager.find_emote_by_number(int(emote_identifier))
                    if emote_info:
                        await self.handle_mod_emote_command(user, target_username, emote_info)
                        return
            
            # Remove regular emote by name - only numbers work now
            
            # Check if message is a ! command
            if not message.startswith('!'):
                return
                
            # Parse command
            command_data = self.command_parser.parse(message)
            if not command_data:
                return
                
            command = command_data['command']
            args = command_data['args']
            
            # Handle commands
            if command == 'help':
                await self.handle_help_command(user)
            elif command == 'emotes':
                await self.handle_emotes_command(user)
            elif command == 'loop':
                await self.handle_loop_command(user, args)
            elif command == 'stop':
                await self.handle_stop_command(user)
            elif command.startswith('setf') or command == 'setvip':
                await self.handle_set_teleport_command(user, command, args)
            elif command == 'summon':
                await self.handle_summon_command(user, args)
            elif command == 'goto':
                await self.handle_goto_command(user, args)
            elif command == 'addmod':
                await self.handle_addmod_command(user, args)
            elif command == 'delmod':
                await self.handle_delmod_command(user, args)
            elif command == 'kick':
                await self.handle_kick_command(user, args)
            elif command == 'rizz':
                await self.handle_rizz_command(user, args)
            elif command == 'ship':
                await self.handle_ship_command(user, args)
            elif command == 'roast':
                await self.handle_roast_command(user, args)
            elif command == 'straightmeter':
                await self.handle_straightmeter_command(user)
            elif command == 'iq':
                await self.handle_iq_command(user, args)
            elif command == 'hatepercentage':
                await self.handle_hatepercentage_command(user, args)
            elif command == 'lovepercentage':
                await self.handle_lovepercentage_command(user, args)
            elif command == 'spam':
                await self.handle_spam_command(user, args)
            elif command == 'tele':
                await self.handle_tele_command(user, args)
            elif command == 'joke':
                await self.handle_joke_command(user)
            elif command == 'repeat':
                await self.handle_repeat_command(user, args)
            elif command == 'off':
                await self.handle_off_command(user)
            elif command == 'modlist':
                await self.handle_modlist_command(user)
            else:
                # Check if it's an emote command
                await self.handle_emote_command(user, command, args)
                
        except Exception as e:
            logger.error(f"Error handling chat message: {e}")
            await self.send_error_message("Sorry, something went wrong processing your command.")
    
    async def handle_help_command(self, user: User):
        """Handle the !help command"""
        try:
            # Part 1: Basic Commands (shorter)
            help_part1 = "🤖 **Help (1/3)** 🤖\n**Emotes:** 1-84 (e.g., 1, 25, 84)\n**Teleport:** f1-f10, vip (mods)\n**Loop:** !loop <number>, !stop\n**List:** !emotes"
            
            # Part 2: Fun Commands (shorter)
            help_part2 = "🤖 **Help (2/3)** 🤖\n**Fun:** !rizz @user, !ship @u1 @u2\n**More:** !roast @user, !iq @user\n**Other:** !joke, !straightmeter\n**Spam:** !spam <msg> <num>"
            
            # Part 3: Moderator Commands (shorter)
            help_part3 = "🤖 **Help (3/3)** 🤖\n**Info:** Basic commands for all users"
            
            if self.is_moderator(user.username):
                if user.username in self.super_admins:
                    help_part3 = "🤖 **Help (3/3)** 🤖\n**Mod:** number @user, !summon @user\n**Admin:** !setf1-f10, !setvip, !delmod, !kick\n**Staff:** !modlist"
                else:
                    help_part3 = "🤖 **Help (3/3)** 🤖\n**Mod:** number @user, !summon @user\n**Movement:** !goto @user, !tele @user\n**Staff:** !modlist"
            
            # Send all parts as whispers
            await self.send_whisper(user, help_part1)
            await asyncio.sleep(1.0)
            
            await self.send_whisper(user, help_part2)
            await asyncio.sleep(1.0)
            
            await self.send_whisper(user, help_part3)
            
            # Send confirmation in public chat
            await self.send_message(f"📩 Help sent to {user.username}!")
            
        except Exception as e:
            logger.error(f"Error handling help command: {e}")
            await self.send_error_message("Failed to send help information.")
    
    async def handle_emotes_command(self, user: User):
        """Handle the !emotes command"""
        try:
            # Get formatted emote list with numbers
            formatted_list = self.emote_manager.get_emote_list_formatted()
            
            # Split the formatted list into whisper-friendly chunks
            lines = formatted_list.split('\n')
            current_chunk = []
            chunk_count = 0
            
            for line in lines:
                current_chunk.append(line)
                
                # Send chunk when it gets too big (around 200 characters)
                chunk_text = '\n'.join(current_chunk)
                if len(chunk_text) > 200 or line == '':  # Empty line indicates category end
                    if current_chunk:
                        chunk_count += 1
                        await self.send_whisper(user, f"📋 **Emotes (Part {chunk_count})** 📋\n{chunk_text.strip()}")
                        await asyncio.sleep(0.6)
                    current_chunk = []
            
            # Send any remaining content
            if current_chunk:
                chunk_count += 1
                remaining_text = '\n'.join(current_chunk).strip()
                await self.send_whisper(user, f"📋 **Emotes (Part {chunk_count})** 📋\n{remaining_text}")
            
            # Send confirmation in public chat
            await self.send_message(f"📩 Emote list sent to {user.username} via whisper!")
            
        except Exception as e:
            logger.error(f"Error handling emotes command: {e}")
            await self.send_error_message("Failed to retrieve emote list.")
    
    async def handle_loop_command(self, user: User, args: List[str]):
        """Handle the !loop command"""
        if not args:
            await self.send_whisper(user, "❌ Please specify an emote NUMBER to loop. Example: !loop 1")
            return
        
        emote_identifier = args[0]
        
        # Check if user already has a loop running
        if user.id in self.active_loops:
            await self.send_whisper(user, "❌ You already have a loop running. Use !stop first.")
            return
        
        # Find the emote by number only
        emote_info = None
        if emote_identifier.isdigit():
            emote_info = self.emote_manager.find_emote_by_number(int(emote_identifier))
        
        if not emote_info:
            await self.send_whisper(user, f"❌ Emote number '{emote_identifier}' not found. Use !emotes to see available emotes.")
            return
        
        # Start the loop
        await self.start_emote_loop(user, emote_info)
    
    async def handle_stop_command(self, user: User):
        """Handle the !stop command"""
        if user.id not in self.active_loops:
            await self.send_whisper(user, "❌ You don't have any emote loops running.")
            return
        
        await self.stop_emote_loop(user)
    
    async def handle_emote_command(self, user: User, command: str, args: List[str]):
        """Handle emote commands like !dance, !wave, etc."""
        emote_info = self.emote_manager.find_emote(command)
        if not emote_info:
            # Not a valid emote command
            await self.send_error_message(f"Unknown command: !{command}. Use !help for available commands.")
            return
        
        # Play the emote once
        await self.play_emote(user, emote_info)
    
    async def start_emote_loop(self, user: User, emote_info: Dict):
        """Start looping an emote for a user"""
        try:
            # Store loop info
            self.active_loops[user.id] = {
                'user': user,
                'emote': emote_info,
                'start_time': asyncio.get_event_loop().time()
            }
            
            # Create and start the loop task
            task = asyncio.create_task(self.emote_loop_task(user, emote_info))
            self.loop_tasks[user.id] = task
            
            await self.send_whisper(user, f"✅ Started looping: {emote_info['name']} 🔄")
            logger.info(f"Started emote loop for {user.username}: {emote_info['name']}")
            
        except Exception as e:
            logger.error(f"Error starting emote loop: {e}")
            await self.send_whisper(user, "❌ Failed to start emote loop.")
    
    async def stop_emote_loop(self, user: User):
        """Stop the emote loop for a user"""
        try:
            if user.id in self.loop_tasks:
                self.loop_tasks[user.id].cancel()
                del self.loop_tasks[user.id]
            
            if user.id in self.active_loops:
                emote_name = self.active_loops[user.id]['emote']['name']
                del self.active_loops[user.id]
                await self.send_whisper(user, f"✅ Stopped looping: {emote_name} ⏹️")
                logger.info(f"Stopped emote loop for {user.username}")
            
        except Exception as e:
            logger.error(f"Error stopping emote loop: {e}")
    
    async def emote_loop_task(self, user: User, emote_info: Dict):
        """Background task for emote looping"""
        try:
            while user.id in self.active_loops:
                await self.play_emote(user, emote_info)
                await asyncio.sleep(self.config.loop_interval)  # Wait configured interval between emotes
        except asyncio.CancelledError:
            logger.info(f"Emote loop cancelled for {user.username}")
        except Exception as e:
            logger.error(f"Error in emote loop task: {e}")
            if user.id in self.active_loops:
                del self.active_loops[user.id]
    
    async def play_emote(self, user: User, emote_info: Dict):
        """Play an emote for a user"""
        try:
            # Get user position
            room_users = await self.highrise.get_room_users()
            user_position = None
            
            try:
                if hasattr(room_users, 'content'):
                    for room_user, position in room_users.content:
                        if room_user.id == user.id:
                            user_position = position
                            break
                else:
                    # Try direct iteration if it's a list/tuple
                    for room_user, position in room_users:
                        if room_user.id == user.id:
                            user_position = position
                            break
            except Exception as parse_error:
                logger.warning(f"Could not parse room users response: {
