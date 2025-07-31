

---

# 🎮 Python Adventure RPG ⚔️

<div align="center">

**A vibrant and immersive terminal-based fantasy RPG built in Python using the `rich` library.**

![Gameplay Screenshot](image.png)

</div>

---

## ✨ Overview

**Python Adventure RPG** is a text-based terminal RPG that combines nostalgic gameplay with modern visuals using `rich`. Create your character, choose a class, battle monsters, level up, shop for potions, and save your progress — all from the command line.

---

## 🚀 Features

* **🎨 Rich UI**: Uses the `rich` library for stunning UI — colored text, tables, panels, progress bars.
* **🧙 Class System**: Choose from **Warrior**, **Mage**, or **Rogue**, each with unique stats and abilities.
* **⚔️ Strategic Combat**: Turn-based battles with regular attacks, class-based special moves, and potions.
* **👹 Monster Scaling**: Fight 8 monster types — including Goblins, Trolls, and Dragon Whelps — with difficulty scaling to your level.
* **📈 Level Progression**: Gain XP and level up to improve HP, Mana, Attack, and Special abilities.
* **🏪 Potion Shop**: Purchase health and mana potions that scale in price and potency with your level.
* **💾 Save/Load**: Supports saving to and loading from named save files via JSON in a `saves/` directory.
* **🏃 Escape Mechanic**: Attempt to flee from battle with a 30% chance of success.

---

## 🛠️ Installation

### Requirements

* Python 3.7+
* A terminal that supports ANSI colors

### Setup

```bash
git clone https://github.com/your-username/rpg_cli.git
cd rpg_cli
pip install rich
python main.py
```

---

## 🎮 How to Play

### Character Creation

Start the game and create your hero:

1. Choose a name.
2. Pick a class:

   | Class      | Strengths                | Special Ability |
   | ---------- | ------------------------ | --------------- |
   | ⚔️ Warrior | High HP & Attack         | Mighty Slash    |
   | 🔮 Mage    | High Magic Damage        | Fireball        |
   | 🗡️ Rogue  | Balanced & Fast Cooldown | Sneak Attack    |

---

### Game Menu Options

Once in the main loop, you can:

* `⚔️ Fight a monster`: Battle a scaled monster.
* `🏪 Visit the shop`: Buy potions.
* `🧪 Use health potion`: Heal yourself outside combat.
* `🔮 Use mana potion`: Restore mana outside combat.
* `📊 View character info`: Full stat display.
* `💾 Save game`: Save progress to a JSON file.
* `📁 Load game`: Load a previously saved file.
* `🚪 Quit game`: Exit.

---

### Combat Mechanics

Combat is turn-based with multiple actions:

* **1. Regular Attack** — Basic attack.
* **2. Special Attack** — High-damage class skill (mana + cooldown).
* **3. Use Health Potion** — Restores HP, skips enemy turn.
* **4. Use Mana Potion** — Restores Mana, skips enemy turn.
* **5. Try to Run Away** — 30% success chance.

Each turn updates status bars, stats, and cooldowns.

---

### Shop System

* Potions scale with your level.
* Prices increase as you grow stronger.
* Health Potion: Restores HP.
* Mana Potion: Restores Mana.
* Purchase as many as you can afford.

---

### Save & Load

* Automatically creates a `saves/` directory.
* Save files are stored in JSON format.
* Supports named saves and overwrite confirmation.

---

## 📁 Project Structure

```
rpg_cli/
├── main.py          # Entry point
├── game.py          # Game loop and flow logic
├── player.py        # Player class with progression, potions, etc.
├── monsters.py      # Monster definitions and scaling
├── combat.py        # Turn-based combat system
├── shop.py          # Potion shop with level-based pricing
├── utils.py         # Helper functions (UI, formatting)
├── saves/           # Save files (auto-created)
├── README.md        # This file
└── LICENSE          # MIT License
```

---

## 💡 Planned Features

* 🗡 Equipment system (gear, armor)
* 🧭 Quest system with side missions
* 🌍 Multiple environments (dungeons, towns)
* 🧠 Skill trees for class upgrades
* 🐉 Boss fights with unique mechanics

---

## 🤝 Contributing

Contributions welcome!

1. Fork it
2. Create a branch (`git checkout -b feature/thing`)
3. Commit (`git commit -m 'Add thing'`)
4. Push (`git push origin feature/thing`)
5. PR

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---


