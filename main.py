# main.py - Main game file
import random
from player import create_player, level_up_player, use_health_potion, use_mana_potion
from combat import battle_monster
from shop import visit_shop
from utils import clear_screen, get_user_choice

def main():
    """Main game loop"""
    clear_screen()
    print("=" * 50)
    print("      WELCOME TO PYTHON ADVENTURE RPG!")
    print("=" * 50)
    print()
    
    # Create player character
    player = create_player()
    
    print(f"\nWelcome, {player['name']} the {player['class']}!")
    print("Your adventure begins now...")
    input("\nPress Enter to continue...")
    
    # Main game loop
    while True:
        clear_screen()
        print("=" * 50)
        print(f"  {player['name']} - Level {player['level']} {player['class']}")
        print("=" * 50)
        print(f"HP: {player['hp']}/{player['max_hp']} | Mana: {player['mana']}/{player['max_mana']} | Gold: {player['gold']}")
        print(f"Attack: {player['attack']} | XP: {player['xp']}/{player['xp_to_next']}")
        print(f"Special Attack Cooldown: {player['special_cooldown']} turns")
        print(f"Health Potions: {player['inventory']['health_potions']} | Mana Potions: {player['inventory']['mana_potions']}")
        print()
        
        print("What would you like to do?")
        print("1. Fight a monster")
        print("2. Visit the shop")
        print("3. Use a health potion")
        print("4. Use a mana potion")
        print("5. View character info")
        print("6. Quit game")
        
        choice = get_user_choice("Enter your choice (1-6): ", ["1", "2", "3", "4", "5", "6"])
        
        if choice == "1":
            # Fight a monster
            battle_result = battle_monster(player)
            if battle_result == "victory":
                # Gain XP and gold
                xp_gained = random.randint(10, 20) + (player['level'] * 2)
                gold_gained = random.randint(5, 15) + player['level']
                
                player['xp'] += xp_gained
                player['gold'] += gold_gained
                
                print(f"\nYou gained {xp_gained} XP and {gold_gained} gold!")
                
                # Check for level up
                if player['xp'] >= player['xp_to_next']:
                    level_up_player(player)
                
                input("\nPress Enter to continue...")
                
            elif battle_result == "defeat":
                print("\nGAME OVER!")
                print("You have been defeated in battle...")
                print("Thanks for playing Python Adventure RPG!")
                break
                
        elif choice == "2":
            # Visit shop
            visit_shop(player)
            
        elif choice == "3":
            # Use health potion
            use_health_potion(player)
            input("\nPress Enter to continue...")
            
        elif choice == "4":
            # Use mana potion
            use_mana_potion(player)
            input("\nPress Enter to continue...")
            
        elif choice == "5":
            # View character info
            clear_screen()
            print("=" * 30)
            print("    CHARACTER INFORMATION")
            print("=" * 30)
            print(f"Name: {player['name']}")
            print(f"Class: {player['class']}")
            print(f"Level: {player['level']}")
            print(f"HP: {player['hp']}/{player['max_hp']}")
            print(f"Mana: {player['mana']}/{player['max_mana']}")
            print(f"Attack: {player['attack']}")
            print(f"XP: {player['xp']}/{player['xp_to_next']}")
            print(f"Gold: {player['gold']}")
            print(f"Health Potions: {player['inventory']['health_potions']}")
            print(f"Mana Potions: {player['inventory']['mana_potions']}")
            print(f"Special Attack Cooldown: {player['special_cooldown']} turns")
            input("\nPress Enter to continue...")
            
        elif choice == "6":
            # Quit game
            print("\nThanks for playing Python Adventure RPG!")
            print("Come back soon for more adventures!")
            break

if __name__ == "__main__":
    main()