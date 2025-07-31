import json
import os
from abc import ABC, abstractmethod
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn
from utils import get_user_choice

console = Console()

class Character(ABC):
    """Abstract base class for all characters"""
    
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

class Player(Character):
    def __init__(self, name="", player_class="", level=1):
        super().__init__(name, level)
        self._player_class = player_class
        self._mana = 0
        self._max_mana = 0
        self._special_damage = 0
        self._special_cooldown = 0
        self._special_max_cooldown = 0
        self._special_mana_cost = 0
        self._xp = 0
        self._xp_to_next = 50
        self._gold = 50
        self._inventory = {"health_potions": 2, "mana_potions": 1}
        
        if name and player_class:
            self._set_class_stats()
    
    @property
    def player_class(self):
        return self._player_class
    
    @player_class.setter
    def player_class(self, value):
        valid_classes = ["Warrior", "Mage", "Rogue"]
        if value not in valid_classes:
            raise ValueError(f"Player class must be one of: {valid_classes}")
        self._player_class = value
    
    @property
    def mana(self):
        return self._mana
    
    @mana.setter
    def mana(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Mana must be a non-negative integer")
        self._mana = min(value, self._max_mana)
    
    @property
    def max_mana(self):
        return self._max_mana
    
    @max_mana.setter
    def max_mana(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Max mana must be a non-negative integer")
        self._max_mana = value
    
    @property
    def special_damage(self):
        return self._special_damage
    
    @special_damage.setter
    def special_damage(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Special damage must be a non-negative integer")
        self._special_damage = value
    
    @property
    def special_cooldown(self):
        return self._special_cooldown
    
    @special_cooldown.setter
    def special_cooldown(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Special cooldown must be a non-negative integer")
        self._special_cooldown = value
    
    @property
    def special_max_cooldown(self):
        return self._special_max_cooldown
    
    @special_max_cooldown.setter
    def special_max_cooldown(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Special max cooldown must be a non-negative integer")
        self._special_max_cooldown = value
    
    @property
    def special_mana_cost(self):
        return self._special_mana_cost
    
    @special_mana_cost.setter
    def special_mana_cost(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Special mana cost must be a non-negative integer")
        self._special_mana_cost = value
    
    @property
    def xp(self):
        return self._xp
    
    @xp.setter
    def xp(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("XP must be a non-negative integer")
        self._xp = value
    
    @property
    def xp_to_next(self):
        return self._xp_to_next
    
    @xp_to_next.setter
    def xp_to_next(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("XP to next level must be a positive integer")
        self._xp_to_next = value
    
    @property
    def gold(self):
        return self._gold
    
    @gold.setter
    def gold(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Gold must be a non-negative integer")
        self._gold = value
    
    @property
    def inventory(self):
        return self._inventory.copy()  # Return a copy to prevent direct modification
    
    @property
    def mana_percentage(self):
        if self._max_mana <= 0:
            return 0
        return (self._mana / self._max_mana) * 100
    
    @property
    def xp_percentage(self):
        if self._xp_to_next <= 0:
            return 0
        return (self._xp / self._xp_to_next) * 100
    
    def _set_class_stats(self):
        """Set initial stats based on class"""
        class_stats = {
            "Warrior": {
                "max_hp": 100, "max_mana": 30, "attack": 20,
                "special_damage": 35, "special_max_cooldown": 5, "special_mana_cost": 15
            },
            "Mage": {
                "max_hp": 80, "max_mana": 60, "attack": 15,
                "special_damage": 50, "special_max_cooldown": 5, "special_mana_cost": 20
            },
            "Rogue": {
                "max_hp": 90, "max_mana": 45, "attack": 18,
                "special_damage": 40, "special_max_cooldown": 4, "special_mana_cost": 15
            }
        }
        
        stats = class_stats[self._player_class]
        self._max_hp = self._hp = stats["max_hp"]
        self._max_mana = self._mana = stats["max_mana"]
        self._attack = stats["attack"]
        self._special_damage = stats["special_damage"]
        self._special_max_cooldown = stats["special_max_cooldown"]
        self._special_mana_cost = stats["special_mana_cost"]
    
    @classmethod
    def create_new_player(cls):
        """Create a new player through character creation"""
        console.clear()
        
        # Character creation panel
        creation_panel = Panel.fit(
            "🎮 CHARACTER CREATION 🎮\n\nCreate your legendary hero!",
            title="⭐ New Adventure ⭐",
            border_style="cyan"
        )
        console.print(creation_panel)
        
        # Get player name
        while True:
            name = Prompt.ask("🧙 Enter your character's name").strip()
            if name:
                break
            console.print("❌ Please enter a valid name!", style="bold red")
        
        # Choose character class
        console.print("\n🎯 Choose your class:", style="bold cyan")
        
        # Create class selection table
        class_table = Table(title="Available Classes")
        class_table.add_column("Choice", style="cyan", no_wrap=True)
        class_table.add_column("Class", style="magenta", no_wrap=True)
        class_table.add_column("Description", style="green")
        class_table.add_column("Stats", style="yellow")
        
        class_table.add_row("1", "⚔️ Warrior", "High health and attack", "💪 Tanky Fighter")
        class_table.add_row("2", "🔮 Mage", "Powerful special attacks", "🧠 Magical Damage")
        class_table.add_row("3", "🗡️ Rogue", "Balanced with quick cooldowns", "⚡ Swift Assassin")
        
        console.print(class_table)
        
        class_choice = Prompt.ask("Enter your choice", choices=["1", "2", "3"], default="1")
        
        class_names = {"1": "Warrior", "2": "Mage", "3": "Rogue"}
        player_class = class_names[class_choice]
        
        player = cls(name, player_class)
        
        # Display creation success
        success_text = Text()
        success_text.append("🎉 Character created successfully!\n", style="bold green")
        success_text.append(f"Welcome, {name} the {player_class}!", style="bold cyan")
        
        console.print(Panel(success_text, title="✅ Success", border_style="green"))
        console.input("\nPress Enter to begin your adventure...")
        
        return player
    
    def take_damage(self, damage):
        """Take damage from an attack"""
        if damage < 0:
            raise ValueError("Damage cannot be negative")
        
        old_hp = self._hp
        self._hp = max(0, self._hp - damage)
        actual_damage = old_hp - self._hp
        
        if actual_damage > 0:
            console.print(f"💥 Took {actual_damage} damage!", style="bold red")
        
        return actual_damage
    
    def get_status_display(self):
        """Get formatted status display"""
        status_table = Table(title=f"🧙 {self.name} - Level {self.level} {self.player_class}")
        status_table.add_column("Attribute", style="cyan")
        status_table.add_column("Value", style="green")
        status_table.add_column("Visual", style="yellow")
        
        # HP bar
        hp_bar = self._create_progress_bar(self.hp, self.max_hp, "red")
        status_table.add_row("❤️ Health", f"{self.hp}/{self.max_hp}", hp_bar)
        
        # Mana bar
        mana_bar = self._create_progress_bar(self.mana, self.max_mana, "blue")
        status_table.add_row("🔮 Mana", f"{self.mana}/{self.max_mana}", mana_bar)
        
        # XP bar
        xp_bar = self._create_progress_bar(self.xp, self.xp_to_next, "green")
        status_table.add_row("⭐ Experience", f"{self.xp}/{self.xp_to_next}", xp_bar)
        
        # Other stats
        status_table.add_row("⚔️ Attack", str(self.attack), "")
        status_table.add_row("💰 Gold", str(self.gold), "")
        status_table.add_row("🧪 Health Potions", str(self._inventory['health_potions']), "")
        status_table.add_row("🔮 Mana Potions", str(self._inventory['mana_potions']), "")
        
        return status_table
    
    def _create_progress_bar(self, current, maximum, color):
        """Create a visual progress bar"""
        if maximum <= 0:
            return f"[{color}]░░░░░░░░░░[/{color}]"
        
        percentage = current / maximum
        filled_blocks = int(percentage * 10)
        
        filled = "█" * filled_blocks
        empty = "░" * (10 - filled_blocks)
        return f"[{color}]{filled}[/{color}][dim]{empty}[/dim]"
    
    def level_up(self):
        """Level up the player character"""
        level_up_panel = Panel.fit(
            f"🎉 LEVEL UP! 🎉\n\nLevel {self.level} → Level {self.level + 1}",
            title="⬆️ LEVEL UP ⬆️",
            border_style="gold1"
        )
        console.print(level_up_panel)
        
        old_level = self.level
        self.level += 1
        
        # Increase stats
        hp_increase = 15 + (self.level * 2)
        mana_increase = 10 + self.level
        attack_increase = 3 + self.level
        special_increase = 5 + self.level
        
        self.max_hp += hp_increase
        self.hp = self.max_hp  # Full heal on level up
        self.max_mana += mana_increase
        self.mana = self.max_mana  # Full mana on level up
        self.attack += attack_increase
        self.special_damage += special_increase
        
        # Set XP for next level
        self.xp = 0
        self.xp_to_next = 50 + (self.level * 25)
        
        # Display stat increases
        increases_table = Table(title="Stat Increases")
        increases_table.add_column("Stat", style="cyan")
        increases_table.add_column("Increase", style="green")
        
        increases_table.add_row("❤️ Max HP", f"+{hp_increase}")
        increases_table.add_row("🔮 Max Mana", f"+{mana_increase}")
        increases_table.add_row("⚔️ Attack", f"+{attack_increase}")
        increases_table.add_row("💥 Special Attack", f"+{special_increase}")
        
        console.print(increases_table)
        console.print("✨ Fully healed and mana restored!", style="bold green")
        console.input("\nPress Enter to continue...")
    
    def use_health_potion(self):
        """Use a healing potion"""
        if self._inventory["health_potions"] <= 0:
            console.print("❌ You don't have any health potions!", style="bold red")
            return False
        
        if self.hp >= self.max_hp:
            console.print("❌ Your HP is already full!", style="bold red")
            return False
        
        # Calculate healing amount
        heal_amount = 30 + (self.level * 5)
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + heal_amount)
        actual_heal = self.hp - old_hp
        
        self._inventory["health_potions"] -= 1
        
        console.print("🧪 You used a health potion!", style="bold green")
        console.print(f"✨ Restored {actual_heal} HP!", style="bold yellow")
        console.print(f"Current HP: [red]{self.hp}/{self.max_hp}[/red]")
        return True
    
    def use_mana_potion(self):
        """Use a mana potion"""
        if self._inventory["mana_potions"] <= 0:
            console.print("❌ You don't have any mana potions!", style="bold red")
            return False
        
        if self.mana >= self.max_mana:
            console.print("❌ Your mana is already full!", style="bold red")
            return False
        
        # Calculate mana restoration
        mana_amount = 25 + (self.level * 3)
        old_mana = self.mana
        self.mana = min(self.max_mana, self.mana + mana_amount)
        actual_restore = self.mana - old_mana
        
        self._inventory["mana_potions"] -= 1
        
        console.print("🔮 You used a mana potion!", style="bold blue")
        console.print(f"✨ Restored {actual_restore} mana!", style="bold yellow")
        console.print(f"Current Mana: [blue]{self.mana}/{self.max_mana}[/blue]")
        return True
    
    def use_special_attack(self):
        """Use the player's special attack"""
        if self.special_cooldown > 0:
            return False, "Special attack is on cooldown!"
        
        if self.mana < self.special_mana_cost:
            return False, f"Not enough mana! Need {self.special_mana_cost}, have {self.mana}"
        
        # Use mana and set cooldown
        self.mana -= self.special_mana_cost
        self.special_cooldown = self.special_max_cooldown
        return True, "Special attack used successfully!"
    
    def reduce_special_cooldown(self):
        """Reduce special attack cooldown by 1"""
        if self.special_cooldown > 0:
            self.special_cooldown -= 1
    
    def add_item_to_inventory(self, item_type, quantity=1):
        """Add items to inventory"""
        if item_type in self._inventory:
            self._inventory[item_type] += quantity
        else:
            self._inventory[item_type] = quantity
    
    def remove_item_from_inventory(self, item_type, quantity=1):
        """Remove items from inventory"""
        if item_type in self._inventory and self._inventory[item_type] >= quantity:
            self._inventory[item_type] -= quantity
            return True
        return False
    
    def save_to_file(self, filename="save_game.json"):
        """Save player data to a JSON file"""
        try:
            player_data = {
                "name": self.name,
                "player_class": self.player_class,
                "level": self.level,
                "hp": self.hp,
                "max_hp": self.max_hp,
                "mana": self.mana,
                "max_mana": self.max_mana,
                "attack": self.attack,
                "special_damage": self.special_damage,
                "special_cooldown": self.special_cooldown,
                "special_max_cooldown": self.special_max_cooldown,
                "special_mana_cost": self.special_mana_cost,
                "xp": self.xp,
                "xp_to_next": self.xp_to_next,
                "gold": self.gold,
                "inventory": self._inventory
            }
            
            with open(filename, 'w') as file:
                json.dump(player_data, file, indent=4)
            
            console.print(f"💾 Game saved successfully to {filename}!", style="bold green")
            return True
        except Exception as e:
            console.print(f"❌ Error saving game: {e}", style="bold red")
            return False
    
    @classmethod
    def load_from_file(cls, filename="save_game.json"):
        """Load player data from a JSON file"""
        try:
            if not os.path.exists(filename):
                console.print(f"❌ Save file {filename} not found!", style="bold red")
                return None
            
            with open(filename, 'r') as file:
                player_data = json.load(file)
            
            # Create new player instance
            player = cls()
            
            # Load all attributes using properties where available
            player.name = player_data.get("name", "")
            player.player_class = player_data.get("player_class", "Warrior")
            player.level = player_data.get("level", 1)
            player.hp = player_data.get("hp", 100)
            player.max_hp = player_data.get("max_hp", 100)
            player.mana = player_data.get("mana", 30)
            player.max_mana = player_data.get("max_mana", 30)
            player.attack = player_data.get("attack", 20)
            player.special_damage = player_data.get("special_damage", 35)
            player.special_cooldown = player_data.get("special_cooldown", 0)
            player.special_max_cooldown = player_data.get("special_max_cooldown", 5)
            player.special_mana_cost = player_data.get("special_mana_cost", 15)
            player.xp = player_data.get("xp", 0)
            player.xp_to_next = player_data.get("xp_to_next", 50)
            player.gold = player_data.get("gold", 50)
            player._inventory = player_data.get("inventory", {"health_potions": 2, "mana_potions": 1})
            
            console.print(f"📁 Game loaded successfully from {filename}!", style="bold green")
            return player
        except Exception as e:
            console.print(f"❌ Error loading game: {e}", style="bold red")
            return None
    
    def display_stats(self):
        """Display detailed character information"""
        console.clear()
        console.print(self.get_status_display())
        
        # Additional info panel
        info_text = Text()
        info_text.append(f"Class: {self.player_class}\n", style="bold cyan")
        info_text.append(f"Special Attack Cooldown: {self.special_cooldown} turns\n", style="yellow")
        info_text.append(f"Special Attack Damage: {self.special_damage}\n", style="red")
        info_text.append(f"Special Mana Cost: {self.special_mana_cost}", style="blue")
        
        console.print(Panel(info_text, title="📊 Additional Stats", border_style="blue"))