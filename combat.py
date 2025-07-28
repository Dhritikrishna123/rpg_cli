# combat.py - Combat system
import random
from player import use_special_attack, reduce_special_cooldown, use_health_potion, use_mana_potion
from monsters import create_monster
from utils import get_user_choice, clear_screen

def battle_monster(player):
    """Main battle function"""
    # Create a monster based on player level
    monster = create_monster(player["level"])
    
    clear_screen()
    print("=" * 50)
    print("           BATTLE BEGINS!")
    print("=" * 50)
    print(f"A wild {monster['name']} appears!")
    print(f"{monster['name']} - HP: {monster['hp']}, Attack: {monster['attack']}")
    input("\nPress Enter to start battle...")
    
    # Battle loop
    turn = 1
    while monster["hp"] > 0 and player["hp"] > 0:
        clear_screen()
        print("=" * 50)
        print(f"           BATTLE - Turn {turn}")
        print("=" * 50)
        print(f"Enemy: {monster['name']} - HP: {monster['hp']}/{monster['max_hp']}")
        print(f"You: {player['name']} - HP: {player['hp']}/{player['max_hp']} | Mana: {player['mana']}/{player['max_mana']}")
        print(f"Gold: {player['gold']} | Health Potions: {player['inventory']['health_potions']} | Mana Potions: {player['inventory']['mana_potions']}")
        print(f"Special Attack Cooldown: {player['special_cooldown']} turns | Mana Cost: {player['special_mana_cost']}")
        print()
        
        # Player turn
        print("Choose your action:")
        print("1. Regular Attack")
        
        # Show special attack status
        special_status = ""
        if player['special_cooldown'] > 0:
            special_status = f" (COOLDOWN: {player['special_cooldown']} turns)"
        elif player['mana'] < player['special_mana_cost']:
            special_status = f" (Need {player['special_mana_cost']} mana, have {player['mana']})"
        
        print(f"2. Special Attack{special_status}")
        print("3. Use Health Potion")
        print("4. Use Mana Potion") 
        print("5. Try to Run Away")
        
        choice = get_user_choice("Enter your choice (1-5): ", ["1", "2", "3", "4", "5"])
        
        player_damage = 0
        
        if choice == "1":
            # Regular attack
            damage_variance = random.randint(-3, 3)
            player_damage = player["attack"] + damage_variance
            print(f"\nYou attack {monster['name']} for {player_damage} damage!")
            
        elif choice == "2":
            # Special attack
            success, message = use_special_attack(player)
            if success:
                damage_variance = random.randint(-5, 5)
                player_damage = player["special_damage"] + damage_variance
                
                if player["class"] == "Warrior":
                    print(f"\nYou use MIGHTY SLASH on {monster['name']}!")
                elif player["class"] == "Mage":
                    print(f"\nYou cast FIREBALL on {monster['name']}!")
                else:  # Rogue
                    print(f"\nYou use SNEAK ATTACK on {monster['name']}!")
                
                print(f"Critical hit for {player_damage} damage!")
                print(f"Mana: {player['mana']}/{player['max_mana']}")
            else:
                print(f"\n{message}")
                input("Press Enter to continue...")
                continue
                
        elif choice == "3":
            # Use health potion
            use_health_potion(player)
            input("\nPress Enter to continue...")
            # Skip to monster turn without dealing damage
            
        elif choice == "4":
            # Use mana potion
            use_mana_potion(player)
            input("\nPress Enter to continue...")
            # Skip to monster turn without dealing damage
            
        elif choice == "5":
            # Try to run away
            escape_chance = random.randint(1, 100)
            if escape_chance <= 30:  # 30% chance to escape
                print(f"\nYou successfully escaped from {monster['name']}!")
                input("Press Enter to continue...")
                return "escaped"
            else:
                print(f"\nYou couldn't escape from {monster['name']}!")
                input("Press Enter to continue...")
        
        # Apply damage to monster
        if player_damage > 0:
            monster["hp"] -= player_damage
            input("\nPress Enter to continue...")
        
        # Check if monster is defeated
        if monster["hp"] <= 0:
            print(f"\n{monster['name']} is defeated!")
            print("Victory!")
            input("\nPress Enter to continue...")
            return "victory"
        
        # Monster turn (only if player didn't use potions)
        if choice not in ["3", "4"]:  # If player didn't use health or mana potion
            monster_damage_variance = random.randint(-2, 2)
            monster_damage = monster["attack"] + monster_damage_variance
            
            print(f"\n{monster['name']} attacks you for {monster_damage} damage!")
            player["hp"] -= monster_damage
            
            input("Press Enter to continue...")
            
            # Check if player is defeated
            if player["hp"] <= 0:
                print(f"\nYou have been defeated by {monster['name']}!")
                input("Press Enter to continue...")
                return "defeat"
        
        # Reduce special attack cooldown
        reduce_special_cooldown(player)
        turn += 1
    
    return "ongoing"

def display_battle_status(player, monster, turn):
    """Display current battle status"""
    print("=" * 50)
    print(f"           BATTLE - Turn {turn}")
    print("=" * 50)
    print(f"Enemy: {monster['name']} - HP: {monster['hp']}/{monster['max_hp']}")
    print(f"You: {player['name']} - HP: {player['hp']}/{player['max_hp']}")
    print(f"Special Attack Cooldown: {player['special_cooldown']} turns")
    print()