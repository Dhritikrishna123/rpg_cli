# shop.py - Shopping system
from utils import get_user_choice, clear_screen

def visit_shop(player):
    """Visit the shop to buy items"""
    while True:
        clear_screen()
        print("=" * 40)
        print("        MERCHANT'S SHOP")
        print("=" * 40)
        print("Welcome, adventurer! What would you like to buy?")
        print()
        print(f"Your Gold: {player['gold']}")
        print(f"Health Potions: {player['inventory']['health_potions']}")
        print(f"Mana Potions: {player['inventory']['mana_potions']}")
        print()
        
        # Calculate potion prices based on player level
        health_potion_price = 15 + (player['level'] * 2)
        mana_potion_price = 12 + (player['level'] * 2)
        
        print("Items for sale:")
        print(f"1. Health Potion - {health_potion_price} gold")
        print("   (Restores 30 + Level*5 HP)")
        print(f"2. Mana Potion - {mana_potion_price} gold")
        print("   (Restores 25 + Level*3 Mana)")
        print("3. Leave shop")
        
        choice = get_user_choice("Enter your choice (1-3): ", ["1", "2", "3"])
        
        if choice == "1":
            # Buy health potion
            if player['gold'] >= health_potion_price:
                player['gold'] -= health_potion_price
                player['inventory']['health_potions'] += 1
                
                print(f"\nYou bought a Health Potion for {health_potion_price} gold!")
                print(f"Remaining gold: {player['gold']}")
                print(f"Total health potions: {player['inventory']['health_potions']}")
                
                # Ask if they want to buy more
                print("\nWould you like to buy another item?")
                continue_shopping = get_user_choice("(y/n): ", ["y", "n", "yes", "no"])
                if continue_shopping.lower() in ["n", "no"]:
                    break
            else:
                print(f"\nYou don't have enough gold!")
                print(f"You need {health_potion_price} gold, but only have {player['gold']} gold.")
                input("\nPress Enter to continue...")
                
        elif choice == "2":
            # Buy mana potion
            if player['gold'] >= mana_potion_price:
                player['gold'] -= mana_potion_price
                player['inventory']['mana_potions'] += 1
                
                print(f"\nYou bought a Mana Potion for {mana_potion_price} gold!")
                print(f"Remaining gold: {player['gold']}")
                print(f"Total mana potions: {player['inventory']['mana_potions']}")
                
                # Ask if they want to buy more
                print("\nWould you like to buy another item?")
                continue_shopping = get_user_choice("(y/n): ", ["y", "n", "yes", "no"])
                if continue_shopping.lower() in ["n", "no"]:
                    break
            else:
                print(f"\nYou don't have enough gold!")
                print(f"You need {mana_potion_price} gold, but only have {player['gold']} gold.")
                input("\nPress Enter to continue...")
                
        elif choice == "3":
            # Leave shop
            print("\nThank you for visiting! Come back anytime!")
            input("Press Enter to continue...")
            break

def get_potion_price(player_level):
    """Calculate potion price based on player level"""
    return 15 + (player_level * 2)

def display_shop_welcome():
    """Display shop welcome message"""
    messages = [
        "Welcome to my humble shop, brave adventurer!",
        "Looking for supplies? You've come to the right place!",
        "Fresh potions, just brewed this morning!",
        "Quality goods for quality adventurers!",
        "Step right up! Don't be shy!"
    ]
    
    import random
    return random.choice(messages)