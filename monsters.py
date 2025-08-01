import random
from abc import ABC, abstractmethod
from rich.console import Console
from rich.text import Text

console = Console()

class Character(ABC):
    """Abstract base class for all characters (shared with Player)"""
    
    def __init__(self, name="", level=1):
        self._name = name
        self._level = level
        self._hp = 0
        self._max_hp = 0
        self._attack = 0
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = value.strip()
    
    @property
    def level(self):
        return self._level
    
    @level.setter
    def level(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("Level must be a positive integer")
        self._level = value
    
    @property
    def hp(self):
        return self._hp
    
    @hp.setter
    def hp(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("HP must be a non-negative integer")
        self._hp = min(value, self._max_hp)
    
    @property
    def max_hp(self):
        return self._max_hp
    
    @max_hp.setter
    def max_hp(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("Max HP must be a positive integer")
        self._max_hp = value
    
    @property
    def attack(self):
        return self._attack
    
    @attack.setter
    def attack(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Attack must be a non-negative integer")
        self._attack = value
    
    @property
    def is_alive(self):
        return self._hp > 0
    
    @property
    def hp_percentage(self):
        if self._max_hp <= 0:
            return 0
        return (self._hp / self._max_hp) * 100
    
    @abstractmethod
    def take_damage(self, damage):
        """Take damage from an attack"""
        pass
    
    @abstractmethod
    def get_status_display(self):
        """Get formatted status display"""
        pass

class MonsterType(ABC):
    """Abstract base class for different monster types"""
    
    @property
    @abstractmethod
    def base_name(self):
        """Base name of the monster type"""
        pass
    
    @property
    @abstractmethod
    def base_hp(self):
        """Base HP of the monster type"""
        pass
    
    @property
    @abstractmethod
    def base_attack(self):
        """Base attack of the monster type"""
        pass
    
    @property
    @abstractmethod
    def description(self):
        """Description of the monster type"""
        pass
    
    @property
    @abstractmethod
    def emoji(self):
        """Emoji representation of the monster"""
        pass
    
    @property
    def special_ability(self):
        """Special ability of the monster (if any)"""
        return None
    
    @property
    def special_ability_chance(self):
        """Chance to use special ability (0.0 to 1.0)"""
        return 0.0
    
    @property
    def flavor_texts(self):
        """List of flavor texts for variety"""
        return [self.description]
    
    @property
    def can_be_boss(self):
        """Whether this monster type can spawn as a boss"""
        return True

class Goblin(MonsterType):
    @property
    def base_name(self):
        return "Goblin"
    
    @property
    def base_hp(self):
        return 30
    
    @property
    def base_attack(self):
        return 8
    
    @property
    def description(self):
        return "A small, green creature with sharp teeth and beady eyes."
    
    @property
    def emoji(self):
        return "👺"
    
    @property
    def special_ability(self):
        return "sneak_attack"
    
    @property
    def special_ability_chance(self):
        return 0.25
    
    @property
    def flavor_texts(self):
        return [
            "A small, green creature with sharp teeth and beady eyes.",
            "This sneaky goblin clutches a rusty dagger, eyeing your gold pouch.",
            "A mischievous goblin that seems to have escaped from a nearby cave.",
            "This goblin's eyes gleam with cunning intelligence and malice."
        ]

class Orc(MonsterType):
    @property
    def base_name(self):
        return "Orc"
    
    @property
    def base_hp(self):
        return 45
    
    @property
    def base_attack(self):
        return 12
    
    @property
    def description(self):
        return "A large, brutish humanoid with massive muscles and crude weapons."
    
    @property
    def emoji(self):
        return "👹"
    
    @property
    def special_ability(self):
        return "rage"
    
    @property
    def special_ability_chance(self):
        return 0.20
    
    @property
    def flavor_texts(self):
        return [
            "A large, brutish humanoid with massive muscles and crude weapons.",
            "This battle-scarred orc wields a massive club, ready for violence.",
            "A fierce orc warrior with tusks protruding from its lower jaw.",
            "The orc's war paint indicates it's a veteran of many battles."
        ]

class Skeleton(MonsterType):
    @property
    def base_name(self):
        return "Skeleton"
    
    @property
    def base_hp(self):
        return 35
    
    @property
    def base_attack(self):
        return 10
    
    @property
    def description(self):
        return "An undead warrior, bones held together by dark magic."
    
    @property
    def emoji(self):
        return "💀"
    
    @property
    def special_ability(self):
        return "bone_armor"
    
    @property
    def special_ability_chance(self):
        return 0.15
    
    @property
    def flavor_texts(self):
        return [
            "An undead warrior, bones held together by dark magic.",
            "Ancient bones rattle as this skeleton prepares for battle.",
            "This skeletal warrior still clutches the sword it died with.",
            "Dark energy flows between the gaps in its ribcage."
        ]

class Wolf(MonsterType):
    @property
    def base_name(self):
        return "Wolf"
    
    @property
    def base_hp(self):
        return 40
    
    @property
    def base_attack(self):
        return 11
    
    @property
    def description(self):
        return "A fierce predator with glowing eyes and sharp fangs."
    
    @property
    def emoji(self):
        return "🐺"
    
    @property
    def special_ability(self):
        return "pack_howl"
    
    @property
    def special_ability_chance(self):
        return 0.18
    
    @property
    def flavor_texts(self):
        return [
            "A fierce predator with glowing eyes and sharp fangs.",
            "This alpha wolf's scarred muzzle tells of countless hunts.",
            "A massive dire wolf with silver-tipped fur and intelligent eyes.",
            "The wolf's low growl sends chills down your spine."
        ]

class Bandit(MonsterType):
    @property
    def base_name(self):
        return "Bandit"
    
    @property
    def base_hp(self):
        return 50
    
    @property
    def base_attack(self):
        return 14
    
    @property
    def description(self):
        return "A human outlaw armed with stolen weapons and armor."
    
    @property
    def emoji(self):
        return "🏴‍☠️"
    
    @property
    def special_ability(self):
        return "dirty_fighting"
    
    @property
    def special_ability_chance(self):
        return 0.22
    
    @property
    def flavor_texts(self):
        return [
            "A human outlaw armed with stolen weapons and armor.",
            "This highway robber demands your coin with blade drawn.",
            "A desperate bandit with nothing left to lose but everything to gain.",
            "The bandit's eyes dart nervously, planning an escape route."
        ]

class Troll(MonsterType):
    @property
    def base_name(self):
        return "Troll"
    
    @property
    def base_hp(self):
        return 70
    
    @property
    def base_attack(self):
        return 16
    
    @property
    def description(self):
        return "A massive creature with incredible regenerative abilities."
    
    @property
    def emoji(self):
        return "🧌"
    
    @property
    def special_ability(self):
        return "regeneration"
    
    @property
    def special_ability_chance(self):
        return 0.30
    
    @property
    def flavor_texts(self):
        return [
            "A massive creature with incredible regenerative abilities.",
            "This ancient troll's wounds heal before your very eyes.",
            "Moss and fungus grow on this elder troll's rocky hide.",
            "The troll's primitive intelligence gleams with predatory cunning."
        ]

class DarkKnight(MonsterType):
    @property
    def base_name(self):
        return "Dark Knight"
    
    @property
    def base_hp(self):
        return 65
    
    @property
    def base_attack(self):
        return 18
    
    @property
    def description(self):
        return "A fallen warrior clad in cursed black armor."
    
    @property
    def emoji(self):
        return "⚔️"
    
    @property
    def special_ability(self):
        return "dark_strike"
    
    @property
    def special_ability_chance(self):
        return 0.25
    
    @property
    def flavor_texts(self):
        return [
            "A fallen warrior clad in cursed black armor.",
            "Once a noble paladin, now corrupted by dark magic.",
            "The knight's armor bears the scars of a thousand battles.",
            "Unholy power radiates from this corrupted champion."
        ]

class DragonWhelp(MonsterType):
    @property
    def base_name(self):
        return "Dragon Whelp"
    
    @property
    def base_hp(self):
        return 80
    
    @property
    def base_attack(self):
        return 20
    
    @property
    def description(self):
        return "A young dragon with fiery breath and sharp claws."
    
    @property
    def emoji(self):
        return "🐉"
    
    @property
    def special_ability(self):
        return "fire_breath"
    
    @property
    def special_ability_chance(self):
        return 0.35
    
    @property
    def flavor_texts(self):
        return [
            "A young dragon with fiery breath and sharp claws.",
            "This juvenile dragon already shows the pride of its ancient bloodline.",
            "Scales shimmer with inner fire as the dragon prepares to strike.",
            "Though young, this dragon's intelligence rivals that of ancient wizards."
        ]

# Boss-only monster types
class AncientLich(MonsterType):
    @property
    def base_name(self):
        return "Ancient Lich"
    
    @property
    def base_hp(self):
        return 120
    
    @property
    def base_attack(self):
        return 25
    
    @property
    def description(self):
        return "An undead sorcerer of immense power, wreathed in necrotic energy."
    
    @property
    def emoji(self):
        return "🧙‍♂️"
    
    @property
    def special_ability(self):
        return "death_curse"
    
    @property
    def special_ability_chance(self):
        return 0.40
    
    @property
    def can_be_boss(self):
        return True
    
    @property
    def flavor_texts(self):
        return [
            "An undead sorcerer of immense power, wreathed in necrotic energy.",
            "This ancient wizard cheated death through forbidden magic.",
            "Centuries of accumulated knowledge gleam in its hollow eye sockets.",
            "The very air around the lich crackles with dark magical energy."
        ]

class CrimsonDragon(MonsterType):
    @property
    def base_name(self):
        return "Crimson Dragon"
    
    @property
    def base_hp(self):
        return 150
    
    @property
    def base_attack(self):
        return 30
    
    @property
    def description(self):
        return "An adult dragon with scales like molten rubies and devastating flame."
    
    @property
    def emoji(self):
        return "🔥"
    
    @property
    def special_ability(self):
        return "inferno_breath"
    
    @property
    def special_ability_chance(self):
        return 0.50
    
    @property
    def can_be_boss(self):
        return True
    
    @property
    def flavor_texts(self):
        return [
            "An adult dragon with scales like molten rubies and devastating flame.",
            "This legendary dragon has terrorized kingdoms for centuries.",
            "The dragon's treasure hoard is said to rival that of kings.",
            "Ancient scars on its hide tell tales of epic battles with heroes."
        ]

class VoidWraith(MonsterType):
    @property
    def base_name(self):
        return "Void Wraith"
    
    @property
    def base_hp(self):
        return 100
    
    @property
    def base_attack(self):
        return 28
    
    @property
    def description(self):
        return "A being of pure shadow that feeds on life force itself."
    
    @property
    def emoji(self):
        return "👻"
    
    @property
    def special_ability(self):
        return "life_drain"
    
    @property
    def special_ability_chance(self):
        return 0.45
    
    @property
    def can_be_boss(self):
        return True
    
    @property
    def flavor_texts(self):
        return [
            "A being of pure shadow that feeds on life force itself.",
            "This wraith exists between the realms of life and death.",
            "The temperature drops noticeably in the presence of this entity.",
            "Reality seems to bend and warp around the wraith's form."
        ]

class Monster(Character):
    def __init__(self, name, hp, attack, level=1, monster_type=None, rarity="common", is_boss=False):
        super().__init__(name, level)
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self._monster_type = monster_type
        self._rarity = rarity
        self._is_boss = is_boss
        self._status_effects = {}  # For tracking poison, stun, etc.
        self._special_cooldown = 0
    
    @property
    def monster_type(self):
        return self._monster_type
    
    @property
    def rarity(self):
        return self._rarity
    
    @property
    def is_boss(self):
        return self._is_boss
    
    @property
    def status_effects(self):
        return self._status_effects.copy()
    
    @property
    def threat_level(self):
        """Calculate threat level based on stats and rarity"""
        base_power = self.max_hp + (self.attack * 5)
        
        # Adjust for rarity
        rarity_multiplier = {
            "common": 1.0,
            "uncommon": 1.3,
            "rare": 1.6,
            "legendary": 2.0
        }
        
        total_power = base_power * rarity_multiplier.get(self._rarity, 1.0)
        
        if self._is_boss:
            total_power *= 1.5
        
        if total_power < 100:
            return "Low"
        elif total_power < 200:
            return "Medium"
        elif total_power < 350:
            return "High"
        elif total_power < 500:
            return "Extreme"
        else:
            return "Legendary"
    
    @property
    def threat_color(self):
        """Get color based on threat level"""
        threat_colors = {
            "Low": "green",
            "Medium": "yellow", 
            "High": "red",
            "Extreme": "bright_red",
            "Legendary": "magenta"
        }
        return threat_colors.get(self.threat_level, "white")
    
    @property
    def rarity_color(self):
        """Get color based on rarity"""
        rarity_colors = {
            "common": "white",
            "uncommon": "green",
            "rare": "blue",
            "legendary": "gold1"
        }
        return rarity_colors.get(self._rarity, "white")
    
    def add_status_effect(self, effect, duration):
        """Add a status effect"""
        self._status_effects[effect] = duration
    
    def remove_status_effect(self, effect):
        """Remove a status effect"""
        if effect in self._status_effects:
            del self._status_effects[effect]
    
    def process_status_effects(self):
        """Process all active status effects"""
        effects_to_remove = []
        
        for effect, duration in self._status_effects.items():
            if effect == "poison":
                poison_damage = max(1, self.max_hp // 10)
                console.print(f"🟢 {self.name} takes {poison_damage} poison damage!", style="bold green")
                self.take_damage(poison_damage)
            elif effect == "regeneration":
                heal_amount = max(1, self.max_hp // 8)
                old_hp = self.hp
                self.hp = min(self.max_hp, self.hp + heal_amount)
                actual_heal = self.hp - old_hp
                if actual_heal > 0:
                    console.print(f"🟡 {self.name} regenerates {actual_heal} HP!", style="bold yellow")
            
            # Reduce duration
            self._status_effects[effect] -= 1
            if self._status_effects[effect] <= 0:
                effects_to_remove.append(effect)
        
        # Remove expired effects
        for effect in effects_to_remove:
            self.remove_status_effect(effect)
            if effect == "stun":
                console.print(f"⚡ {self.name} recovers from being stunned!", style="bold cyan")
    
    def can_act(self):
        """Check if monster can act (not stunned)"""
        return "stun" not in self._status_effects
    
    def use_special_ability(self, player):
        """Use the monster's special ability"""
        if not self._monster_type or not self._monster_type.special_ability:
            return False
        
        if self._special_cooldown > 0:
            return False
        
        if random.random() > self._monster_type.special_ability_chance:
            return False
        
        ability = self._monster_type.special_ability
        
        if ability == "sneak_attack":
            bonus_damage = random.randint(5, 10)
            console.print(f"💨 {self.name} strikes from the shadows!", style="bold yellow")
            console.print(f"🗡️ Sneak attack deals {bonus_damage} extra damage!", style="bold red")
            player.take_damage(bonus_damage)
            self._special_cooldown = 3
            
        elif ability == "rage":
            self.attack += 5
            console.print(f"😡 {self.name} enters a berserker rage!", style="bold red")
            console.print(f"⚔️ Attack increased by 5!", style="bold yellow")
            self._special_cooldown = 4
            
        elif ability == "bone_armor":
            console.print(f"🦴 {self.name}'s bones rattle and strengthen!", style="bold white")
            console.print(f"🛡️ Next attack will deal reduced damage!", style="bold blue")
            # This would need to be handled in combat system
            self._special_cooldown = 5
            
        elif ability == "pack_howl":
            console.print(f"🐺 {self.name} lets out a bone-chilling howl!", style="bold cyan")
            console.print(f"😱 You feel intimidated! Next attack may miss!", style="bold yellow")
            self._special_cooldown = 4
            
        elif ability == "dirty_fighting":
            if random.random() < 0.5:
                console.print(f"💥 {self.name} throws dirt in your eyes!", style="bold brown")
                console.print(f"😵 You are briefly stunned!", style="bold red")
                # Player stun would need to be handled in combat system
            else:
                console.print(f"🗡️ {self.name} aims for a weak spot!", style="bold red")
                critical_damage = random.randint(8, 15)
                player.take_damage(critical_damage)
            self._special_cooldown = 3
            
        elif ability == "regeneration":
            self.add_status_effect("regeneration", 3)
            console.print(f"🟢 {self.name} begins regenerating!", style="bold green")
            self._special_cooldown = 6
            
        elif ability == "dark_strike":
            dark_damage = random.randint(10, 18)
            console.print(f"⚫ {self.name} channels dark energy into its blade!", style="bold magenta")
            console.print(f"💀 Dark strike deals {dark_damage} unholy damage!", style="bold red")
            player.take_damage(dark_damage)
            self._special_cooldown = 5
            
        elif ability == "fire_breath":
            fire_damage = random.randint(12, 20)
            console.print(f"🔥 {self.name} breathes a cone of flames!", style="bold red")
            console.print(f"🌋 Fire breath deals {fire_damage} fire damage!", style="bold orange1")
            player.take_damage(fire_damage)
            self._special_cooldown = 4
            
        elif ability == "death_curse":
            curse_damage = random.randint(15, 25)
            console.print(f"💜 {self.name} weaves a deadly curse!", style="bold magenta")
            console.print(f"☠️ Death curse deals {curse_damage} necrotic damage!", style="bold red")
            player.take_damage(curse_damage)
            # Add poison effect
            console.print(f"🟢 You feel the curse lingering in your veins!", style="bold green")
            self._special_cooldown = 7
            
        elif ability == "inferno_breath":
            inferno_damage = random.randint(20, 35)
            console.print(f"🔥 {self.name} unleashes a devastating inferno!", style="bold bright_red")
            console.print(f"🌋 Inferno breath deals {inferno_damage} massive fire damage!", style="bold red")
            player.take_damage(inferno_damage)
            self._special_cooldown = 6
            
        elif ability == "life_drain":
            drain_damage = random.randint(12, 22)
            console.print(f"👻 {self.name} drains your life force!", style="bold blue")
            console.print(f"💀 Life drain deals {drain_damage} damage!", style="bold red")
            player.take_damage(drain_damage)
            # Heal the wraith
            self.hp = min(self.max_hp, self.hp + drain_damage // 2)
            console.print(f"💚 {self.name} recovers {drain_damage // 2} HP!", style="bold green")
            self._special_cooldown = 5
        
        return True
    
    def reduce_special_cooldown(self):
        """Reduce special ability cooldown"""
        if self._special_cooldown > 0:
            self._special_cooldown -= 1
    
    def take_damage(self, damage):
        """Take damage from an attack"""
        if damage < 0:
            raise ValueError("Damage cannot be negative")
        
        old_hp = self.hp
        self.hp = max(0, self.hp - damage)
        actual_damage = old_hp - self.hp
        
        if actual_damage > 0:
            console.print(f"💥 {self.name} takes {actual_damage} damage!", style=f"bold {self.threat_color}")
        
        if not self.is_alive:
            console.print(f"💀 {self.name} has been defeated!", style="bold green")
        
        return actual_damage
    
    def get_status_display(self):
        """Get formatted status display"""
        status_text = Text()
        emoji = self._monster_type.emoji if self._monster_type else "👾"
        
        # Name with rarity coloring
        status_text.append(f"{emoji} ", style="white")
        status_text.append(f"{self.name}", style=f"bold {self.rarity_color}")
        
        if self._is_boss:
            status_text.append(" 👑", style="gold1")
        
        status_text.append(f"\nLevel: {self.level} | ", style="cyan")
        status_text.append(f"HP: {self.hp}/{self.max_hp} | ", style="red")
        status_text.append(f"Attack: {self.attack}\n", style="yellow")
        status_text.append(f"Rarity: {self._rarity.title()}", style=self.rarity_color)
        status_text.append(f" | Threat: {self.threat_level}", style=self.threat_color)
        
        # Show active status effects
        if self._status_effects:
            status_text.append(f"\nEffects: ", style="magenta")
            effects = []
            for effect, duration in self._status_effects.items():
                effects.append(f"{effect.title()}({duration})")
            status_text.append(", ".join(effects), style="yellow")
        
        return status_text
    
    @classmethod
    def create_monster(cls, player_level):
        """Create a monster scaled to player level"""
        # Determine if boss spawn (5% chance at level 5+, increases with level)
        boss_chance = max(0, (player_level - 4) * 0.02)
        is_boss = random.random() < boss_chance and player_level >= 5
        
        if is_boss:
            # Boss monsters
            boss_types = [AncientLich(), CrimsonDragon(), VoidWraith()]
            monster_type = random.choice(boss_types)
        else:
            # Regular monsters
            monster_types = [
                Goblin(), Orc(), Skeleton(), Wolf(),
                Bandit(), Troll(), DarkKnight(), DragonWhelp()
            ]
            monster_type = random.choice(monster_types)
        
        # Determine rarity
        if is_boss:
            rarity = "legendary"
        else:
            rarity_roll = random.random()
            if rarity_roll < 0.70:
                rarity = "common"
            elif rarity_roll < 0.90:
                rarity = "uncommon"
            elif rarity_roll < 0.98:
                rarity = "rare"
            else:
                rarity = "legendary"
        
        # Scale monster stats based on player level and rarity
        level_multiplier = 1 + (player_level - 1) * 0.3
        
        # Rarity multipliers
        rarity_multipliers = {
            "common": 1.0,
            "uncommon": 1.2,
            "rare": 1.4,
            "legendary": 1.7
        }
        
        total_multiplier = level_multiplier * rarity_multipliers[rarity]
        
        if is_boss:
            total_multiplier *= 1.5
        
        hp_variance = random.randint(-5, 10)
        attack_variance = random.randint(-2, 3)
        
        scaled_hp = int(monster_type.base_hp * total_multiplier) + hp_variance
        scaled_attack = int(monster_type.base_attack * total_multiplier) + attack_variance
        
        # Ensure minimum stats
        scaled_hp = max(scaled_hp, 20)
        scaled_attack = max(scaled_attack, 5)
        
        # Create name with modifiers
        name = monster_type.base_name
        
        if is_boss:
            boss_titles = ["Overlord", "Destroyer", "Terror", "Nightmare", "Doom Bringer"]
            name = f"{random.choice(boss_titles)} {name}"
        elif rarity == "legendary":
            name = f"Legendary {name}"
        elif rarity == "rare":
            name = f"Ancient {name}"
        elif rarity == "uncommon":
            name = f"Elite {name}"
        
        # Additional level-based titles for high-level monsters
        if player_level > 15:
            name = f"Apex {name}"
        elif player_level > 10:
            name = f"Champion {name}"
        elif player_level > 6:
            name = f"Veteran {name}"
        
        return cls(name, scaled_hp, scaled_attack, player_level, monster_type, rarity, is_boss)
    
    def get_description(self):
        """Get a description of the monster with variety"""
        if self._monster_type and self._monster_type.flavor_texts:
            base_description = random.choice(self._monster_type.flavor_texts)
            
            # Add rarity-based flavor
            if self._rarity == "uncommon":
                base_description += " This specimen seems unusually strong."
            elif self._rarity == "rare":
                base_description += " An aura of power surrounds this rare creature."
            elif self._rarity == "legendary":
                base_description += " This legendary being radiates immense power."
            
            if self._is_boss:
                base_description += " Its presence fills you with dread."
            
            return base_description
        return "A mysterious creature of unknown origin."
    
    def get_combat_message(self, action="appears"):
        """Get a formatted combat message"""
        emoji = self._monster_type.emoji if self._monster_type else "👾"
        
        rarity_prefix = ""
        if self._is_boss:
            rarity_prefix = "💀 BOSS: "
        elif self._rarity == "legendary":
            rarity_prefix = "✨ LEGENDARY: "
        elif self._rarity == "rare":
            rarity_prefix = "💎 RARE: "
        elif self._rarity == "uncommon":
            rarity_prefix = "⭐ ELITE: "
        
        if action == "appears":
            return f"{rarity_prefix}{emoji} A wild [bold {self.rarity_color}]{self.name}[/bold {self.rarity_color}] appears!"
        elif action == "attacks":
            return f"{emoji} {self.name} prepares to attack!"
        elif action == "defeated":
            return f"💀 {self.name} has been defeated!"
        
        return f"{emoji} {self.name} {action}!"
    
    def get_reward_multiplier(self):
        """Get reward multiplier based on rarity and boss status"""
        multipliers = {
            "common": 1.0,
            "uncommon": 1.3,
            "rare": 1.6,
            "legendary": 2.0
        }
        
        base_multiplier = multipliers.get(self._rarity, 1.0)
        
        if self._is_boss:
            base_multiplier *= 2.0
        
        return base_multiplier
    
    def __str__(self):
        rarity_indicator = f" ({self._rarity.title()})" if self._rarity != "common" else ""
        boss_indicator = " [BOSS]" if self._is_boss else ""
        return f"{self.name}{rarity_indicator}{boss_indicator} (Level {self.level}) - HP: {self.hp}/{self.max_hp}, Attack: {self.attack}"
    
    def __repr__(self):
        return f"Monster(name='{self.name}', hp={self.hp}, attack={self.attack}, level={self.level}, rarity='{self._rarity}', is_boss={self._is_boss})"