# 🎮 Python Adventure RPG ⚔️

<div align="center">

**A vibrant and immersive text-based RPG adventure built with Python and the `rich` library.**

![Gameplay Screenshot](https://i.imgur.com/gJ5n4f5.png)

</div>

---

## ✨ Overview

Welcome to **Python Adventure RPG**, a classic command-line role-playing game that brings the magic of text-based adventures to life with a modern, colorful interface. Create your hero, choose your class, and embark on an epic journey filled with dangerous monsters, strategic combat, and glorious treasure. Forge your legend, one command at a time!

---

## 🚀 Key Features

-   **🎨 Rich & Beautiful Interface**: Utilizes the `rich` library for stunning, modern-looking text, tables, panels, and progress bars in the terminal.
-   **🛡️ Three Unique Classes**: Choose your path as a mighty **Warrior**, a powerful **Mage**, or a cunning **Rogue**, each with unique stats and special attacks.
-   **⚔️ Dynamic Turn-Based Combat**: Engage in strategic battles featuring regular attacks, mana-based special abilities with cooldowns, and potion usage.
-   **📈 Character Progression**: Gain XP by defeating monsters, level up to enhance your stats, and grow from a novice adventurer into a legendary hero.
-   **👹 Diverse Monster Menagerie**: Battle 8 different types of creatures, from lowly Goblins to fearsome Dragon Whelps, that scale in difficulty with your level.
-   **🏪 Interactive Shop**: Use the gold earned from your victories to visit the merchant and stock up on vital health and mana potions.
-   **💾 Save & Load System**: Your progress is valuable! Save your game at any time and load it later to continue your adventure right where you left off.
-   **🏃 Escape Mechanics**: Not ready for a fight? You have a chance to run away, but be warned—it's not always successful!

---

## 🛠️ Getting Started

### Prerequisites

-   Python 3.7 or higher
-   A terminal that supports rich text and colors (most modern terminals do).

### Installation & Setup

1.  **Clone the repository** to your local machine.
    ```bash
    git clone [https://github.com/your-username/rpg_cli.git](https://github.com/your-username/rpg_cli.git)
    ```
2.  **Navigate** to the game directory.
    ```bash
    cd rpg_cli
    ```
3.  **Install the required dependency**. This game uses the `rich` library to create its beautiful interface.
    ```bash
    pip install rich
    ```
4.  **Run the game**!
    ```bash
    python main.py
    ```

---

## 🎯 How to Play

### Character Creation

Your journey begins by creating a character. You will:
1.  **Enter a name** for your hero.
2.  **Choose a class**:
    | Class | Strengths | Special Ability |
    | :--- | :--- | :--- |
    | **⚔️ Warrior** | High HP & Attack | **Mighty Slash** |
    | **🔮 Mage** | Powerful Magic | **Fireball** |
    | **🗡️ Rogue** | Balanced & Agile | **Sneak Attack** |

### The Main Loop

Once in the game, you'll be presented with a main menu where you can choose your next action:
-   **Fight a monster**: Seek out and battle a random creature.
-   **Visit the shop**: Purchase potions.
-   **Use potions**: Heal HP or restore Mana outside of combat.
-   **View character info**: See your detailed stats and progress.
-   **Save/Load game**: Manage your game sessions.
-   **Quit**: Exit the game.

### Combat System

Combat is turn-based. On your turn, you can:
-   **Regular Attack**: A standard attack with reliable damage.
-   **Special Attack**: A powerful, class-specific move that costs mana and has a cooldown period.
-   **Use Potions**: Use your turn to heal or restore mana. This action allows you to skip the monster's next attack.
-   **Try to Run Away**: Attempt to flee from battle (30% success rate).

### Progression

-   **Gain XP & Gold**: Defeating monsters rewards you with experience points and gold.
-   **Level Up**: Accumulate enough XP to level up, which increases all your stats, fully restores your HP/Mana, and increases the XP required for the next level.
-   **Monster Scaling**: The monsters you encounter become stronger as you level up, ensuring the challenge never fades.
    -   **Elite** monsters appear at level 4+
    -   **Champion** monsters appear at level 7+
    -   **Legendary** monsters appear at level 11+

---

## 📁 Project Structure

The project is organized into modular files, making it easy to understand and extend.


rpg_cli/
├── main.py          # The main entry point for the game.
├── game.py          # Core game loop, main menu, and event handling.
├── player.py        # Manages the player character, stats, inventory, and progression.
├── monsters.py      # Defines all monster types, their stats, and scaling logic.
├── combat.py        # Handles the turn-based combat system and battle actions.
├── shop.py          # Implements the interactive item shop.
├── utils.py         # Utility functions used across the project (now mostly handled by rich).
├── saves/           # Directory where save files are stored (created automatically).
├── README.md        # You are here!
└── LICENSE          # The MIT License file.


---

## 💡 Future Enhancements

This project has a solid foundation, but there's always room for more adventure!
-   **Equipment System**: Introduce weapons, armor, and accessories.
-   **Quest System**: Add story-driven missions with unique rewards.
-   **More Environments**: Explore different dungeons, forests, and towns.
-   **Boss Battles**: Create epic encounters with powerful, unique bosses.
-   **Expanded Skill Trees**: Allow for more customization upon leveling up.

---

## 🤝 Contributing

Contributions are welcome and greatly appreciated! If you have an idea for an improvement:

1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---

## 📄 License

This project is open source and distributed under the **MIT License**. See `LICENSE` for more information.

---

<div align="center">

**Ready to forge your legend? The adventure awaits!**

*Built with ❤️ and Python*

</div>
