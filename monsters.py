# monsters.py - Monster creation and management
import random

def create_monster(player_level):
    """Create a monster scaled to player level"""
    
    # List of monster types
    monster_types = [
        {"name": "Goblin", "hp_base": 30, "attack_base": 8},
        {"name": "Orc", "hp_base": 45, "attack_base": 12},
        {"name": "Skeleton", "hp_base": 35, "attack_base": 10},
        {"name": "Wolf", "hp_base": 40, "attack_base": 11},
        {"name": "Bandit", "hp_base": 50, "attack_base": 14},
        {"name": "Troll", "hp_base": 70, "attack_base": 16},
        {"name": "Dark Knight", "hp_base": 65, "attack_base": 18},
        {"name": "Dragon Whelp", "hp_base": 80, "attack_base": 20}
    ]
    
    # Choose random monster type
    monster_type = random.choice(monster_types)
    
    # Scale monster stats based on player level
    level_multiplier = 1 + (player_level - 1) * 0.3
    hp_variance = random.randint(-5, 10)
    attack_variance = random.randint(-2, 3)
    
    scaled_hp = int(monster_type["hp_base"] * level_multiplier) + hp_variance
    scaled_attack = int(monster_type["attack_base"] * level_multiplier) + attack_variance
    
    # Ensure minimum stats
    scaled_hp = max(scaled_hp, 20)
    scaled_attack = max(scaled_attack, 5)
    
    # Create monster dictionary
    monster = {
        "name": monster_type["name"],
        "hp": scaled_hp,
        "max_hp": scaled_hp,
        "attack": scaled_attack,
        "level": player_level
    }
    
    # Add level indicator for stronger monsters
    if player_level > 3:
        monster["name"] = f"Elite {monster['name']}"
    elif player_level > 6:
        monster["name"] = f"Champion {monster['name']}"
    elif player_level > 10:
        monster["name"] = f"Legendary {monster['name']}"
    
    return monster

def get_monster_description(monster):
    """Get a description of the monster"""
    descriptions = {
        "Goblin": "A small, green creature with sharp teeth and beady eyes.",
        "Orc": "A large, brutish humanoid with massive muscles and crude weapons.",
        "Skeleton": "An undead warrior, bones held together by dark magic.",
        "Wolf": "A fierce predator with glowing eyes and sharp fangs.",
        "Bandit": "A human outlaw armed with stolen weapons and armor.",
        "Troll": "A massive creature with incredible regenerative abilities.",
        "Dark Knight": "A fallen warrior clad in cursed black armor.",
        "Dragon Whelp": "A young dragon with fiery breath and sharp claws."
    }
    
    # Extract base name (remove Elite/Champion/Legendary prefix)
    base_name = monster["name"]
    for prefix in ["Legendary ", "Champion ", "Elite "]:
        if base_name.startswith(prefix):
            base_name = base_name[len(prefix):]
            break
    
    return descriptions.get(base_name, "A mysterious creature of unknown origin.")