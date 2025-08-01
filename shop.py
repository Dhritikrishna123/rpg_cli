import random
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.align import Align

console = Console()

class Shop:
    def __init__(self, player):
        self.player = player
        
        # NEW: Shop keeper dialogue system
        self.greetings = {
            "low_gold": [
                "Looking a bit light on coin, eh? Maybe some smaller purchases today?",
                "Every adventurer starts somewhere! What can I get you?",
                "Don't worry about the gold - fame comes to those who persevere!"
            ],
            "high_gold": [
                "Ah, a wealthy adventurer! I have the finest wares for you!",
                "Your coin purse looks heavy - let me show you my premium items!",
                "Welcome, valued customer! My best items await!"
            ],
            "high_level": [
                "A legendary hero graces my shop! I have rare items worthy of your skill!",
                "Tales of your adventures reach even here! What can I craft for you?",
                "Such power... let me offer equipment fit for a champion!"
            ],
            "regular": [
                "Welcome to my shop, adventurer!",
                "What can I interest you in today?",
                "Browse my wares - I have everything an adventurer needs!"
            ]
        }
        
        self.farewells = [
            "Safe travels, and may fortune favor you!",
            "Come back when you need more supplies!",
            "Your business is always welcome here!",
            "Go forth and seek glory, brave one!"
        ]
        
        # NEW: Equipment database
        self.equipment_db = {
            "weapons": {
                1: [
                    {"name": "Iron Sword", "attack_bonus": 5, "price": 100, "description": "A sturdy iron blade"},
                    {"name": "Wooden Staff", "attack_bonus": 3, "mana_bonus": 10, "price": 80, "description": "A simple mage's staff"}
                ],
                5: [
                    {"name": "Steel Sword", "attack_bonus": 10, "price": 250, "description": "A sharp steel blade"},
                    {"name": "Mystic Wand", "attack_bonus": 8, "mana_bonus": 20, "price": 300, "description": "A wand crackling with energy"},
                    {"name": "Shadow Dagger", "attack_bonus": 12, "price": 280, "description": "A swift assassin's blade"}
                ],
                10: [
                    {"name": "Enchanted Blade", "attack_bonus": 18, "price": 500, "description": "A magically enhanced sword"},
                    {"name": "Arcane Staff", "attack_bonus": 15, "mana_bonus": 35, "price": 550, "description": "A staff of pure magical energy"},
                    {"name": "Venom Dagger", "attack_bonus": 20, "price": 480, "description": "A poisoned assassin's weapon"}
                ],
                15: [
                    {"name": "Dragon Slayer", "attack_bonus": 25, "price": 800, "description": "Forged from dragon scales"},
                    {"name": "Staff of Power", "attack_bonus": 22, "mana_bonus": 50, "price": 900, "description": "Ultimate magical focus"},
                    {"name": "Shadow Strike", "attack_bonus": 28, "price": 750, "description": "Blade of legendary assassins"}
                ]
            },
            "armor": {
                1: [
                    {"name": "Leather Armor", "hp_bonus": 20, "price": 120, "description": "Basic protective gear"},
                    {"name": "Cloth Robes", "hp_bonus": 10, "mana_bonus": 15, "price": 100, "description": "Simple mage robes"}
                ],
                5: [
                    {"name": "Chain Mail", "hp_bonus": 40, "price": 300, "description": "Interlocked metal protection"},
                    {"name": "Enchanted Robes", "hp_bonus": 25, "mana_bonus": 30, "price": 350, "description": "Magically woven fabric"},
                    {"name": "Studded Leather", "hp_bonus": 35, "price": 280, "description": "Reinforced leather armor"}
                ],
                10: [
                    {"name": "Plate Armor", "hp_bonus": 70, "price": 600, "description": "Heavy metal protection"},
                    {"name": "Mystic Vestments", "hp_bonus": 45, "mana_bonus": 50, "price": 650, "description": "Robes of ancient power"},
                    {"name": "Shadow Cloak", "hp_bonus": 55, "price": 580, "description": "Armor of stealth masters"}
                ],
                15: [
                    {"name": "Dragon Scale Mail", "hp_bonus": 100, "price": 1000, "description": "Armor of dragon hide"},
                    {"name": "Archmage Robes", "hp_bonus": 70, "mana_bonus": 80, "price": 1200, "description": "Robes of magical mastery"},
                    {"name": "Void Leather", "hp_bonus": 85, "price": 950, "description": "Armor touched by shadow"}
                ]
            }
        }
    
    def get_greeting(self):
        """Get appropriate greeting based on player status"""
        if self.player.gold < 50:
            return random.choice(self.greetings["low_gold"])
        elif self.player.gold > 500:
            return random.choice(self.greetings["high_gold"])
        elif self.player.level > 10:
            return random.choice(self.greetings["high_level"])
        else:
            return random.choice(self.greetings["regular"])
    
    def get_available_equipment(self, equipment_type):
        """Get equipment available for player's level"""
        available = []
        equipment_levels = sorted(self.equipment_db[equipment_type].keys())
        
        for level_req in equipment_levels:
            if self.player.level >= level_req:
                available.extend(self.equipment_db[equipment_type][level_req])
        
        return available
    
    def visit_shop(self):
        """Visit the shop to buy items"""
        while True:
            console.clear()
            
            # Shop welcome banner with dynamic greeting
            greeting = self.get_greeting()
            shop_banner = Panel.fit(
                f"🏪 MERCHANT'S SHOP 🏪\n\n"
                f"[cyan]{greeting}[/cyan]",
                title="⚖️ MAGICAL EMPORIUM ⚖️",
                border_style="gold1"
            )
            console.print(shop_banner)
            
            # Player status display
            self._display_player_status()
            
            # Main shop menu
            console.print("\n🛒 What would you like to browse?", style="bold cyan")
            
            menu_table = Table(show_header=False, box=None, padding=(0, 2))
            menu_table.add_column("Choice", style="yellow", width=3)
            menu_table.add_column("Category", style="cyan")
            menu_table.add_column("Description", style="dim")
            
            menu_table.add_row("1", "🧪 Potions", "Health and mana restoration")
            menu_table.add_row("2", "⚔️ Weapons", "Increase your attack power")
            menu_table.add_row("3", "🛡️ Armor", "Boost your health and defense")
            menu_table.add_row("4", "💰 Sell Items", "Convert items to gold")
            menu_table.add_row("5", "🚪 Leave Shop", "Exit the shop")
            
            console.print(menu_table)
            
            choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5"], default="5")
            
            if choice == "1":
                self._visit_potion_shop()
            elif choice == "2":
                self._visit_weapon_shop()
            elif choice == "3":
                self._visit_armor_shop()
            elif choice == "4":
                self._visit_sell_shop()
            elif choice == "5":
                # Farewell message
                farewell = random.choice(self.farewells)
                farewell_panel = Panel.fit(
                    f"{farewell}\n\n⚔️✨ May your adventures be legendary! ✨⚔️",
                    title="👋 Safe Travels",
                    border_style="green"
                )
                console.print(farewell_panel)
                console.input("Press Enter to continue...")
                break
    
    def _visit_potion_shop(self):
        """Visit the potion section of the shop"""
        while True:
            console.clear()
            
            console.print(Panel.fit("🧪 POTION SHOP 🧪\n\"Finest elixirs in the realm!\"", 
                                  title="⚗️ ALCHEMY CORNER", border_style="blue"))
            
            self._display_player_status()
            
            # Calculate potion prices based on player level
            health_potion_price = 15 + (self.player.level * 2)
            mana_potion_price = 12 + (self.player.level * 2)
            
            # Items for sale table
            items_table = Table(title="🛍️ Potions for Sale")
            items_table.add_column("Item", style="cyan", no_wrap=True)
            items_table.add_column("Price", style="gold1", justify="right")
            items_table.add_column("Effect", style="green")
            items_table.add_column("Stock", style="blue")
            
            # Health potion info
            health_heal = 30 + (self.player.level * 5)
            health_affordable = "✅" if self.player.gold >= health_potion_price else "❌"
            items_table.add_row(
                "🧪 Health Potion",
                f"{health_potion_price} gold",
                f"Restores {health_heal} HP",
                f"{health_affordable} Available"
            )
            
            # Mana potion info
            mana_restore = 25 + (self.player.level * 3)
            mana_affordable = "✅" if self.player.gold >= mana_potion_price else "❌"
            items_table.add_row(
                "🔮 Mana Potion",
                f"{mana_potion_price} gold",
                f"Restores {mana_restore} Mana",
                f"{mana_affordable} Available"
            )
            
            console.print(items_table)
            
            # Potion menu
            console.print("\n🛒 What would you like to do?", style="bold cyan")
            
            potion_menu = Table(show_header=False, box=None, padding=(0, 2))
            potion_menu.add_column("Choice", style="yellow", width=3)
            potion_menu.add_column("Action", style="cyan")
            
            potion_menu.add_row("1", "🧪 Buy Health Potion")
            potion_menu.add_row("2", "🔮 Buy Mana Potion")
            potion_menu.add_row("3", "🔙 Back to Main Shop")
            
            console.print(potion_menu)
            
            choice = Prompt.ask("Enter your choice", choices=["1", "2", "3"], default="3")
            
            if choice == "1":
                success = self._buy_item("health_potion", health_potion_price, "Health Potion")
                if not success:
                    console.input("\nPress Enter to continue...")
            elif choice == "2":
                success = self._buy_item("mana_potion", mana_potion_price, "Mana Potion")
                if not success:
                    console.input("\nPress Enter to continue...")
            elif choice == "3":
                break
    
    def _visit_weapon_shop(self):
        """Visit the weapon section of the shop"""
        console.clear()
        
        available_weapons = self.get_available_equipment("weapons")
        
        if not available_weapons:
            console.print(Panel("No weapons available for your level yet!", 
                               title="⚔️ Weapon Shop", border_style="red"))
            console.input("Press Enter to continue...")
            return
        
        console.print(Panel.fit("⚔️ WEAPON SHOP ⚔️\n\"Blades forged for heroes!\"", 
                              title="🗡️ ARMORY", border_style="red"))
        
        self._display_player_status()
        
        # Display current weapon
        current_weapon = self.player.equipment.get("weapon")
        if current_weapon:
            console.print(f"Current Weapon: [bold green]{current_weapon['name']}[/bold green] (+{current_weapon['attack_bonus']} Attack)")
        else:
            console.print("Current Weapon: [dim]None equipped[/dim]")
        
        # Weapons table
        weapons_table = Table(title="🗡️ Available Weapons")
        weapons_table.add_column("Item", style="cyan")
        weapons_table.add_column("Attack Bonus", style="red")
        weapons_table.add_column("Price", style="gold1")
        weapons_table.add_column("Description", style="green")
        weapons_table.add_column("Affordable", style="blue")
        
        for i, weapon in enumerate(available_weapons, 1):
            affordable = "✅" if self.player.gold >= weapon["price"] else "❌"
            weapons_table.add_row(
                f"{i}. {weapon['name']}",
                f"+{weapon['attack_bonus']}",
                f"{weapon['price']} gold",
                weapon["description"],
                affordable
            )
        
        console.print(weapons_table)
        
        # Purchase menu
        choices = [str(i) for i in range(1, len(available_weapons) + 1)] + ["back"]
        choice = Prompt.ask("Choose weapon to buy (or 'back')", choices=choices, default="back")
        
        if choice != "back":
            weapon_index = int(choice) - 1
            weapon = available_weapons[weapon_index]
            self._buy_equipment("weapon", weapon)
        
        console.input("\nPress Enter to continue...")
    
    def _visit_armor_shop(self):
        """Visit the armor section of the shop"""
        console.clear()
        
        available_armor = self.get_available_equipment("armor")
        
        if not available_armor:
            console.print(Panel("No armor available for your level yet!", 
                               title="🛡️ Armor Shop", border_style="red"))
            console.input("Press Enter to continue...")
            return
        
        console.print(Panel.fit("🛡️ ARMOR SHOP 🛡️\n\"Protection fit for champions!\"", 
                              title="🛡️ DEFENSE DEPOT", border_style="blue"))
        
        self._display_player_status()
        
        # Display current armor
        current_armor = self.player.equipment.get("armor")
        if current_armor:
            console.print(f"Current Armor: [bold green]{current_armor['name']}[/bold green] (+{current_armor['hp_bonus']} HP)")
        else:
            console.print("Current Armor: [dim]None equipped[/dim]")
        
        # Armor table
        armor_table = Table(title="🛡️ Available Armor")
        armor_table.add_column("Item", style="cyan")
        armor_table.add_column("HP Bonus", style="red")
        armor_table.add_column("Mana Bonus", style="blue")
        armor_table.add_column("Price", style="gold1")
        armor_table.add_column("Affordable", style="green")
        
        for i, armor in enumerate(available_armor, 1):
            affordable = "✅" if self.player.gold >= armor["price"] else "❌"
            mana_bonus = f"+{armor.get('mana_bonus', 0)}" if armor.get('mana_bonus', 0) > 0 else "-"
            armor_table.add_row(
                f"{i}. {armor['name']}",
                f"+{armor['hp_bonus']}",
                mana_bonus,
                f"{armor['price']} gold",
                affordable
            )
        
        console.print(armor_table)
        
        # Purchase menu
        choices = [str(i) for i in range(1, len(available_armor) + 1)] + ["back"]
        choice = Prompt.ask("Choose armor to buy (or 'back')", choices=choices, default="back")
        
        if choice != "back":
            armor_index = int(choice) - 1
            armor = available_armor[armor_index]
            self._buy_equipment("armor", armor)
        
        console.input("\nPress Enter to continue...")
    
    def _visit_sell_shop(self):
        """Visit the sell section of the shop"""
        console.clear()
        
        console.print(Panel.fit("💰 ITEM EXCHANGE 💰\n\"Turn your treasures into gold!\"", 
                              title="💱 TRADING POST", border_style="gold1"))
        
        self._display_player_status()
        
        # Calculate sell prices (50% of buy price)
        health_sell_price = max(1, (15 + (self.player.level * 2)) // 2)
        mana_sell_price = max(1, (12 + (self.player.level * 2)) // 2)
        
        # Sellable items table
        sell_table = Table(title="💰 Items You Can Sell")
        sell_table.add_column("Item", style="cyan")
        sell_table.add_column("Quantity", style="green")
        sell_table.add_column("Sell Price", style="gold1")
        sell_table.add_column("Total Value", style="blue")
        
        # Health potions
        health_qty = self.player.inventory.get("health_potions", 0)
        if health_qty > 0:
            sell_table.add_row(
                "🧪 Health Potion",
                str(health_qty),
                f"{health_sell_price} gold each",
                f"{health_sell_price * health_qty} gold total"
            )
        
        # Mana potions
        mana_qty = self.player.inventory.get("mana_potions", 0)
        if mana_qty > 0:
            sell_table.add_row(
                "🔮 Mana Potion",
                str(mana_qty),
                f"{mana_sell_price} gold each",
                f"{mana_sell_price * mana_qty} gold total"
            )
        
        # Equipment
        current_weapon = self.player.equipment.get("weapon")
        if current_weapon:
            weapon_sell_price = current_weapon["price"] // 3  # 33% of original price
            sell_table.add_row(
                f"⚔️ {current_weapon['name']}",
                "1",
                f"{weapon_sell_price} gold",
                f"{weapon_sell_price} gold"
            )
        
        current_armor = self.player.equipment.get("armor")
        if current_armor:
            armor_sell_price = current_armor["price"] // 3
            sell_table.add_row(
                f"🛡️ {current_armor['name']}",
                "1", 
                f"{armor_sell_price} gold",
                f"{armor_sell_price} gold"
            )
        
        console.print(sell_table)
        
        if health_qty == 0 and mana_qty == 0 and not current_weapon and not current_armor:
            console.print("❌ You have nothing to sell!", style="bold red")
            console.input("Press Enter to continue...")
            return
        
        # Sell menu
        sell_choices = []
        if health_qty > 0:
            sell_choices.append("health")
        if mana_qty > 0:
            sell_choices.append("mana")
        if current_weapon:
            sell_choices.append("weapon")
        if current_armor:
            sell_choices.append("armor")
        sell_choices.append("back")
        
        choice = Prompt.ask("What would you like to sell? (health/mana/weapon/armor/back)", choices=sell_choices, default="back")
        
        if choice == "health" and health_qty > 0:
            quantity = int(Prompt.ask(f"How many health potions? (1-{health_qty})", default="1"))
            quantity = max(1, min(quantity, health_qty))
            total_gold = health_sell_price * quantity
            
            if Confirm.ask(f"Sell {quantity} health potion(s) for {total_gold} gold?"):
                self.player._inventory["health_potions"] -= quantity
                self.player.gold += total_gold
                console.print(f"✅ Sold {quantity} health potion(s) for {total_gold} gold!", style="bold green")
        
        elif choice == "mana" and mana_qty > 0:
            quantity = int(Prompt.ask(f"How many mana potions? (1-{mana_qty})", default="1"))
            quantity = max(1, min(quantity, mana_qty))
            total_gold = mana_sell_price * quantity
            
            if Confirm.ask(f"Sell {quantity} mana potion(s) for {total_gold} gold?"):
                self.player._inventory["mana_potions"] -= quantity
                self.player.gold += total_gold
                console.print(f"✅ Sold {quantity} mana potion(s) for {total_gold} gold!", style="bold green")
        
        elif choice == "weapon" and current_weapon:
            weapon_sell_price = current_weapon["price"] // 3
            if Confirm.ask(f"Sell {current_weapon['name']} for {weapon_sell_price} gold?"):
                self.player._equipment["weapon"] = None
                self.player.gold += weapon_sell_price
                console.print(f"✅ Sold {current_weapon['name']} for {weapon_sell_price} gold!", style="bold green")
        
        elif choice == "armor" and current_armor:
            armor_sell_price = current_armor["price"] // 3
            if Confirm.ask(f"Sell {current_armor['name']} for {armor_sell_price} gold?"):
                self.player._equipment["armor"] = None
                self.player.gold += armor_sell_price
                console.print(f"✅ Sold {current_armor['name']} for {armor_sell_price} gold!", style="bold green")
        
        console.input("\nPress Enter to continue...")
    
    def _display_player_status(self):
        """Display current player gold and inventory"""
        status_text = Text()
        status_text.append("💰 Your Gold: ", style="yellow")
        status_text.append(f"{self.player.gold}", style="bold gold1")
        status_text.append(f" | Level: {self.player.level}", style="cyan")
        status_text.append(" | 🎒 Inventory: ", style="cyan")
        status_text.append(f"🧪 {self.player.inventory['health_potions']} health", style="red")
        status_text.append(" | ", style="dim")
        status_text.append(f"🔮 {self.player.inventory['mana_potions']} mana", style="blue")
        
        console.print(Panel(Align.center(status_text), border_style="cyan"))
    
    def _buy_item(self, item_type, price, item_name):
        """Buy a potion from the shop"""
        if self.player.gold >= price:
            self.player.gold -= price
            
            if item_type == "health_potion":
                self.player._inventory["health_potions"] += 1
                icon = "🧪"
                color = "red"
            else:
                self.player._inventory["mana_potions"] += 1
                icon = "🔮"
                color = "blue"
            
            # Purchase success message
            success_text = Text()
            success_text.append("✅ Purchase Successful!\n\n", style="bold green")
            success_text.append(f"You bought a ", style="white")
            success_text.append(f"{icon} {item_name}", style=f"bold {color}")
            success_text.append(f" for ", style="white")
            success_text.append(f"{price} gold", style="gold1")
            success_text.append("!\n\n", style="white")
            
            success_text.append("💰 Remaining gold: ", style="yellow")
            success_text.append(f"{self.player.gold}", style="bold gold1")
            success_text.append(f"\n{icon} Total {item_name.lower()}s: ", style=color)
            success_text.append(f"{self.player.inventory[item_type + 's']}", style=f"bold {color}")
            
            console.print(Panel(success_text, title="🛍️ Transaction Complete", border_style="green"))
            return True
        else:
            # Insufficient funds message
            needed = price - self.player.gold
            error_text = Text()
            error_text.append("❌ Insufficient Funds!\n\n", style="bold red")
            error_text.append(f"You need ", style="white")
            error_text.append(f"{price} gold", style="gold1")
            error_text.append(f" but only have ", style="white")
            error_text.append(f"{self.player.gold} gold", style="gold1")
            error_text.append(".\n\n", style="white")
            error_text.append(f"You need ", style="yellow")
            error_text.append(f"{needed} more gold", style="bold gold1")
            error_text.append(".", style="yellow")
            
            console.print(Panel(error_text, title="💸 Transaction Failed", border_style="red"))
            return False
    
    def _buy_equipment(self, equipment_type, item):
        """Buy equipment from the shop"""
        if self.player.gold >= item["price"]:
            if Confirm.ask(f"Buy {item['name']} for {item['price']} gold?"):
                self.player.gold -= item["price"]
                old_item = self.player.equip_item(equipment_type, item)
                
                # Show purchase success
                success_text = Text()
                success_text.append("✅ Equipment Purchased!\n\n", style="bold green")
                success_text.append(f"You bought ", style="white")
                success_text.append(f"{item['name']}", style="bold cyan")
                success_text.append(f" for ", style="white")
                success_text.append(f"{item['price']} gold", style="gold1")
                success_text.append("!\n\n", style="white")
                
                if old_item:
                    success_text.append(f"Replaced: {old_item['name']}\n", style="dim")
                
                success_text.append("💰 Remaining gold: ", style="yellow")
                success_text.append(f"{self.player.gold}", style="bold gold1")
                
                console.print(Panel(success_text, title="🛍️ Equipment Upgraded", border_style="green"))
        else:
            needed = item["price"] - self.player.gold
            console.print(f"❌ You need {needed} more gold to buy this item!", style="bold red")
    
    def display_shop_info(self):
        """Display information about the shop"""
        info_text = Text()
        info_text.append("🏪 Shop Information\n\n", style="bold cyan")
        info_text.append("• Potions scale with your level for better effects\n", style="white")
        info_text.append("• Prices increase as you level up\n", style="white")
        info_text.append("• Equipment unlocks as you gain levels\n", style="white")
        info_text.append("• You can sell items for gold (at reduced prices)\n", style="white")
        info_text.append("• Shop keeper dialogue changes based on your status\n", style="white")
        
        console.print(Panel(info_text, title="ℹ️ Shop Guide", border_style="blue"))
        console.input("\nPress Enter to continue...")