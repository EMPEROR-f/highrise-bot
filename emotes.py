"""
Emote Management System
"""

from typing import Dict, List, Optional

class EmoteManager:
    """Manages the emote database and operations"""
    
    def __init__(self):
        self.emotes = self._load_emotes()
        self.emote_by_name = {emote['name'].lower(): emote for emote in self.emotes}
        self.emote_by_id = {str(emote['id']): emote for emote in self.emotes}
    
    def _load_emotes(self) -> List[Dict]:
        """Load the complete list of free emotes"""
        return [
            # Action emotes
            {"id": "idle-loop-sitfloor", "name": "sit", "category": "action"},
            {"id": "idle-enthusiastic", "name": "enthused", "category": "emotion"},
            {"id": "emote-yes", "name": "yes", "category": "gesture"},
            {"id": "emote-wave", "name": "wave", "category": "greeting"},
            {"id": "emote-tired", "name": "tired", "category": "emotion"},
            {"id": "emote-snowball", "name": "snowball", "category": "fun"},
            {"id": "emote-snowangel", "name": "snowangel", "category": "fun"},
            {"id": "emote-shy", "name": "shy", "category": "emotion"},
            {"id": "emote-sad", "name": "sad", "category": "emotion"},
            {"id": "emote-no", "name": "no", "category": "gesture"},
            {"id": "emote-model", "name": "model", "category": "pose"},
            {"id": "emote-lust", "name": "flirtywave", "category": "greeting"},
            {"id": "emote-laughing", "name": "laugh", "category": "emotion"},
            {"id": "emote-kiss", "name": "kiss", "category": "emotion"},
            {"id": "emote-hot", "name": "sweating", "category": "emotion"},
            {"id": "emote-hello", "name": "hello", "category": "greeting"},
            {"id": "emote-greedy", "name": "greedy", "category": "emotion"},
            {"id": "emote-exasperatedb", "name": "facepalm", "category": "gesture"},
            {"id": "emote-curtsy", "name": "curtsy", "category": "greeting"},
            {"id": "emote-confused", "name": "confusion", "category": "emotion"},
            {"id": "emote-charging", "name": "charging", "category": "action"},
            {"id": "emote-bow", "name": "bow", "category": "greeting"},
            {"id": "emoji-thumbsup", "name": "thumbsup", "category": "gesture"},
            {"id": "emoji-gagging", "name": "tummyache", "category": "emotion"},
            {"id": "emoji-flex", "name": "flex", "category": "pose"},
            {"id": "emoji-cursing", "name": "cursing", "category": "emotion"},
            {"id": "emoji-celebrate", "name": "raisetheroof", "category": "celebration"},
            {"id": "emoji-angry", "name": "angry", "category": "emotion"},
            
            # Dance emotes
            {"id": "dance-tiktok8", "name": "savagedance", "category": "dance"},
            {"id": "dance-tiktok2", "name": "dontstartnow", "category": "dance"},
            {"id": "dance-shoppingcart", "name": "letsgo", "category": "dance"},
            {"id": "dance-russian", "name": "russian", "category": "dance"},
            {"id": "dance-pennywise", "name": "pennys", "category": "dance"},
            {"id": "dance-macarena", "name": "macarena", "category": "dance"},
            {"id": "dance-blackpink", "name": "kpop", "category": "dance"},
            {"id": "dance-jinglebell", "name": "jinglebell", "category": "dance"},
            {"id": "dance-zombie", "name": "zombie", "category": "dance"},
            {"id": "dance-pinguin", "name": "penguin", "category": "dance"},
            {"id": "dance-creepypuppet", "name": "creepypuppet", "category": "dance"},
            {"id": "dance-tiktok9", "name": "tiktok9", "category": "dance"},
            {"id": "dance-weird", "name": "weird", "category": "dance"},
            {"id": "dance-tiktok10", "name": "tiktok10", "category": "dance"},
            {"id": "dance-icecream", "name": "icecream", "category": "dance"},
            {"id": "dance-wrong", "name": "wrong", "category": "dance"},
            {"id": "idle-dance-tiktok4", "name": "tiktok4", "category": "dance"},
            {"id": "dance-anime", "name": "anime", "category": "dance"},
            {"id": "dance-kawai", "name": "kawaii", "category": "dance"},
            {"id": "dance-touch", "name": "touch", "category": "dance"},
            {"id": "dance-employee", "name": "pushit", "category": "dance"},
            
            # Idle/Action emotes
            {"id": "idle-nervous", "name": "nervous", "category": "emotion"},
            {"id": "idle-toilet", "name": "toilet", "category": "action"},
            {"id": "idle_singing", "name": "singing", "category": "music"},
            {"id": "idle-uwu", "name": "uwu", "category": "emotion"},
            {"id": "idle-wild", "name": "scritchy", "category": "action"},
            {"id": "idle-guitar", "name": "airguitar", "category": "music"},
            
            # Special emotes
            {"id": "emote-hyped", "name": "hyped", "category": "emotion"},
            {"id": "emote-astronaut", "name": "astronaut", "category": "pose"},
            {"id": "emote-hearteyes", "name": "hearteyes", "category": "emotion"},
            {"id": "emote-swordfight", "name": "swordfight", "category": "action"},
            {"id": "emote-timejump", "name": "timejump", "category": "action"},
            {"id": "emote-snake", "name": "snake", "category": "action"},
            {"id": "emote-heartfingers", "name": "heartfingers", "category": "gesture"},
            {"id": "emote-float", "name": "float", "category": "action"},
            {"id": "emote-telekinesis", "name": "telekinesis", "category": "action"},
            {"id": "emote-sleigh", "name": "sleigh", "category": "action"},
            {"id": "emote-maniac", "name": "maniac", "category": "emotion"},
            {"id": "emote-energyball", "name": "energyball", "category": "action"},
            {"id": "emote-frog", "name": "frog", "category": "action"},
            {"id": "emote-superpose", "name": "superpose", "category": "pose"},
            {"id": "emote-cute", "name": "cute", "category": "emotion"},
            {"id": "emote-pose1", "name": "pose1", "category": "pose"},
            {"id": "emote-pose3", "name": "pose3", "category": "pose"},
            {"id": "emote-pose5", "name": "pose5", "category": "pose"},
            {"id": "emote-pose7", "name": "pose7", "category": "pose"},
            {"id": "emote-pose8", "name": "pose8", "category": "pose"},
            {"id": "emote-pose10", "name": "pose10", "category": "pose"},
            {"id": "emote-cutey", "name": "cutey", "category": "emotion"},
            {"id": "emote-punkguitar", "name": "punkguitar", "category": "music"},
            {"id": "emote-fashionista", "name": "fashionista", "category": "pose"},
            {"id": "emote-gravity", "name": "gravity", "category": "action"},
            {"id": "emote-shy2", "name": "advancedshy", "category": "emotion"},
            {"id": "emote-iceskating", "name": "iceskating", "category": "action"},
            {"id": "emote-pose6", "name": "surprisebig", "category": "pose"},
            {"id": "emote-celebrationstep", "name": "celebrationstep", "category": "celebration"},
            {"id": "emote-creepycute", "name": "creepycute", "category": "emotion"},
            {"id": "emote-boxer", "name": "boxer", "category": "action"},
            {"id": "emote-headblowup", "name": "headblowup", "category": "action"},
            {"id": "emote-pose9", "name": "ditzypose", "category": "pose"},
            {"id": "emote-teleporting", "name": "teleporting", "category": "action"},
            {"id": "emote-gift", "name": "thisforyou", "category": "gesture"},
        ]
    
    def find_emote(self, identifier: str) -> Optional[Dict]:
        """Find an emote by name or ID"""
        identifier = identifier.lower().strip()
        
        # Try by name first
        if identifier in self.emote_by_name:
            return self.emote_by_name[identifier]
        
        # Try by ID
        if identifier in self.emote_by_id:
            return self.emote_by_id[identifier]
        
        # Try partial name match
        for name, emote in self.emote_by_name.items():
            if identifier in name:
                return emote
        
        return None
    
    def get_emotes_by_category(self) -> Dict[str, List[Dict]]:
        """Get emotes grouped by category"""
        categories = {}
        for emote in self.emotes:
            category = emote['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(emote)
        return categories
    
    def get_emote_list_formatted(self) -> str:
        """Get a formatted string list of all emotes with numbers"""
        result_lines = []
        current_line = []
        
        # Show emotes in their original order with sequential numbers
        for i, emote in enumerate(self.emotes, 1):
            current_line.append(f"{i}.{emote['name']}")
            
            # Group emotes in lines of 4 for more compact display
            if len(current_line) == 4:
                result_lines.append(" | ".join(current_line))
                current_line = []
        
        # Add any remaining emotes
        if current_line:
            result_lines.append(" | ".join(current_line))
        
        return "\n".join(result_lines)
    
    def get_total_emotes(self) -> int:
        """Get total number of emotes"""
        return len(self.emotes)
    
    def get_emote_names(self) -> List[str]:
        """Get list of all emote names"""
        return [emote['name'] for emote in self.emotes]
    
    def find_emote_by_number(self, number: int) -> Optional[Dict]:
        """Find an emote by its number (1-based index)"""
        if number < 1 or number > len(self.emotes):
            return None
        return self.emotes[number - 1]
    
    def get_emote_number(self, emote_name: str) -> Optional[int]:
        """Get the number of an emote by its name"""
        for i, emote in enumerate(self.emotes):
            if emote['name'].lower() == emote_name.lower():
                return i + 1
        return None
      
