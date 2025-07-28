# player.py - Player character management
from utils import get_user_choice, clear_screen

def create_player():
    """Create a new player character"""
    clear_screen()
    print("=" * 40)
    print("      CHARACTER CREATION")
    print("=" * 40)
    
    # Get player name
    while True:
        name = input("Enter your character's name: ").strip()
        if name:
            break
        print("Please enter a valid name!")
    
    # Choose character class
    print("\nChoose your class:")
    print("1. Warrior - High health and attack")
    print("2. Mage - Moderate stats, powerful special attack")
    print("3. Rogue - Balanced stats, quick special cooldown")
    
    class_choice = get_user_choice("Enter your choice (1-3): ", ["1", "2", "3"])
    
    # Set base stats based on class
    if class_choice == "1":
        player_class = "Warrior"
        base_hp = 100
        base_attack = 20
        special_damage = 35
    elif class_choice == "2":
        player_class = "Mage"
        base_hp = 80
        base_attack = 15
        special_damage = 50
    else:  # Rogue
        player_class = "Rogue"
        base_hp = 90
        base_attack = 18
        special_damage = 40
    
    # Set mana based on class
    if player_class == "Mage":
        base_mana = 60
    elif player_class == "Warrior":
        base_mana = 30
    else:  # Rogue
        base_mana = 45
    
    # Create player dictionary
    player = {
        "name": name,
        "class": player_class,
        "level": 1,
        "hp": base_hp,
        "max_hp": base_hp,
        "mana": base_mana,
        "max_mana": base_mana,
        "attack": base_attack,
        "special_damage": special_damage,
        "special_cooldown": 0,
        "special_max_cooldown": 4 if player_class == "Rogue" else 5,
        "special_mana_cost": 20 if player_class == "Mage" else 15,
        "xp": 0,
        "xp_to_next": 50,
        "gold": 50,
        "inventory": {
            "health_potions": 2,
            "mana_potions": 1
        }
    }
    
    return player

def level_up_player(player):
    """Level up the player character"""
    print("\n" + "=" * 30)
    print("       LEVEL UP!")
    print("=" * 30)
    
    old_level = player["level"]
    player["level"] += 1
    
    # Increase stats
    hp_increase = 15 + (player["level"] * 2)
    mana_increase = 10 + player["level"]
    attack_increase = 3 + player["level"]
    special_increase = 5 + player["level"]
    
    player["max_hp"] += hp_increase
    player["hp"] = player["max_hp"]  # Full heal on level up
    player["max_mana"] += mana_increase
    player["mana"] = player["max_mana"]  # Full mana on level up
    player["attack"] += attack_increase
    player["special_damage"] += special_increase
    
    # Set XP for next level
    player["xp"] = 0
    player["xp_to_next"] = 50 + (player["level"] * 25)
    
    print(f"Level {old_level} -> Level {player['level']}")
    print(f"Max HP increased by {hp_increase}!")
    print(f"Max Mana increased by {mana_increase}!")
    print(f"Attack increased by {attack_increase}!")
    print(f"Special Attack increased by {special_increase}!")
    print("Fully healed and restored mana!")
    
    input("\nPress Enter to continue...")

def use_health_potion(player):
    """Use a healing potion"""
    if player["inventory"]["health_potions"] <= 0:
        print("You don't have any health potions!")
        return
    
    if player["hp"] >= player["max_hp"]:
        print("Your HP is already full!")
        return
    
    # Calculate healing amount
    heal_amount = 30 + (player["level"] * 5)
    old_hp = player["hp"]
    player["hp"] = min(player["max_hp"], player["hp"] + heal_amount)
    actual_heal = player["hp"] - old_hp
    
    player["inventory"]["health_potions"] -= 1
    
    print(f"You used a health potion!")
    print(f"Restored {actual_heal} HP!")
    print(f"Current HP: {player['hp']}/{player['max_hp']}")

def use_mana_potion(player):
    """Use a mana potion"""
    if player["inventory"]["mana_potions"] <= 0:
        print("You don't have any mana potions!")
        return
    
    if player["mana"] >= player["max_mana"]:
        print("Your mana is already full!")
        return
    
    # Calculate mana restoration
    mana_amount = 25 + (player["level"] * 3)
    old_mana = player["mana"]
    player["mana"] = min(player["max_mana"], player["mana"] + mana_amount)
    actual_restore = player["mana"] - old_mana
    
    player["inventory"]["mana_potions"] -= 1
    
    print(f"You used a mana potion!")
    print(f"Restored {actual_restore} mana!")
    print(f"Current Mana: {player['mana']}/{player['max_mana']}")

def use_special_attack(player):
    """Use the player's special attack"""
    if player["special_cooldown"] > 0:
        return False, "Special attack is on cooldown!"
    
    if player["mana"] < player["special_mana_cost"]:
        return False, f"Not enough mana! Need {player['special_mana_cost']}, have {player['mana']}"
    
    # Use mana and set cooldown
    player["mana"] -= player["special_mana_cost"]
    player["special_cooldown"] = player["special_max_cooldown"]
    return True, "Special attack used successfully!"

def reduce_special_cooldown(player):
    """Reduce special attack cooldown by 1"""
    if player["special_cooldown"] > 0:
        player["special_cooldown"] -= 1