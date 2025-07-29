import json
import os
from utils import get_user_choice, clear_screen

class Player:
    def __init__(self, name="", player_class="", level=1):
        self.name = name
        self.player_class = player_class
        self.level = level
        self.hp = 0
        self.max_hp = 0
        self.mana = 0
        self.max_mana = 0
        self.attack = 0
        self.special_damage = 0
        self.special_cooldown = 0
        self.special_max_cooldown = 0
        self.special_mana_cost = 0
        self.xp = 0
        self.xp_to_next = 50
        self.gold = 50
        self.inventory = {"health_potions": 2, "mana_potions": 1}
        
        if name and player_class:
            self._set_class_stats()
    
    def _set_class_stats(self):
        """Set initial stats based on class"""
        if self.player_class == "Warrior":
            self.max_hp = self.hp = 100
            self.max_mana = self.mana = 30
            self.attack = 20
            self.special_damage = 35
            self.special_max_cooldown = 5
            self.special_mana_cost = 15
        elif self.player_class == "Mage":
            self.max_hp = self.hp = 80
            self.max_mana = self.mana = 60
            self.attack = 15
            self.special_damage = 50
            self.special_max_cooldown = 5
            self.special_mana_cost = 20
        else:  # Rogue
            self.max_hp = self.hp = 90
            self.max_mana = self.mana = 45
            self.attack = 18
            self.special_damage = 40
            self.special_max_cooldown = 4
            self.special_mana_cost = 15
    
    @classmethod
    def create_new_player(cls):
        """Create a new player through character creation"""
        clear_screen()
        print("=" * 40)
        print("      CHARACTER CREATION")
        print("=" * 40)
        
        # Get player name
        while True:
            name = input("Enter your character's name: ").strip()
            if name:
                break
            print("Please enter a valid name!")
        
        # Choose character class
        print("\nChoose your class:")
        print("1. Warrior - High health and attack")
        print("2. Mage - Moderate stats, powerful special attack")
        print("3. Rogue - Balanced stats, quick special cooldown")
        
        class_choice = get_user_choice("Enter your choice (1-3): ", ["1", "2", "3"])
        
        class_names = {"1": "Warrior", "2": "Mage", "3": "Rogue"}
        player_class = class_names[class_choice]
        
        player = cls(name, player_class)
        return player
    
    def level_up(self):
        """Level up the player character"""
        print("\n" + "=" * 30)
        print("       LEVEL UP!")
        print("=" * 30)
        
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
        
        print(f"Level {old_level} -> Level {self.level}")
        print(f"Max HP increased by {hp_increase}!")
        print(f"Max Mana increased by {mana_increase}!")
        print(f"Attack increased by {attack_increase}!")
        print(f"Special Attack increased by {special_increase}!")
        print("Fully healed and restored mana!")
        
        input("\nPress Enter to continue...")
    
    def use_health_potion(self):
        """Use a healing potion"""
        if self.inventory["health_potions"] <= 0:
            print("You don't have any health potions!")
            return
        
        if self.hp >= self.max_hp:
            print("Your HP is already full!")
            return
        
        # Calculate healing amount
        heal_amount = 30 + (self.level * 5)
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + heal_amount)
        actual_heal = self.hp - old_hp
        
        self.inventory["health_potions"] -= 1
        
        print(f"You used a health potion!")
        print(f"Restored {actual_heal} HP!")
        print(f"Current HP: {self.hp}/{self.max_hp}")
    
    def use_mana_potion(self):
        """Use a mana potion"""
        if self.inventory["mana_potions"] <= 0:
            print("You don't have any mana potions!")
            return
        
        if self.mana >= self.max_mana:
            print("Your mana is already full!")
            return
        
        # Calculate mana restoration
        mana_amount = 25 + (self.level * 3)
        old_mana = self.mana
        self.mana = min(self.max_mana, self.mana + mana_amount)
        actual_restore = self.mana - old_mana
        
        self.inventory["mana_potions"] -= 1
        
        print(f"You used a mana potion!")
        print(f"Restored {actual_restore} mana!")
        print(f"Current Mana: {self.mana}/{self.max_mana}")
    
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
                "inventory": self.inventory
            }
            
            with open(filename, 'w') as file:
                json.dump(player_data, file, indent=4)
            
            print(f"Game saved successfully to {filename}!")
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    @classmethod
    def load_from_file(cls, filename="save_game.json"):
        """Load player data from a JSON file"""
        try:
            if not os.path.exists(filename):
                print(f"Save file {filename} not found!")
                return None
            
            with open(filename, 'r') as file:
                player_data = json.load(file)
            
            # Create new player instance
            player = cls()
            
            # Load all attributes
            for key, value in player_data.items():
                setattr(player, key, value)
            
            print(f"Game loaded successfully from {filename}!")
            return player
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
    
    def display_stats(self):
        """Display detailed character information"""
        clear_screen()
        print("=" * 30)
        print("    CHARACTER INFORMATION")
        print("=" * 30)
        print(f"Name: {self.name}")
        print(f"Class: {self.player_class}")
        print(f"Level: {self.level}")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"Mana: {self.mana}/{self.max_mana}")
        print(f"Attack: {self.attack}")
        print(f"XP: {self.xp}/{self.xp_to_next}")
        print(f"Gold: {self.gold}")
        print(f"Health Potions: {self.inventory['health_potions']}")
        print(f"Mana Potions: {self.inventory['mana_potions']}")
        print(f"Special Attack Cooldown: {self.special_cooldown} turns")

