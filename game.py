import random
import os
from player import Player
from monsters import Monster
from combat import Combat
from shop import Shop
from utils import clear_screen, get_user_choice

class Game:
    def __init__(self):
        self.player = None
        self.save_directory = "saves"
        
        # Create saves directory if it doesn't exist
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
    
    def start(self):
        """Start the game"""
        clear_screen()
        print("=" * 50)
        print("      WELCOME TO PYTHON ADVENTURE RPG!")
        print("=" * 50)
        print()
        
        # Main menu
        print("1. New Game")
        print("2. Load Game")
        print("3. Quit")
        
        choice = get_user_choice("Enter your choice (1-3): ", ["1", "2", "3"])
        
        if choice == "1":
            self.player = Player.create_new_player()
            print(f"\nWelcome, {self.player.name} the {self.player.player_class}!")
            print("Your adventure begins now...")
            input("\nPress Enter to continue...")
            self.main_game_loop()
        elif choice == "2":
            self.load_game()
        elif choice == "3":
            print("\nThanks for playing!")
            return
    
    def main_game_loop(self):
        """Main game loop"""
        while True:
            clear_screen()
            print("=" * 50)
            print(f"  {self.player.name} - Level {self.player.level} {self.player.player_class}")
            print("=" * 50)
            print(f"HP: {self.player.hp}/{self.player.max_hp} | Mana: {self.player.mana}/{self.player.max_mana} | Gold: {self.player.gold}")
            print(f"Attack: {self.player.attack} | XP: {self.player.xp}/{self.player.xp_to_next}")
            print(f"Special Attack Cooldown: {self.player.special_cooldown} turns")
            print(f"Health Potions: {self.player.inventory['health_potions']} | Mana Potions: {self.player.inventory['mana_potions']}")
            print()
            
            print("What would you like to do?")
            print("1. Fight a monster")
            print("2. Visit the shop")
            print("3. Use a health potion")
            print("4. Use a mana potion")
            print("5. View character info")
            print("6. Save game")
            print("7. Load game")
            print("8. Quit game")
            
            choice = get_user_choice("Enter your choice (1-8): ", ["1", "2", "3", "4", "5", "6", "7", "8"])
            
            if choice == "1":
                self.fight_monster()
            elif choice == "2":
                shop = Shop(self.player)
                shop.visit_shop()
            elif choice == "3":
                self.player.use_health_potion()
                input("\nPress Enter to continue...")
            elif choice == "4":
                self.player.use_mana_potion()
                input("\nPress Enter to continue...")
            elif choice == "5":
                self.player.display_stats()
                input("\nPress Enter to continue...")
            elif choice == "6":
                self.save_game()
            elif choice == "7":
                self.load_game()
            elif choice == "8":
                print("\nThanks for playing Python Adventure RPG!")
                print("Come back soon for more adventures!")
                break
    
    def fight_monster(self):
        """Fight a monster"""
        monster = Monster.create_monster(self.player.level)
        combat = Combat(self.player, monster)
        battle_result = combat.start_battle()
        
        if battle_result == "victory":
            # Gain XP and gold
            xp_gained = random.randint(10, 20) + (self.player.level * 2)
            gold_gained = random.randint(5, 15) + self.player.level
            
            self.player.xp += xp_gained
            self.player.gold += gold_gained
            
            print(f"\nYou gained {xp_gained} XP and {gold_gained} gold!")
            
            # Check for level up
            if self.player.xp >= self.player.xp_to_next:
                self.player.level_up()
            
            input("\nPress Enter to continue...")
            
        elif battle_result == "defeat":
            print("\nGAME OVER!")
            print("You have been defeated in battle...")
            print("Thanks for playing Python Adventure RPG!")
            exit()
    
    def save_game(self):
        """Save the current game"""
        save_files = [f for f in os.listdir(self.save_directory) if f.endswith('.json')]
        
        print("\nExisting save files:")
        for i, save_file in enumerate(save_files, 1):
            print(f"{i}. {save_file}")
        print(f"{len(save_files) + 1}. Create new save file")
        
        if save_files:
            choice = get_user_choice(f"Choose save slot (1-{len(save_files) + 1}): ", 
                                   [str(i) for i in range(1, len(save_files) + 2)])
            
            if int(choice) <= len(save_files):
                filename = save_files[int(choice) - 1]
            else:
                filename = input("Enter save file name (without .json): ").strip() + ".json"
        else:
            filename = input("Enter save file name (without .json): ").strip() + ".json"
        
        filepath = os.path.join(self.save_directory, filename)
        if self.player.save_to_file(filepath):
            input("\nPress Enter to continue...")
    
    def load_game(self):
        """Load a saved game"""
        save_files = [f for f in os.listdir(self.save_directory) if f.endswith('.json')]
        
        if not save_files:
            print("\nNo save files found!")
            input("Press Enter to continue...")
            return
        
        print("\nAvailable save files:")
        for i, save_file in enumerate(save_files, 1):
            print(f"{i}. {save_file}")
        
        choice = get_user_choice(f"Choose save file (1-{len(save_files)}): ", 
                               [str(i) for i in range(1, len(save_files) + 1)])
        
        filename = save_files[int(choice) - 1]
        filepath = os.path.join(self.save_directory, filename)
        
        loaded_player = Player.load_from_file(filepath)
        if loaded_player:
            self.player = loaded_player
            print(f"Welcome back, {self.player.name}!")
            input("\nPress Enter to continue...")
            self.main_game_loop()
        else:
            input("Press Enter to continue...")


