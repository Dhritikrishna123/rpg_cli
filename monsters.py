import random
from abc import ABC, abstractmethod
from rich.console import Console
from rich.text import Text

console = Console()

class Character(ABC):
    """Abstract base class for all characters (shared with Player)"""
    
    def __init__(self, name="", level=1):
        self._name = name
        self._level = level
        self._hp = 0
        self._max_hp = 0
        self._attack = 0
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = value.strip()
    
    @property
    def level(self):
        return self._level
    
    @level.setter
    def level(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("Level must be a positive integer")
        self._level = value
    
    @property
    def hp(self):
        return self._hp
    
    @hp.setter
    def hp(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("HP must be a non-negative integer")
        self._hp = min(value, self._max_hp)
    
    @property
    def max_hp(self):
        return self._max_hp
    
    @max_hp.setter
    def max_hp(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("Max HP must be a positive integer")
        self._max_hp = value
    
    @property
    def attack(self):
        return self._attack
    
    @attack.setter
    def attack(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Attack must be a non-negative integer")
        self._attack = value
    
    @property
    def is_alive(self):
        return self._hp > 0
    
    @property
    def hp_percentage(self):
        if self._max_hp <= 0:
            return 0
        return (self._hp / self._max_hp) * 100
    
    @abstractmethod
    def take_damage(self, damage):
        """Take damage from an attack"""
        pass
    
    @abstractmethod
    def get_status_display(self):
        """Get formatted status display"""
        pass

class MonsterType(ABC):
    """Abstract base class for different monster types"""
    
    @property
    @abstractmethod
    def base_name(self):
        """Base name of the monster type"""
        pass
    
    @property
    @abstractmethod
    def base_hp(self):
        """Base HP of the monster type"""
        pass
    
    @property
    @abstractmethod
    def base_attack(self):
        """Base attack of the monster type"""
        pass
    
    @property
    @abstractmethod
    def description(self):
        """Description of the monster type"""
        pass
    
    @property
    @abstractmethod
    def emoji(self):
        """Emoji representation of the monster"""
        pass

class Goblin(MonsterType):
    @property
    def base_name(self):
        return "Goblin"
    
    @property
    def base_hp(self):
        return 30
    
    @property
    def base_attack(self):
        return 8
    
    @property
    def description(self):
        return "A small, green creature with sharp teeth and beady eyes."
    
    @property
    def emoji(self):
        return "👺"

class Orc(MonsterType):
    @property
    def base_name(self):
        return "Orc"
    
    @property
    def base_hp(self):
        return 45
    
    @property
    def base_attack(self):
        return 12
    
    @property
    def description(self):
        return "A large, brutish humanoid with massive muscles and crude weapons."
    
    @property
    def emoji(self):
        return "👹"

class Skeleton(MonsterType):
    @property
    def base_name(self):
        return "Skeleton"
    
    @property
    def base_hp(self):
        return 35
    
    @property
    def base_attack(self):
        return 10
    
    @property
    def description(self):
        return "An undead warrior, bones held together by dark magic."
    
    @property
    def emoji(self):
        return "💀"

class Wolf(MonsterType):
    @property
    def base_name(self):
        return "Wolf"
    
    @property
    def base_hp(self):
        return 40
    
    @property
    def base_attack(self):
        return 11
    
    @property
    def description(self):
        return "A fierce predator with glowing eyes and sharp fangs."
    
    @property
    def emoji(self):
        return "🐺"

class Bandit(MonsterType):
    @property
    def base_name(self):
        return "Bandit"
    
    @property
    def base_hp(self):
        return 50
    
    @property
    def base_attack(self):
        return 14
    
    @property
    def description(self):
        return "A human outlaw armed with stolen weapons and armor."
    
    @property
    def emoji(self):
        return "🏴‍☠️"

class Troll(MonsterType):
    @property
    def base_name(self):
        return "Troll"
    
    @property
    def base_hp(self):
        return 70
    
    @property
    def base_attack(self):
        return 16
    
    @property
    def description(self):
        return "A massive creature with incredible regenerative abilities."
    
    @property
    def emoji(self):
        return "🧌"

class DarkKnight(MonsterType):
    @property
    def base_name(self):
        return "Dark Knight"
    
    @property
    def base_hp(self):
        return 65
    
    @property
    def base_attack(self):
        return 18
    
    @property
    def description(self):
        return "A fallen warrior clad in cursed black armor."
    
    @property
    def emoji(self):
        return "⚔️"

class DragonWhelp(MonsterType):
    @property
    def base_name(self):
        return "Dragon Whelp"
    
    @property
    def base_hp(self):
        return 80
    
    @property
    def base_attack(self):
        return 20
    
    @property
    def description(self):
        return "A young dragon with fiery breath and sharp claws."
    
    @property
    def emoji(self):
        return "🐉"

class Monster(Character):
    def __init__(self, name, hp, attack, level=1, monster_type=None):
        super().__init__(name, level)
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self._monster_type = monster_type
    
    @property
    def monster_type(self):
        return self._monster_type
    
    @property
    def threat_level(self):
        """Calculate threat level based on stats"""
        total_power = self.max_hp + (self.attack * 5)
        if total_power < 100:
            return "Low"
        elif total_power < 200:
            return "Medium"
        elif total_power < 300:
            return "High"
        else:
            return "Extreme"
    
    @property
    def threat_color(self):
        """Get color based on threat level"""
        threat_colors = {
            "Low": "green",
            "Medium": "yellow", 
            "High": "red",
            "Extreme": "bright_red"
        }
        return threat_colors.get(self.threat_level, "white")
    
    def take_damage(self, damage):
        """Take damage from an attack"""
        if damage < 0:
            raise ValueError("Damage cannot be negative")
        
        old_hp = self.hp
        self.hp = max(0, self.hp - damage)
        actual_damage = old_hp - self.hp
        
        if actual_damage > 0:
            console.print(f"💥 {self.name} takes {actual_damage} damage!", style=f"bold {self.threat_color}")
        
        if not self.is_alive:
            console.print(f"💀 {self.name} has been defeated!", style="bold green")
        
        return actual_damage
    
    def get_status_display(self):
        """Get formatted status display"""
        status_text = Text()
        emoji = self._monster_type.emoji if self._monster_type else "👾"
        status_text.append(f"{emoji} {self.name}\n", style=f"bold {self.threat_color}")
        status_text.append(f"Level: {self.level} | ", style="cyan")
        status_text.append(f"HP: {self.hp}/{self.max_hp} | ", style="red")
        status_text.append(f"Attack: {self.attack}\n", style="yellow")
        status_text.append(f"Threat Level: {self.threat_level}", style=self.threat_color)
        
        return status_text
    
    @classmethod
    def create_monster(cls, player_level):
        """Create a monster scaled to player level"""
        monster_types = [
            Goblin(), Orc(), Skeleton(), Wolf(),
            Bandit(), Troll(), DarkKnight(), DragonWhelp()
        ]
        
        # Choose random monster type
        monster_type = random.choice(monster_types)
        
        # Scale monster stats based on player level
        level_multiplier = 1 + (player_level - 1) * 0.3
        hp_variance = random.randint(-5, 10)
        attack_variance = random.randint(-2, 3)
        
        scaled_hp = int(monster_type.base_hp * level_multiplier) + hp_variance
        scaled_attack = int(monster_type.base_attack * level_multiplier) + attack_variance
        
        # Ensure minimum stats
        scaled_hp = max(scaled_hp, 20)
        scaled_attack = max(scaled_attack, 5)
        
        # Add level indicator for stronger monsters
        name = monster_type.base_name
        if player_level > 10:
            name = f"Legendary {name}"
        elif player_level > 6:
            name = f"Champion {name}"
        elif player_level > 3:
            name = f"Elite {name}"
        
        return cls(name, scaled_hp, scaled_attack, player_level, monster_type)
    
    def get_description(self):
        """Get a description of the monster"""
        if self._monster_type:
            return self._monster_type.description
        return "A mysterious creature of unknown origin."
    
    def get_combat_message(self, action="appears"):
        """Get a formatted combat message"""
        emoji = self._monster_type.emoji if self._monster_type else "👾"
        
        if action == "appears":
            return f"{emoji} A wild [bold {self.threat_color}]{self.name}[/bold {self.threat_color}] appears!"
        elif action == "attacks":
            return f"{emoji} {self.name} prepares to attack!"
        elif action == "defeated":
            return f"💀 {self.name} has been defeated!"
        
        return f"{emoji} {self.name} {action}!"
    
    def __str__(self):
        return f"{self.name} (Level {self.level}) - HP: {self.hp}/{self.max_hp}, Attack: {self.attack}"
    
    def __repr__(self):
        return f"Monster(name='{self.name}', hp={self.hp}, attack={self.attack}, level={self.level})"