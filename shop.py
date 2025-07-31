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
    
    def visit_shop(self):
        """Visit the shop to buy items"""
        while True:
            console.clear()
            
            # Shop welcome banner
            shop_banner = Panel.fit(
                "🏪 MERCHANT'S SHOP 🏪\n\n"
                "[cyan]Welcome, brave adventurer![/cyan]\n"
                "[dim]\"I have the finest potions in the realm!\"[/dim]",
                title="⚖️ MAGICAL EMPORIUM ⚖️",
                border_style="gold1"
            )
            console.print(shop_banner)
            
            # Player status display
            self._display_player_status()
            
            # Calculate potion prices based on player level
            health_potion_price = 15 + (self.player.level * 2)
            mana_potion_price = 12 + (self.player.level * 2)
            
            # Items for sale table
            items_table = Table(title="🛍️ Items for Sale")
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
            
            # Shop menu
            console.print("\n🛒 What would you like to do?", style="bold cyan")
            
            menu_table = Table(show_header=False, box=None, padding=(0, 2))
            menu_table.add_column("Choice", style="yellow", width=3)
            menu_table.add_column("Action", style="cyan")
            menu_table.add_column("Status", style="dim")
            
            # Health potion option
            health_status = "" if self.player.gold >= health_potion_price else "(Not enough gold)"
            menu_table.add_row("1", "🧪 Buy Health Potion", health_status)
            
            # Mana potion option
            mana_status = "" if self.player.gold >= mana_potion_price else "(Not enough gold)"
            menu_table.add_row("2", "🔮 Buy Mana Potion", mana_status)
            
            menu_table.add_row("3", "🚪 Leave Shop", "")
            
            console.print(menu_table)
            
            choice = Prompt.ask("Enter your choice", choices=["1", "2", "3"], default="3")
            
            if choice == "1":
                success = self._buy_item("health_potion", health_potion_price, "Health Potion")
                if success and not Confirm.ask("\n🛍️ Would you like to buy another item?", default=True):
                    break
                elif not success:
                    console.input("\nPress Enter to continue...")
                    
            elif choice == "2":
                success = self._buy_item("mana_potion", mana_potion_price, "Mana Potion")
                if success and not Confirm.ask("\n🛍️ Would you like to buy another item?", default=True):
                    break
                elif not success:
                    console.input("\nPress Enter to continue...")
                    
            elif choice == "3":
                # Farewell message
                farewell_panel = Panel.fit(
                    "Thank you for visiting!\n"
                    "Come back anytime, adventurer!\n"
                    "May fortune favor your journey! ⚔️✨",
                    title="👋 Safe Travels",
                    border_style="green"
                )
                console.print(farewell_panel)
                console.input("Press Enter to continue...")
                break
    
    def _display_player_status(self):
        """Display current player gold and inventory"""
        status_text = Text()
        status_text.append("💰 Your Gold: ", style="yellow")
        status_text.append(f"{self.player.gold}", style="bold gold1")
        status_text.append(" | 🎒 Inventory: ", style="cyan")
        status_text.append(f"🧪 {self.player.inventory['health_potions']} health", style="red")
        status_text.append(" | ", style="dim")
        status_text.append(f"🔮 {self.player.inventory['mana_potions']} mana", style="blue")
        
        console.print(Panel(Align.center(status_text), border_style="cyan"))
    
    def _buy_item(self, item_type, price, item_name):
        """Buy an item from the shop"""
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
    
    def display_shop_info(self):
        """Display information about the shop (could be used for help)"""
        info_text = Text()
        info_text.append("🏪 Shop Information\n\n", style="bold cyan")
        info_text.append("• Potions scale with your level for better effects\n", style="white")
        info_text.append("• Prices increase as you level up\n", style="white")
        info_text.append("• Stock is unlimited - buy as many as you can afford\n", style="white")
        info_text.append("• Health potions restore HP instantly\n", style="red")
        info_text.append("• Mana potions restore mana for special attacks\n", style="blue")
        
        console.print(Panel(info_text, title="ℹ️ Shop Guide", border_style="blue"))
        console.input("\nPress Enter to continue...")