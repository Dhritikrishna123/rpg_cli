# utils.py - Utility functions
import os

def clear_screen():
    """Clear the console screen"""
    # Works on both Windows and Unix-like systems
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_choice(prompt, valid_choices):
    """Get valid user input from a list of choices"""
    while True:
        choice = input(prompt).strip().lower()
        
        # Check if choice is valid (case-insensitive)
        for valid_choice in valid_choices:
            if choice == valid_choice.lower():
                return choice
        
        print(f"Invalid choice! Please enter one of: {', '.join(valid_choices)}")

def display_health_bar(current_hp, max_hp, width=20):
    """Display a visual health bar"""
    if max_hp <= 0:
        return "[" + " " * width + "]"
    
    filled = int((current_hp / max_hp) * width)
    filled = max(0, min(filled, width))  # Ensure it's within bounds
    
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}]"

def format_number(number):
    """Format numbers with commas for better readability"""
    return f"{number:,}"

def calculate_damage_range(base_damage, variance=3):
    """Calculate damage range for display purposes"""
    min_damage = max(1, base_damage - variance)
    max_damage = base_damage + variance
    return f"{min_damage}-{max_damage}"

def press_enter_to_continue():
    """Standard press enter to continue prompt"""
    input("\nPress Enter to continue...")

def display_separator(char="=", width=50):
    """Display a separator line"""
    print(char * width)

def get_yes_no_input(prompt):
    """Get yes/no input from user"""
    while True:
        choice = input(prompt + " (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def display_title(title, width=50):
    """Display a centered title with borders"""
    title_length = len(title)
    padding = (width - title_length - 2) // 2
    
    print("=" * width)
    print(" " * padding + title + " " * padding)
    if (width - title_length - 2) % 2 == 1:
        print(" " * (padding + 1))  # Add extra space if odd
    print("=" * width)