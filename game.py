import random
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from player import Player
from monsters import Monster
from combat import Combat
from shop import Shop

console = Console()

class Game:
    def __init__(self):
        self.player = None
        self.save_directory = "saves"
        
        # Create saves directory if it doesn't exist
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
    
    def start(self):
        """Start the game"""
        console.clear()
        
        # Game title with fancy styling
        title_panel = Panel.fit(
            "[bold magenta]🎮 PYTHON ADVENTURE RPG 🎮[/bold magenta]\n\n"
            "[cyan]Welcome to an epic fantasy adventure![/cyan]\n"
            "[dim]Prepare for battles, magic, and glory![/dim]",
            title="⚔️ EPIC ADVENTURE AWAITS ⚔️",
            border_style="gold1"
        )
        console.print(title_panel)
        
        # Main menu options
        menu_table = Table(title="🎯 Main Menu", show_header=False)
        menu_table.add_column("Option", style="cyan", no_wrap=True)
        menu_table.add_column("Description", style="green")
        
        menu_table.add_row("1", "🆕 New Game - Start a fresh adventure")
        menu_table.add_row("2", "📁 Load Game - Continue your journey")
        menu_table.add_row("3", "🚪 Quit - Exit the game")
        
        console.print(menu_table)
        
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3"], default="1")
        
        if choice == "1":
            self.player = Player.create_new_player()
            welcome_text = Text()
            welcome_text.append(f"Welcome, ", style="cyan")
            welcome_text.append(f"{self.player.name}", style="bold yellow")
            welcome_text.append(f" the {self.player.player_class}!", style="cyan")
            welcome_text.append("\n\nYour adventure begins now...", style="green")
            
            console.print(Panel(welcome_text, title="🌟 Adventure Begins", border_style="green"))
            console.input("\nPress Enter to continue...")
            self.main_game_loop()
        elif choice == "2":
            self.load_game()
        elif choice == "3":
            farewell_panel = Panel.fit(
                "Thanks for playing Python Adventure RPG!\n"
                "May your next adventure be legendary! ⚔️✨",
                title="👋 Farewell",
                border_style="blue"
            )
            console.print(farewell_panel)
            return
    
    def main_game_loop(self):
        """Main game loop"""
        while True:
            console.clear()
            
            # Display player status at top
            self._display_player_status()
            
            # Main game menu
            console.print("\n🎯 What would you like to do?", style="bold cyan")
            
            # Create action menu table
            action_table = Table(show_header=False, box=None)
            action_table.add_column("Choice", style="yellow", width=3)
            action_table.add_column("Action", style="cyan")
            action_table.add_column("Description", style="dim")
            
            action_table.add_row("1", "⚔️ Fight a monster", "Battle dangerous creatures")
            action_table.add_row("2", "🏪 Visit the shop", "Buy potions and supplies")
            action_table.add_row("3", "🧪 Use health potion", "Restore your HP")
            action_table.add_row("4", "🔮 Use mana potion", "Restore your mana")
            action_table.add_row("5", "📊 View character info", "Check detailed stats")
            action_table.add_row("6", "💾 Save game", "Save your progress")
            action_table.add_row("7", "📁 Load game", "Load a saved game")
            action_table.add_row("8", "🚪 Quit game", "Exit the adventure")
            
            console.print(action_table)
            
            choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5", "6", "7", "8"], default="1")
            
            if choice == "1":
                self.fight_monster()
            elif choice == "2":
                shop = Shop(self.player)
                shop.visit_shop()
            elif choice == "3":
                self._use_health_potion()
            elif choice == "4":
                self._use_mana_potion()
            elif choice == "5":
                self._view_character_info()
            elif choice == "6":
                self.save_game()
            elif choice == "7":
                self.load_game()
            elif choice == "8":
                if Confirm.ask("Are you sure you want to quit?"):
                    farewell_text = Text()
                    farewell_text.append("Thanks for playing Python Adventure RPG!\n", style="bold green")
                    farewell_text.append("Come back soon for more adventures! ⚔️✨", style="cyan")
                    
                    console.print(Panel(farewell_text, title="👋 See You Later", border_style="blue"))
                    break
    
    def _display_player_status(self):
        """Display current player status"""
        # Main status panel
        status_table = Table(title=f"🧙 {self.player.name} - Level {self.player.level} {self.player.player_class}")
        status_table.add_column("Attribute", style="cyan", width=12)
        status_table.add_column("Current", style="white", width=8)
        status_table.add_column("Visual", style="green", width=12)
        status_table.add_column("Status", style="yellow")
        
        # Create visual bars
        hp_bar = self._create_visual_bar(self.player.hp, self.player.max_hp, "red")
        mana_bar = self._create_visual_bar(self.player.mana, self.player.max_mana, "blue")
        xp_bar = self._create_visual_bar(self.player.xp, self.player.xp_to_next, "green")
        
        # Add rows
        status_table.add_row("❤️ Health", f"{self.player.hp}/{self.player.max_hp}", hp_bar, self._get_hp_status())
        status_table.add_row("🔮 Mana", f"{self.player.mana}/{self.player.max_mana}", mana_bar, self._get_mana_status())
        status_table.add_row("⭐ Experience", f"{self.player.xp}/{self.player.xp_to_next}", xp_bar, f"{self.player.xp_percentage:.1f}%")
        status_table.add_row("⚔️ Attack", str(self.player.attack), "", "")
        status_table.add_row("💰 Gold", str(self.player.gold), "", "")
        
        console.print(status_table)
        
        # Inventory and cooldown info
        info_text = Text()
        info_text.append("🎒 Inventory: ", style="bold cyan")
        info_text.append(f"🧪 {self.player.inventory['health_potions']} health ", style="red")
        info_text.append(f"🔮 {self.player.inventory['mana_potions']} mana ", style="blue")
        
        if self.player.special_cooldown > 0:
            info_text.append(f"| ⏰ Special cooldown: {self.player.special_cooldown} turns", style="yellow")
        else:
            info_text.append("| ✅ Special attack ready!", style="green")
        
        console.print(Panel(info_text, border_style="cyan"))
    
    def _create_visual_bar(self, current, maximum, color):
        """Create a visual progress bar"""
        if maximum <= 0:
            return f"[{color}]░░░░░░░░░░[/{color}]"
        
        percentage = current / maximum
        filled_blocks = int(percentage * 10)
        
        filled = "█" * filled_blocks
        empty = "░" * (10 - filled_blocks)
        return f"[{color}]{filled}[/{color}][dim]{empty}[/dim]"
    
    def _get_hp_status(self):
        """Get HP status description"""
        percentage = self.player.hp_percentage
        if percentage >= 80:
            return "[green]Excellent[/green]"
        elif percentage >= 60:
            return "[yellow]Good[/yellow]"
        elif percentage >= 30:
            return "[orange1]Wounded[/orange1]"
        else:
            return "[red]Critical[/red]"
    
    def _get_mana_status(self):
        """Get mana status description"""
        percentage = self.player.mana_percentage
        if percentage >= 80:
            return "[blue]Full Power[/blue]"
        elif percentage >= 50:
            return "[cyan]Adequate[/cyan]"
        elif percentage >= 25:
            return "[yellow]Low[/yellow]"
        else:
            return "[red]Depleted[/red]"
    
    def _use_health_potion(self):
        """Use a health potion from main menu"""
        if self.player.use_health_potion():
            console.input("\nPress Enter to continue...")
        else:
            console.input("\nPress Enter to continue...")
    
    def _use_mana_potion(self):
        """Use a mana potion from main menu"""
        if self.player.use_mana_potion():
            console.input("\nPress Enter to continue...")
        else:
            console.input("\nPress Enter to continue...")
    
    def _view_character_info(self):
        """View detailed character information"""
        console.clear()
        console.print(self.player.get_status_display())
        console.input("\nPress Enter to continue...")
    
    def fight_monster(self):
        """Fight a monster"""
        # Show loading animation
        with console.status("[bold green]🎲 Searching for monsters...", spinner="dots"):
            import time
            time.sleep(1)  # Dramatic pause
        
        monster = Monster.create_monster(self.player.level)
        
        # Monster encounter panel
        encounter_text = Text()
        encounter_text.append("🚨 MONSTER ENCOUNTER! 🚨\n\n", style="bold red")
        encounter_text.append(monster.get_combat_message("appears"), style="bold yellow")
        encounter_text.append(f"\n\n{monster.get_description()}", style="dim")
        
        console.print(Panel(encounter_text, title="⚔️ BATTLE INCOMING", border_style="red"))
        
        if not Confirm.ask("Do you want to fight this monster?", default=True):
            console.print("🏃 You decided to avoid the fight and retreat safely.", style="cyan")
            console.input("\nPress Enter to continue...")
            return
        
        combat = Combat(self.player, monster)
        battle_result = combat.start_battle()
        
        if battle_result == "victory":
            self._handle_victory(monster)
        elif battle_result == "defeat":
            self._handle_defeat()
        elif battle_result == "escaped":
            console.print("🏃 You successfully escaped from the battle!", style="bold yellow")
            console.input("\nPress Enter to continue...")
    
    def _handle_victory(self, monster):
        """Handle victory rewards"""
        # Calculate rewards
        base_xp = random.randint(10, 20)
        level_bonus_xp = self.player.level * 2
        monster_bonus_xp = monster.level * 3
        total_xp = base_xp + level_bonus_xp + monster_bonus_xp
        
        base_gold = random.randint(5, 15)
        level_bonus_gold = self.player.level * 2
        monster_bonus_gold = monster.level
        total_gold = base_gold + level_bonus_gold + monster_bonus_gold
        
        # Award rewards
        self.player.xp += total_xp
        self.player.gold += total_gold
        
        # Create victory panel
        victory_text = Text()
        victory_text.append("🏆 VICTORY! 🏆\n\n", style="bold gold1")
        victory_text.append(f"You defeated the {monster.name}!\n\n", style="green")
        victory_text.append("💰 Rewards Earned:\n", style="bold cyan")
        victory_text.append(f"⭐ XP: +{total_xp}\n", style="yellow")
        victory_text.append(f"💰 Gold: +{total_gold}", style="gold1")
        
        console.print(Panel(victory_text, title="🎉 BATTLE WON", border_style="green"))
        
        # Check for level up
        if self.player.xp >= self.player.xp_to_next:
            console.input("\nPress Enter to continue...")
            self.player.level_up()
        
        console.input("\nPress Enter to continue...")
    
    def _handle_defeat(self):
        """Handle player defeat"""
        defeat_panel = Panel.fit(
            "💀 GAME OVER 💀\n\n"
            "You have been defeated in battle...\n"
            "Your adventure ends here, but legends never die!\n\n"
            "Thanks for playing Python Adventure RPG!",
            title="⚰️ DEFEAT ⚰️",
            border_style="red"
        )
        console.print(defeat_panel)
        console.input("\nPress Enter to exit...")
        exit()
    
    def save_game(self):
        """Save the current game"""
        save_files = [f for f in os.listdir(self.save_directory) if f.endswith('.json')]
        
        console.print("\n💾 Save Game", style="bold cyan")
        
        if save_files:
            save_table = Table(title="Existing Save Files")
            save_table.add_column("Slot", style="cyan", no_wrap=True)
            save_table.add_column("File Name", style="green")
            
            for i, save_file in enumerate(save_files, 1):
                save_table.add_row(str(i), save_file)
            save_table.add_row(str(len(save_files) + 1), "[italic]Create new save file[/italic]")
            
            console.print(save_table)
            
            choice = Prompt.ask(f"Choose save slot", 
                               choices=[str(i) for i in range(1, len(save_files) + 2)],
                               default="1")
            
            if int(choice) <= len(save_files):
                filename = save_files[int(choice) - 1]
                if not Confirm.ask(f"Overwrite {filename}?"):
                    return
            else:
                filename = Prompt.ask("Enter save file name (without .json)").strip() + ".json"
        else:
            filename = Prompt.ask("Enter save file name (without .json)").strip() + ".json"
        
        filepath = os.path.join(self.save_directory, filename)
        if self.player.save_to_file(filepath):
            console.input("\nPress Enter to continue...")
    
    def load_game(self):
        """Load a saved game"""
        save_files = [f for f in os.listdir(self.save_directory) if f.endswith('.json')]
        
        if not save_files:
            no_saves_panel = Panel.fit(
                "No save files found!\n"
                "Start a new game to create your first save.",
                title="📁 No Saves",
                border_style="yellow"
            )
            console.print(no_saves_panel)
            console.input("Press Enter to continue...")
            return
        
        console.print("\n📁 Load Game", style="bold cyan")
        
        load_table = Table(title="Available Save Files")
        load_table.add_column("Slot", style="cyan", no_wrap=True)
        load_table.add_column("File Name", style="green")
        
        for i, save_file in enumerate(save_files, 1):
            load_table.add_row(str(i), save_file)
        
        console.print(load_table)
        
        choice = Prompt.ask(f"Choose save file", 
                           choices=[str(i) for i in range(1, len(save_files) + 1)],
                           default="1")
        
        filename = save_files[int(choice) - 1]
        filepath = os.path.join(self.save_directory, filename)
        
        loaded_player = Player.load_from_file(filepath)
        if loaded_player:
            self.player = loaded_player
            welcome_back_text = Text()
            welcome_back_text.append("Welcome back, ", style="cyan")
            welcome_back_text.append(f"{self.player.name}", style="bold yellow")
            welcome_back_text.append("!\nYour adventure continues...", style="cyan")
            
            console.print(Panel(welcome_back_text, title="🎮 Game Loaded", border_style="green"))
            console.input("\nPress Enter to continue...")
            self.main_game_loop()
        else:
            console.input("Press Enter to continue...")