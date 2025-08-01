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
        
        # NEW: Equipment system
        self._equipment = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
        
        # NEW: Skill points system
        self._skill_points = 0
        self._allocated_skills = {
            "strength": 0,  # +2 attack per point
            "vitality": 0,  # +10 HP per point
            "intelligence": 0,  # +8 mana per point
            "agility": 0   # +1 special damage per point
        }
        
        # NEW: Player statistics
        self._stats = {
            "monsters_defeated": 0,
            "total_xp_earned": 0,
            "battles_won": 0,
            "battles_lost": 0,
            "potions_used": 0,
            "gold_earned": 0,
            "levels_gained": 0
        }
        
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
    def equipment(self):
        return self._equipment.copy()
    
    @property
    def skill_points(self):
        return self._skill_points
    
    @property
    def allocated_skills(self):
        return self._allocated_skills.copy()
    
    @property
    def stats(self):
        return self._stats.copy()
    
    @property
    def total_attack(self):
        """Calculate total attack including equipment and skills"""
        base_attack = self._attack
        skill_bonus = self._allocated_skills["strength"] * 2
        equipment_bonus = 0
        
        if self._equipment["weapon"]:
            equipment_bonus += self._equipment["weapon"]["attack_bonus"]
        
        return base_attack + skill_bonus + equipment_bonus
    
    @property
    def total_max_hp(self):
        """Calculate total max HP including equipment and skills"""
        base_hp = self._max_hp
        skill_bonus = self._allocated_skills["vitality"] * 10
        equipment_bonus = 0
        
        if self._equipment["armor"]:
            equipment_bonus += self._equipment["armor"]["hp_bonus"]
        
        return base_hp + skill_bonus + equipment_bonus
    
    @property
    def total_max_mana(self):
        """Calculate total max mana including skills"""
        base_mana = self._max_mana
        skill_bonus = self._allocated_skills["intelligence"] * 8
        return base_mana + skill_bonus
    
    @property
    def total_special_damage(self):
        """Calculate total special damage including skills"""
        base_special = self._special_damage
        skill_bonus = self._allocated_skills["agility"] * 1
        return base_special + skill_bonus
    
    @property
    def attack(self):
        """Override to return total attack"""
        return self.total_attack
    
    @property
    def max_hp(self):
        """Override to return total max HP"""
        return self.total_max_hp
    
    @property
    def max_mana(self):
        """Override to return total max mana"""  
        return self.total_max_mana
    
    @property
    def special_damage(self):
        """Override to return total special damage"""
        return self.total_special_damage
    
    # NEW: Class-specific passive abilities
    def get_class_passive_bonus(self, bonus_type):
        """Get class-specific passive bonuses"""
        if self._player_class == "Warrior" and bonus_type == "damage_reduction":
            return 0.1  # 10% damage reduction
        elif self._player_class == "Mage" and bonus_type == "mana_efficiency":
            return 0.15  # 15% less mana cost for specials
        elif self._player_class == "Rogue" and bonus_type == "critical_chance":
            return 0.05  # +5% critical hit chance
        return 0
    
    def equip_item(self, item_type, item):
        """Equip an item"""
        if item_type in self._equipment:
            old_item = self._equipment[item_type]
            self._equipment[item_type] = item
            
            # Update current HP/mana if max values changed
            if item_type == "armor":
                ratio = self.hp / (self.total_max_hp - (item["hp_bonus"] if item else 0) + (old_item["hp_bonus"] if old_item else 0))
                self.hp = int(self.total_max_hp * ratio)
            
            console.print(f"⚔️ Equipped {item['name']}!", style="bold green")
            return old_item
        return None
    
    def allocate_skill_point(self, skill, points=1):
        """Allocate skill points to a skill"""
        if self._skill_points >= points and skill in self._allocated_skills:
            self._skill_points -= points
            self._allocated_skills[skill] += points
            
            # Update current stats if max values changed
            if skill == "vitality":
                self.hp = min(self.hp + (points * 10), self.total_max_hp)
            elif skill == "intelligence":
                self.mana = min(self.mana + (points * 8), self.total_max_mana)
            
            return True
        return False
    
    def update_stat(self, stat_name, value):
        """Update a player statistic"""
        if stat_name in self._stats:
            self._stats[stat_name] += value
    
    # Rest of the properties remain the same...
    @property
    def mana(self):
        return self._mana
    
    @mana.setter
    def mana(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Mana must be a non-negative integer")
        self._mana = min(value, self.total_max_mana)
    
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
        # Apply mage passive ability
        base_cost = self._special_mana_cost
        if self._player_class == "Mage":
            base_cost = int(base_cost * (1 - self.get_class_passive_bonus("mana_efficiency")))
        return base_cost
    
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
        return self._inventory.copy()
    
    @property
    def mana_percentage(self):
        if self.total_max_mana <= 0:
            return 0
        return (self._mana / self.total_max_mana) * 100
    
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
        class_table.add_column("Passive Ability", style="yellow")
        
        class_table.add_row("1", "⚔️ Warrior", "High health and attack", "🛡️ 10% Damage Reduction")
        class_table.add_row("2", "🔮 Mage", "Powerful special attacks", "🧠 15% Mana Efficiency")
        class_table.add_row("3", "🗡️ Rogue", "Balanced with quick cooldowns", "⚡ +5% Critical Chance")
        
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
        """Take damage from an attack with class passive abilities"""
        if damage < 0:
            raise ValueError("Damage cannot be negative")
        
        # Apply warrior damage reduction
        if self._player_class == "Warrior":
            damage = int(damage * (1 - self.get_class_passive_bonus("damage_reduction")))
            
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
        hp_bar = self._create_progress_bar(self.hp, self.total_max_hp, "red")
        status_table.add_row("❤️ Health", f"{self.hp}/{self.total_max_hp}", hp_bar)
        
        # Mana bar
        mana_bar = self._create_progress_bar(self.mana, self.total_max_mana, "blue")
        status_table.add_row("🔮 Mana", f"{self.mana}/{self.total_max_mana}", mana_bar)
        
        # XP bar
        xp_bar = self._create_progress_bar(self.xp, self.xp_to_next, "green")
        status_table.add_row("⭐ Experience", f"{self.xp}/{self.xp_to_next}", xp_bar)
        
        # Other stats
        status_table.add_row("⚔️ Attack", str(self.total_attack), "")
        status_table.add_row("💰 Gold", str(self.gold), "")
        status_table.add_row("🔥 Skill Points", str(self.skill_points), "")
        status_table.add_row("🧪 Health Potions", str(self._inventory['health_potions']), "")
        status_table.add_row("🔮 Mana Potions", str(self._inventory['mana_potions']), "")
        
        return status_table
    
    def view_skill_menu(self):
        """Display and handle skill point allocation"""
        if self._skill_points <= 0:
            console.print("❌ No skill points available!", style="bold red")
            return
            
        console.clear()
        console.print(Panel.fit(f"🔥 Skill Points Available: {self._skill_points}", 
                              title="💪 Character Development", border_style="gold1"))
        
        skills_table = Table(title="Skills")
        skills_table.add_column("Skill", style="cyan")
        skills_table.add_column("Current", style="green")
        skills_table.add_column("Effect", style="yellow")
        skills_table.add_column("Next Level", style="blue")
        
        skills_table.add_row("💪 Strength", str(self._allocated_skills["strength"]), 
                           "+2 Attack per point", f"+{(self._allocated_skills['strength'] + 1) * 2} total attack")
        skills_table.add_row("❤️ Vitality", str(self._allocated_skills["vitality"]), 
                           "+10 HP per point", f"+{(self._allocated_skills['vitality'] + 1) * 10} total HP")
        skills_table.add_row("🧠 Intelligence", str(self._allocated_skills["intelligence"]), 
                           "+8 Mana per point", f"+{(self._allocated_skills['intelligence'] + 1) * 8} total mana")
        skills_table.add_row("⚡ Agility", str(self._allocated_skills["agility"]), 
                           "+1 Special Damage", f"+{(self._allocated_skills['agility'] + 1)} special damage")
        
        console.print(skills_table)
        
        choice = Prompt.ask("Allocate point to which skill? (strength/vitality/intelligence/agility or 'back')", 
                          choices=["strength", "vitality", "intelligence", "agility", "back"])
        
        if choice != "back":
            if self.allocate_skill_point(choice):
                console.print(f"✅ Allocated 1 skill point to {choice.title()}!", style="bold green")
                console.input("Press Enter to continue...")
            else:
                console.print("❌ Failed to allocate skill point!", style="bold red")
                console.input("Press Enter to continue...")
    
    def view_equipment_menu(self):
        """Display current equipment"""
        console.clear()
        equipment_table = Table(title="🎒 Current Equipment")
        equipment_table.add_column("Slot", style="cyan")
        equipment_table.add_column("Item", style="green")
        equipment_table.add_column("Bonus", style="yellow")
        
        for slot, item in self._equipment.items():
            if item:
                bonus_text = ""
                if "attack_bonus" in item:
                    bonus_text += f"+{item['attack_bonus']} Attack "
                if "hp_bonus" in item:
                    bonus_text += f"+{item['hp_bonus']} HP "
                equipment_table.add_row(slot.title(), item["name"], bonus_text.strip())
            else:
                equipment_table.add_row(slot.title(), "Empty", "No bonus")
        
        console.print(equipment_table)
        console.input("Press Enter to continue...")
    
    def view_statistics(self):
        """Display player statistics"""
        console.clear()
        stats_table = Table(title="📊 Adventure Statistics")
        stats_table.add_column("Statistic", style="cyan")
        stats_table.add_column("Value", style="green")
        
        stats_table.add_row("👹 Monsters Defeated", str(self._stats["monsters_defeated"]))
        stats_table.add_row("⭐ Total XP Earned", str(self._stats["total_xp_earned"]))
        stats_table.add_row("🏆 Battles Won", str(self._stats["battles_won"]))
        stats_table.add_row("💀 Battles Lost", str(self._stats["battles_lost"]))
        stats_table.add_row("🧪 Potions Used", str(self._stats["potions_used"]))
        stats_table.add_row("💰 Gold Earned", str(self._stats["gold_earned"]))
        stats_table.add_row("📈 Levels Gained", str(self._stats["levels_gained"]))
        
        # Calculate win rate
        total_battles = self._stats["battles_won"] + self._stats["battles_lost"]
        win_rate = (self._stats["battles_won"] / total_battles * 100) if total_battles > 0 else 0
        stats_table.add_row("📈 Win Rate", f"{win_rate:.1f}%")
        
        console.print(stats_table)
        console.input("Press Enter to continue...")
    
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
        self._stats["levels_gained"] += 1
        
        # Increase stats
        hp_increase = 15 + (self.level * 2)
        mana_increase = 10 + self.level
        attack_increase = 3 + self.level
        special_increase = 5 + self.level
        
        self._max_hp += hp_increase
        self.hp = self.total_max_hp  # Full heal on level up
        self._max_mana += mana_increase
        self.mana = self.total_max_mana  # Full mana on level up
        self._attack += attack_increase
        self._special_damage += special_increase
        
        # Award skill points (1 per level, bonus at certain levels)
        skill_points_gained = 1
        if self.level % 5 == 0:  # Bonus skill point every 5 levels
            skill_points_gained += 1
        self._skill_points += skill_points_gained
        
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
        increases_table.add_row("🔥 Skill Points", f"+{skill_points_gained}")
        
        console.print(increases_table)
        console.print("✨ Fully healed and mana restored!", style="bold green")
        console.input("\nPress Enter to continue...")
    
    def use_health_potion(self):
        """Use a healing potion"""
        if self._inventory["health_potions"] <= 0:
            console.print("❌ You don't have any health potions!", style="bold red")
            return False
        
        if self.hp >= self.total_max_hp:
            console.print("❌ Your HP is already full!", style="bold red")
            return False
        
        # Calculate healing amount
        heal_amount = 30 + (self.level * 5)
        old_hp = self.hp
        self.hp = min(self.total_max_hp, self.hp + heal_amount)
        actual_heal = self.hp - old_hp
        
        self._inventory["health_potions"] -= 1
        self._stats["potions_used"] += 1
        
        console.print("🧪 You used a health potion!", style="bold green")
        console.print(f"✨ Restored {actual_heal} HP!", style="bold yellow")
        console.print(f"Current HP: [red]{self.hp}/{self.total_max_hp}[/red]")
        return True
    
    def use_mana_potion(self):
        """Use a mana potion"""
        if self._inventory["mana_potions"] <= 0:
            console.print("❌ You don't have any mana potions!", style="bold red")
            return False
        
        if self.mana >= self.total_max_mana:
            console.print("❌ Your mana is already full!", style="bold red")
            return False
        
        # Calculate mana restoration
        mana_amount = 25 + (self.level * 3)
        old_mana = self.mana
        self.mana = min(self.total_max_mana, self.mana + mana_amount)
        actual_restore = self.mana - old_mana
        
        self._inventory["mana_potions"] -= 1
        self._stats["potions_used"] += 1
        
        console.print("🔮 You used a mana potion!", style="bold blue")
        console.print(f"✨ Restored {actual_restore} mana!", style="bold yellow")
        console.print(f"Current Mana: [blue]{self.mana}/{self.total_max_mana}[/blue]")
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
                "max_hp": self._max_hp,  # Save base values
                "mana": self.mana,
                "max_mana": self._max_mana,  # Save base values
                "attack": self._attack,  # Save base values
                "special_damage": self._special_damage,
                "special_cooldown": self.special_cooldown,
                "special_max_cooldown": self.special_max_cooldown,
                "special_mana_cost": self._special_mana_cost,
                "xp": self.xp,
                "xp_to_next": self.xp_to_next,
                "gold": self.gold,
                "inventory": self._inventory,
                "equipment": self._equipment,
                "skill_points": self._skill_points,
                "allocated_skills": self._allocated_skills,
                "stats": self._stats
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
            player._max_hp = player_data.get("max_hp", 100)
            player.hp = player_data.get("hp", 100)
            player._max_mana = player_data.get("max_mana", 30)
            player.mana = player_data.get("mana", 30)
            player._attack = player_data.get("attack", 20)
            player._special_damage = player_data.get("special_damage", 35)
            player.special_cooldown = player_data.get("special_cooldown", 0)
            player.special_max_cooldown = player_data.get("special_max_cooldown", 5)
            player._special_mana_cost = player_data.get("special_mana_cost", 15)
            player.xp = player_data.get("xp", 0)
            player.xp_to_next = player_data.get("xp_to_next", 50)
            player.gold = player_data.get("gold", 50)
            player._inventory = player_data.get("inventory", {"health_potions": 2, "mana_potions": 1})
            
            # Load new features (with defaults for old saves)
            player._equipment = player_data.get("equipment", {"weapon": None, "armor": None, "accessory": None})
            player._skill_points = player_data.get("skill_points", 0)
            player._allocated_skills = player_data.get("allocated_skills", {"strength": 0, "vitality": 0, "intelligence": 0, "agility": 0})
            player._stats = player_data.get("stats", {"monsters_defeated": 0, "total_xp_earned": 0, "battles_won": 0, "battles_lost": 0, "potions_used": 0, "gold_earned": 0, "levels_gained": 0})
            
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
        info_text.append(f"Special Attack Damage: {self.total_special_damage}\n", style="red")
        info_text.append(f"Special Mana Cost: {self.special_mana_cost}", style="blue")
        
        console.print(Panel(info_text, title="📊 Additional Stats", border_style="blue"))