import random
from abc import ABC, abstractmethod
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from utils import get_user_choice

console = Console()

class BattleAction(ABC):
    """Abstract base class for battle actions"""
    
    @abstractmethod
    def execute(self, player, monster):
        """Execute the battle action"""
        pass
    
    @abstractmethod
    def can_execute(self, player):
        """Check if the action can be executed"""
        pass
    
    @property
    @abstractmethod
    def action_name(self):
        """Name of the action"""
        pass

class RegularAttack(BattleAction):
    @property
    def action_name(self):
        return "Regular Attack"
    
    def can_execute(self, player):
        return True
    
    def execute(self, player, monster):
        damage_variance = random.randint(-3, 3)
        player_damage = player.attack + damage_variance
        
        console.print(f"\n⚔️  You attack {monster.name} for [bold red]{player_damage}[/bold red] damage!", style="bold green")
        monster.take_damage(player_damage)
        return "continue"

class SpecialAttack(BattleAction):
    @property
    def action_name(self):
        return "Special Attack"
    
    def can_execute(self, player):
        return player.special_cooldown == 0 and player.mana >= player.special_mana_cost
    
    def execute(self, player, monster):
        success, message = player.use_special_attack()
        if success:
            damage_variance = random.randint(-5, 5)
            player_damage = player.special_damage + damage_variance
            
            if player.player_class == "Warrior":
                console.print(f"\n💥 You use [bold yellow]MIGHTY SLASH[/bold yellow] on {monster.name}!", style="bold red")
            elif player.player_class == "Mage":
                console.print(f"\n🔥 You cast [bold yellow]FIREBALL[/bold yellow] on {monster.name}!", style="bold red")
            else:  # Rogue
                console.print(f"\n🗡️  You use [bold yellow]SNEAK ATTACK[/bold yellow] on {monster.name}!", style="bold red")
            
            console.print(f"Critical hit for [bold red]{player_damage}[/bold red] damage!", style="bold yellow")
            console.print(f"Mana: [cyan]{player.mana}/{player.max_mana}[/cyan]")
            
            monster.take_damage(player_damage)
            return "continue"
        else:
            console.print(f"\n❌ {message}", style="bold red")
            return "retry"

class UseHealthPotion(BattleAction):
    @property
    def action_name(self):
        return "Use Health Potion"
    
    def can_execute(self, player):
        return player.inventory["health_potions"] > 0 and player.hp < player.max_hp
    
    def execute(self, player, monster):
        player.use_health_potion()
        return "skip_monster_turn"

class UseManaPotion(BattleAction):
    @property
    def action_name(self):
        return "Use Mana Potion"
    
    def can_execute(self, player):
        return player.inventory["mana_potions"] > 0 and player.mana < player.max_mana
    
    def execute(self, player, monster):
        player.use_mana_potion()
        return "skip_monster_turn"

class TryEscape(BattleAction):
    @property
    def action_name(self):
        return "Try to Run Away"
    
    def can_execute(self, player):
        return True
    
    def execute(self, player, monster):
        escape_chance = random.randint(1, 100)
        if escape_chance <= 30:  # 30% chance to escape
            console.print(f"\n🏃 You successfully escaped from {monster.name}!", style="bold green")
            return "escaped"
        else:
            console.print(f"\n❌ You couldn't escape from {monster.name}!", style="bold red")
            return "continue"

class Combat:
    def __init__(self, player, monster):
        self._player = player
        self._monster = monster
        self._turn = 1
        
        # Initialize battle actions
        self.actions = {
            "1": RegularAttack(),
            "2": SpecialAttack(),
            "3": UseHealthPotion(),
            "4": UseManaPotion(),
            "5": TryEscape()
        }
    
    @property
    def player(self):
        return self._player
    
    @property
    def monster(self):
        return self._monster
    
    @property
    def turn(self):
        return self._turn
    
    @turn.setter
    def turn(self, value):
        if value < 1:
            raise ValueError("Turn number must be positive")
        self._turn = value
    
    def start_battle(self):
        """Main battle function"""
        console.clear()
        
        # Create battle start panel
        battle_panel = Panel.fit(
            f"🗡️  BATTLE BEGINS! 🗡️\n\nA wild [bold red]{self.monster.name}[/bold red] appears!\n"
            f"HP: [red]{self.monster.hp}[/red] | Attack: [yellow]{self.monster.attack}[/yellow]",
            title="⚔️ COMBAT ⚔️",
            border_style="red"
        )
        console.print(battle_panel)
        console.input("\nPress Enter to start battle...")
        
        # Battle loop
        while self.monster.is_alive and self.player.is_alive:
            console.clear()
            self._display_battle_status()
            
            # Player turn
            action_result = self._player_turn()
            
            if action_result == "escaped":
                return "escaped"
            elif action_result == "skip_monster_turn":
                self._end_turn()
                continue
            
            # Check if monster is defeated
            if not self.monster.is_alive:
                console.print(f"\n🏆 {self.monster.name} is defeated!", style="bold green")
                console.print("🎉 Victory!", style="bold yellow")
                console.input("\nPress Enter to continue...")
                return "victory"
            
            # Monster turn (only if player didn't use potions)
            if action_result != "skip_monster_turn":
                self._monster_turn()
                
                # Check if player is defeated
                if not self.player.is_alive:
                    console.print(f"\n💀 You have been defeated by {self.monster.name}!", style="bold red")
                    console.input("Press Enter to continue...")
                    return "defeat"
            
            self._end_turn()
        
        return "ongoing"
    
    def _display_battle_status(self):
        """Display current battle status with Rich formatting"""
        # Create battle status table
        table = Table(title=f"⚔️ BATTLE - Turn {self.turn} ⚔️")
        table.add_column("Combatant", style="cyan", no_wrap=True)
        table.add_column("HP", style="magenta")
        table.add_column("Mana", style="blue")
        table.add_column("Attack", style="red")
        table.add_column("Status", style="green")
        
        # Monster row
        monster_hp_bar = self._create_hp_bar(self.monster.hp, self.monster.max_hp)
        table.add_row(
            f"👹 {self.monster.name}",
            f"{monster_hp_bar} {self.monster.hp}/{self.monster.max_hp}",
            "N/A",
            str(self.monster.attack),
            "🔥 Hostile"
        )
        
        # Player row
        player_hp_bar = self._create_hp_bar(self.player.hp, self.player.max_hp)
        player_mana_bar = self._create_mana_bar(self.player.mana, self.player.max_mana)
        cooldown_status = f"⏰ {self.player.special_cooldown}" if self.player.special_cooldown > 0 else "✅ Ready"
        table.add_row(
            f"🧙 {self.player.name}",
            f"{player_hp_bar} {self.player.hp}/{self.player.max_hp}",
            f"{player_mana_bar} {self.player.mana}/{self.player.max_mana}",
            str(self.player.attack),
            cooldown_status
        )
        
        console.print(table)
        
        # Inventory info
        inventory_text = Text()
        inventory_text.append("💰 Gold: ", style="yellow")
        inventory_text.append(str(self.player.gold), style="bold yellow")
        inventory_text.append(" | 🧪 Health Potions: ", style="red")
        inventory_text.append(str(self.player.inventory['health_potions']), style="bold red")
        inventory_text.append(" | 🔮 Mana Potions: ", style="blue")
        inventory_text.append(str(self.player.inventory['mana_potions']), style="bold blue")
        
        console.print(Panel(inventory_text, title="💼 Inventory", border_style="green"))
    
    def _create_hp_bar(self, current, maximum):
        """Create a visual HP bar"""
        if maximum <= 0:
            return "[red]░░░░░░░░░░[/red]"
        
        percentage = current / maximum
        filled_blocks = int(percentage * 10)
        
        if percentage > 0.6:
            color = "green"
        elif percentage > 0.3:
            color = "yellow"
        else:
            color = "red"
        
        filled = "█" * filled_blocks
        empty = "░" * (10 - filled_blocks)
        return f"[{color}]{filled}[/{color}][dim]{empty}[/dim]"
    
    def _create_mana_bar(self, current, maximum):
        """Create a visual mana bar"""
        if maximum <= 0:
            return "[blue]░░░░░░░░░░[/blue]"
        
        percentage = current / maximum
        filled_blocks = int(percentage * 10)
        
        filled = "█" * filled_blocks
        empty = "░" * (10 - filled_blocks)
        return f"[blue]{filled}[/blue][dim]{empty}[/dim]"
    
    def _player_turn(self):
        """Handle player's turn"""
        console.print("\n🎯 Choose your action:", style="bold cyan")
        
        # Display available actions
        for key, action in self.actions.items():
            status = ""
            if not action.can_execute(self.player):
                if isinstance(action, SpecialAttack):
                    if self.player.special_cooldown > 0:
                        status = f" [dim](COOLDOWN: {self.player.special_cooldown} turns)[/dim]"
                    elif self.player.mana < self.player.special_mana_cost:
                        status = f" [dim](Need {self.player.special_mana_cost} mana, have {self.player.mana})[/dim]"
                elif isinstance(action, UseHealthPotion):
                    if self.player.inventory["health_potions"] <= 0:
                        status = " [dim](No potions)[/dim]"
                    elif self.player.hp >= self.player.max_hp:
                        status = " [dim](HP full)[/dim]"
                elif isinstance(action, UseManaPotion):
                    if self.player.inventory["mana_potions"] <= 0:
                        status = " [dim](No potions)[/dim]"
                    elif self.player.mana >= self.player.max_mana:
                        status = " [dim](Mana full)[/dim]"
            
            console.print(f"{key}. {action.action_name}{status}")
        
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5"], default="1")
        
        action = self.actions[choice]
        if action.can_execute(self.player):
            result = action.execute(self.player, self.monster)
            if result != "retry":
                console.input("\nPress Enter to continue...")
            return result
        else:
            console.print("❌ Cannot perform that action right now!", style="bold red")
            console.input("\nPress Enter to continue...")
            return "retry"
    
    def _monster_turn(self):
        """Handle monster's turn"""
        monster_damage_variance = random.randint(-2, 2)
        monster_damage = self.monster.attack + monster_damage_variance
        
        console.print(f"\n👹 {self.monster.name} attacks you for [bold red]{monster_damage}[/bold red] damage!", style="bold red")
        self.player.take_damage(monster_damage)
        
        console.input("Press Enter to continue...")
    
    def _end_turn(self):
        """End the current turn"""
        self.player.reduce_special_cooldown()
        self.turn += 1