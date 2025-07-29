import random
from utils import get_user_choice, clear_screen

class Combat:
    def __init__(self, player, monster):
        self.player = player
        self.monster = monster
        self.turn = 1
    
    def start_battle(self):
        """Main battle function"""
        clear_screen()
        print("=" * 50)
        print("           BATTLE BEGINS!")
        print("=" * 50)
        print(f"A wild {self.monster.name} appears!")
        print(f"{self.monster.name} - HP: {self.monster.hp}, Attack: {self.monster.attack}")
        input("\nPress Enter to start battle...")
        
        # Battle loop
        while self.monster.hp > 0 and self.player.hp > 0:
            clear_screen()
            self._display_battle_status()
            
            # Player turn
            action_result = self._player_turn()
            
            if action_result == "escaped":
                return "escaped"
            elif action_result == "skip_monster_turn":
                self._end_turn()
                continue
            
            # Check if monster is defeated
            if self.monster.hp <= 0:
                print(f"\n{self.monster.name} is defeated!")
                print("Victory!")
                input("\nPress Enter to continue...")
                return "victory"
            
            # Monster turn (only if player didn't use potions)
            if action_result != "skip_monster_turn":
                self._monster_turn()
                
                # Check if player is defeated
                if self.player.hp <= 0:
                    print(f"\nYou have been defeated by {self.monster.name}!")
                    input("Press Enter to continue...")
                    return "defeat"
            
            self._end_turn()
        
        return "ongoing"
    
    def _display_battle_status(self):
        """Display current battle status"""
        print("=" * 50)
        print(f"           BATTLE - Turn {self.turn}")
        print("=" * 50)
        print(f"Enemy: {self.monster.name} - HP: {self.monster.hp}/{self.monster.max_hp}")
        print(f"You: {self.player.name} - HP: {self.player.hp}/{self.player.max_hp} | Mana: {self.player.mana}/{self.player.max_mana}")
        print(f"Gold: {self.player.gold} | Health Potions: {self.player.inventory['health_potions']} | Mana Potions: {self.player.inventory['mana_potions']}")
        print(f"Special Attack Cooldown: {self.player.special_cooldown} turns | Mana Cost: {self.player.special_mana_cost}")
        print()
    
    def _player_turn(self):
        """Handle player's turn"""
        print("Choose your action:")
        print("1. Regular Attack")
        
        # Show special attack status
        special_status = ""
        if self.player.special_cooldown > 0:
            special_status = f" (COOLDOWN: {self.player.special_cooldown} turns)"
        elif self.player.mana < self.player.special_mana_cost:
            special_status = f" (Need {self.player.special_mana_cost} mana, have {self.player.mana})"
        
        print(f"2. Special Attack{special_status}")
        print("3. Use Health Potion")
        print("4. Use Mana Potion") 
        print("5. Try to Run Away")
        
        choice = get_user_choice("Enter your choice (1-5): ", ["1", "2", "3", "4", "5"])
        
        if choice == "1":
            return self._regular_attack()
        elif choice == "2":
            return self._special_attack()
        elif choice == "3":
            self.player.use_health_potion()
            input("\nPress Enter to continue...")
            return "skip_monster_turn"
        elif choice == "4":
            self.player.use_mana_potion()
            input("\nPress Enter to continue...")
            return "skip_monster_turn"
        elif choice == "5":
            return self._try_escape()
    
    def _regular_attack(self):
        """Perform regular attack"""
        damage_variance = random.randint(-3, 3)
        player_damage = self.player.attack + damage_variance
        
        print(f"\nYou attack {self.monster.name} for {player_damage} damage!")
        self.monster.hp -= player_damage
        input("\nPress Enter to continue...")
        return "continue"
    
    def _special_attack(self):
        """Perform special attack"""
        success, message = self.player.use_special_attack()
        if success:
            damage_variance = random.randint(-5, 5)
            player_damage = self.player.special_damage + damage_variance
            
            if self.player.player_class == "Warrior":
                print(f"\nYou use MIGHTY SLASH on {self.monster.name}!")
            elif self.player.player_class == "Mage":
                print(f"\nYou cast FIREBALL on {self.monster.name}!")
            else:  # Rogue
                print(f"\nYou use SNEAK ATTACK on {self.monster.name}!")
            
            print(f"Critical hit for {player_damage} damage!")
            print(f"Mana: {self.player.mana}/{self.player.max_mana}")
            
            self.monster.hp -= player_damage
            input("\nPress Enter to continue...")
            return "continue"
        else:
            print(f"\n{message}")
            input("Press Enter to continue...")
            return "retry"
    
    def _try_escape(self):
        """Try to escape from battle"""
        escape_chance = random.randint(1, 100)
        if escape_chance <= 30:  # 30% chance to escape
            print(f"\nYou successfully escaped from {self.monster.name}!")
            input("Press Enter to continue...")
            return "escaped"
        else:
            print(f"\nYou couldn't escape from {self.monster.name}!")
            input("Press Enter to continue...")
            return "continue"
    
    def _monster_turn(self):
        """Handle monster's turn"""
        monster_damage_variance = random.randint(-2, 2)
        monster_damage = self.monster.attack + monster_damage_variance
        
        print(f"\n{self.monster.name} attacks you for {monster_damage} damage!")
        self.player.hp -= monster_damage
        
        input("Press Enter to continue...")
    
    def _end_turn(self):
        """End the current turn"""
        self.player.reduce_special_cooldown()
        self.turn += 1