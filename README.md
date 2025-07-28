# 🗡️ Dungeon Forge RPG

*A classic text-based RPG adventure built with Python*

---

## 🎮 Game Overview

**Dungeon Forge RPG** is an immersive command-line role-playing game that brings back the golden age of text adventures. Create your hero, battle fearsome monsters, level up your skills, and forge your legend in this exciting dungeon-crawling experience.

### ✨ Key Features

- **Three Unique Classes**: Choose your path as a mighty Warrior, mystical Mage, or cunning Rogue
- **Dynamic Combat System**: Engage in turn-based battles with special attacks and strategic potion usage
- **Progressive Difficulty**: Face increasingly challenging foes as you grow stronger
- **Character Progression**: Level up to unlock powerful abilities and increased stats
- **Interactive Shop**: Purchase health and mana potions to aid your adventures
- **Rich Monster Variety**: Battle 8 different creature types, from goblins to dragon whelps

---

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher
- Terminal/Command Prompt access

### Installation & Setup

1. **Clone or download** the game files to your local machine
2. **Navigate** to the game directory in your terminal
3. **Run the game**:
   ```bash
   python main.py
   ```

That's it! No additional dependencies required.

---

## 🎯 How to Play

### Character Creation
Choose from three distinct classes, each with unique strengths:

| Class | Strengths | Special Ability |
|-------|-----------|----------------|
| **⚔️ Warrior** | High HP & Attack | Mighty Slash |
| **🔮 Mage** | Powerful Magic | Fireball |
| **🗡️ Rogue** | Balanced & Agile | Sneak Attack |

### Combat System
- **Regular Attacks**: Reliable damage with slight variance
- **Special Attacks**: Powerful abilities with cooldown periods and mana costs
- **Potions**: Heal HP or restore mana during battle
- **Escape Option**: Attempt to flee from overwhelming foes (30% success rate)

### Progression
- **Gain XP** by defeating monsters
- **Level up** to increase all stats and unlock stronger abilities
- **Earn gold** to purchase essential supplies
- **Face elite enemies** as you become more powerful

---

## 🎲 Game Mechanics

### Stats Explained
- **HP (Health Points)**: Your life force - reach 0 and it's game over
- **Mana**: Required for special attacks and magical abilities  
- **Attack**: Base damage for regular attacks
- **Special Damage**: Enhanced damage for class abilities
- **Gold**: Currency for purchasing items

### Monster Scaling
Enemies automatically scale with your level, ensuring consistent challenge:
- **Elite** monsters appear at level 4+
- **Champion** monsters appear at level 7+  
- **Legendary** monsters appear at level 11+

---

## 📁 Project Structure

```
dungeon-forge-rpg/
├── main.py          # Game entry point and main loop
├── player.py        # Character management and abilities
├── combat.py        # Battle system and mechanics
├── monsters.py      # Creature generation and scaling
├── shop.py          # Merchant and item trading
└── utils.py         # Helper functions and utilities
```


---

## 🎪 Sample Gameplay

```
==================================================
      WELCOME TO DUNGEON FORGE RPG!
==================================================

Enter your character's name: Heroic_Player
Choose your class:
1. Warrior - High health and attack
2. Mage - Moderate stats, powerful special attack  
3. Rogue - Balanced stats, quick special cooldown

Welcome, Heroic_Player the Warrior!
Your adventure begins now...

==================================================
  Heroic_Player - Level 1 Warrior
==================================================
HP: 100/100 | Mana: 30/30 | Gold: 50
Attack: 20 | XP: 0/50
```

---

## 🎯 Future Enhancements

- **Equipment System**: Weapons and armor to customize your build
- **Quest System**: Story-driven missions with unique rewards
- **Multiple Areas**: Different dungeons and environments to explore
- **Save/Load Feature**: Preserve your progress between sessions
- **Boss Battles**: Epic encounters with legendary creatures

---

## 🤝 Contributing

Interested in improving Dungeon Forge RPG? Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🎮 Alternative Game Names

Can't decide on "Dungeon Forge RPG"? Here are some other great options:

- **Terminal Quest** - *Classic Adventure Awaits*
- **Console Crusader** - *Text-Based Fantasy RPG*  
- **ASCII Adventures** - *Retro Gaming Experience*
- **Command Line Champion** - *Pure Python RPG*
- **Text Realm** - *Where Words Become Worlds*

---

<div align="center">

**Ready to forge your legend? The dungeon awaits!** ⚔️

*Built with ❤️ and Python*

</div>