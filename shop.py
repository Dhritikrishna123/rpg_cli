from utils import get_user_choice, clear_screen

class Shop:
    def __init__(self, player):
        self.player = player
    
    def visit_shop(self):
        """Visit the shop to buy items"""
        while True:
            clear_screen()
            print("=" * 40)
            print("        MERCHANT'S SHOP")
            print("=" * 40)
            print("Welcome, adventurer! What would you like to buy?")
            print()
            print(f"Your Gold: {self.player.gold}")
            print(f"Health Potions: {self.player.inventory['health_potions']}")
            print(f"Mana Potions: {self.player.inventory['mana_potions']}")
            print()
            
            # Calculate potion prices based on player level
            health_potion_price = 15 + (self.player.level * 2)
            mana_potion_price = 12 + (self.player.level * 2)
            
            print("Items for sale:")
            print(f"1. Health Potion - {health_potion_price} gold")
            print("   (Restores 30 + Level*5 HP)")
            print(f"2. Mana Potion - {mana_potion_price} gold")
            print("   (Restores 25 + Level*3 Mana)")
            print("3. Leave shop")
            
            choice = get_user_choice("Enter your choice (1-3): ", ["1", "2", "3"])
            
            if choice == "1":
                if self._buy_item("health_potion", health_potion_price):
                    continue_shopping = get_user_choice("\nWould you like to buy another item? (y/n): ", ["y", "n", "yes", "no"])
                    if continue_shopping.lower() in ["n", "no"]:
                        break
                else:
                    input("\nPress Enter to continue...")
                    
            elif choice == "2":
                if self._buy_item("mana_potion", mana_potion_price):
                    continue_shopping = get_user_choice("\nWould you like to buy another item? (y/n): ", ["y", "n", "yes", "no"])
                    if continue_shopping.lower() in ["n", "no"]:
                        break
                else:
                    input("\nPress Enter to continue...")
                    
            elif choice == "3":
                print("\nThank you for visiting! Come back anytime!")
                input("Press Enter to continue...")
                break
    
    def _buy_item(self, item_type, price):
        """Buy an item from the shop"""
        if self.player.gold >= price:
            self.player.gold -= price
            
            if item_type == "health_potion":
                self.player.inventory["health_potions"] += 1
                item_name = "Health Potion"
            else:
                self.player.inventory["mana_potions"] += 1
                item_name = "Mana Potion"
            
            print(f"\nYou bought a {item_name} for {price} gold!")
            print(f"Remaining gold: {self.player.gold}")
            print(f"Total {item_name.lower()}s: {self.player.inventory[item_type + 's']}")
            return True
        else:
            print(f"\nYou don't have enough gold!")
            print(f"You need {price} gold, but only have {self.player.gold} gold.")
            return False
