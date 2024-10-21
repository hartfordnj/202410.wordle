import random
import os

# Define a word bank for each difficulty category with 5-letter words
easy_words = ["brick", "chart", "habit", "blank", "fight", "light", "lemon", "apple", "beach", "grape", "plant", "storm", "candy", "drink", "paper", "flame", "store", "party", "chair", "taste", "bread", "shiny", "water", "smile"]
medium_words = ["stoop", "check", "leaky", "spool", "trace", "frank", "crisp", "brisk", "plumb", "sheep", "grasp", "flock", "spear", "cloak", "crave", "blink", "flint", "proud", "stark", "shrub", "brace", "flour", "plume", "whisk"]
hard_words = ["realm", "haste", "lapse", "clamp", "knack", "glyph", "prank", "shrew", "wince", "quilt", "pivot", "flair", "quash", "brine", "scorn", "twist", "crisp", "wharf", "fluke", "mourn", "slant"]
expert_words = ["azure", "plumb", "fjord", "glyph", "wrath", "quoth", "whisk", "sword", "whale", "scalp", "fluke", "mirth", "snarl", "crust", "blurt", "quack", "slink", "quilt", "wrist", "squib", "flint", "shard", "blimp", "crave"]
legendary_words = ["nymph", "glyph", "sphinx", "joust", "fjord", "quark", "wharf", "zilch", "flask", "gnash", "knave", "tryst", "whorl", "lynch", "crust", "plumb", "sworn", "whisk", "blitz", "quill", "shirk", "quaff", "wrung"]

# Define enemy types with base difficulty ratios
enemies = {
    "Grunt": {"easy": 30, "medium": 40, "hard": 30},
    "Warrior": {"easy": 20, "medium": 50, "hard": 30},
    "Champion": {"medium": 20, "hard": 50, "expert": 30},
    "Guardian": {"hard": 30, "expert": 50, "legendary": 20},
    "Overlord": {"expert": 40, "legendary": 60}
}

# Define a pool of books with their properties
book_pool = [
    {"name": "Book of Position 1 Reveal", "effect": "reveal_position_1_40", "rarity": "common"},
    {"name": "Book of Vowels", "effect": "reveal_vowel_50", "rarity": "rare"},
    {"name": "Book of Extra Guess", "effect": "extra_guess", "rarity": "common"},
    {"name": "Book of Middle Letter", "effect": "reveal_middle_letter_40", "rarity": "uncommon"},
    {"name": "Book of Luck", "effect": "increase_effects_10", "rarity": "rare"},
    {"name": "Book of Last Letter", "effect": "reveal_last_letter_40", "rarity": "uncommon"},
    {"name": "Book of Books", "effect": "notify_double_vowels_40", "rarity": "rare"},
    {"name": "Book of Stuck", "effect": "notify_unique_letters_30", "rarity": "rare"}
]

# Define the Bookbag class to manage inventory
class Bookbag:
    def __init__(self, capacity=5):
        self.capacity = capacity
        self.books = []

    def add_book(self, book):
        """Add a book to the Bookbag, if there's space."""
        if len(self.books) < self.capacity:
            self.books.append(book)
            print(f"Added {book['name']} to your Bookbag.")
        else:
            print("Your Bookbag is full! You need to remove a book to add a new one.")
            self.display_books()
            if input("Would you like to remove a book? (y/n): ").strip().lower() == 'y':
                self.remove_book()  # Prompt player to remove a book if bag is full
                self.add_book(book)  # Add the new book after making space

    def remove_book(self):
        """Remove a book from the Bookbag."""
        print("Which book would you like to remove?")
        self.display_books()
        choice = input("Enter the number of the book to remove: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(self.books):
            removed_book = self.books.pop(int(choice) - 1)
            print(f"Removed {removed_book['name']} from your Bookbag.")
        else:
            print("Invalid choice. No book was removed.")

    def display_books(self, book_effects=None):
        """Display the books currently in the Bookbag, including whether they triggered."""
        if not self.books:
            print("Your Bookbag is empty.")
        else:
            for i, book in enumerate(self.books, 1):
                effect_status = "Nope!"
                if book_effects and book['effect'] in book_effects:
                    effect_status = book_effects[book['effect']]
                print(f"{i}: {book['name']} - {book['rarity'].capitalize()} - {effect_status}")

    def get_effects(self):
        """Return a list of all book effects currently in the Bookbag."""
        return [book['effect'] for book in self.books]

def clear_terminal():
    """Clear the terminal for a clean display."""
    os.system('cls' if os.name == 'nt' else 'clear')

def adjust_ratios(ratios):
    """Randomize the difficulty ratios by +/- 5%."""
    adjustments = [random.randint(-5, 5) for _ in range(len(ratios))]
    for i, key in enumerate(ratios.keys()):
        ratios[key] = max(0, ratios[key] + adjustments[i])
    
    # Normalize to ensure total adds up to 100%
    total = sum(ratios.values())
    for key in ratios:
        ratios[key] = int((ratios[key] / total) * 100)

def select_word(ratios, debug_mode):
    """Select a word based on the adjusted ratios."""
    difficulty = random.choices(
        list(ratios.keys()), 
        weights=list(ratios.values())
    )[0]

    word_pools = {
        "easy": easy_words,
        "medium": medium_words,
        "hard": hard_words,
        "expert": expert_words,
        "legendary": legendary_words
    }
    word = random.choice(word_pools[difficulty])

    if debug_mode:
        print(f"(DEBUG) Selected word: {word} ({difficulty})")  # Debug line
    return word, difficulty

def give_feedback(guess, word, keyboard):
    """Provide feedback on the player's guess, similar to Wordle feedback."""
    feedback = []
    for i, char in enumerate(guess):
        if i < len(word) and char == word[i]:
            feedback.append(char.upper())  # Correct position
            keyboard[char] = char.upper()
        elif char in word:
            feedback.append(char.lower())  # Wrong position but in the word
            if keyboard[char].islower():
                keyboard[char] = char.lower()
        else:
            feedback.append("_")  # Not in word
            keyboard[char] = "_"
    return " ".join(feedback)

def reveal_consonant(word):
    """Reveal one consonant in the word."""
    consonants = [char for char in word if char not in 'aeiou']
    if consonants:
        revealed = random.choice(consonants)
        print(f"A consonant has been revealed: {revealed}")
        return revealed
    return None

def reveal_vowel(word):
    """Reveal one vowel in the word."""
    vowels = [char for char in word if char in 'aeiou']
    if vowels:
        revealed = random.choice(vowels)
        return revealed
    return None

def display_keyboard(keyboard):
    """Display the keyboard with the status of each letter."""
    keyboard_layout = [
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm"
    ]
    print("\nKeyboard:")
    for row in keyboard_layout:
        print(" ".join([keyboard[char] for char in row]))
    print()
    
    # Display correct and incorrect letters
    correct_letters = [char for char in keyboard if keyboard[char].isupper() or keyboard[char].islower()]
    incorrect_letters = [char for char in keyboard if keyboard[char] == '_']
    print(f"Correct: {' '.join(correct_letters)}")
    print(f"Incorrect: {' '.join(incorrect_letters)}")
    print()

def choose_book(available_books):
    """Allow the player to choose a book at the end of a round."""
    print("\nYou have found two books!")

    # Randomly select two books from the book pool
    book_choices = random.sample(available_books, 2)
    for i, book in enumerate(book_choices, 1):
        print(f"{i}: {book['name']} - {book['rarity'].capitalize()}")

    choice = input("Choose a book (1 or 2): ").strip()

    if choice in ["1", "2"]:
        chosen_book = book_choices[int(choice) - 1]
        return chosen_book["effect"]
    return None

# Main game loop
def main():
    print("Welcome to the Wordle Roguelike!")  # Introductory message
    start_game = input("Press 'Y' to begin or any other key to quit: ").strip().lower()
    if start_game != 'y':
        print("Goodbye!")
        return

    debug_mode = input("Enable debug mode? (y/n): ").strip().lower() == 'y'
    enemies_to_fight = ["Grunt", "Grunt", "Warrior", "Warrior", "Champion", "Champion", "Guardian", "Overlord"]
    bookbag = Bookbag()

    for round_count, enemy in enumerate(enemies_to_fight, 1):
        clear_terminal()
        print(f"Round {round_count} of {len(enemies_to_fight)}: Encountering a {enemy}")
        if not simulate_battle(enemy, bookbag.get_effects(), bookbag, debug_mode):
            print("Game Over!")
            play_again = input("Would you like to play again? (y/n): ").strip().lower()
            if play_again == 'y':
                main()
            else:
                print("Thanks for playing!")
                return
        print("Congratulations! You've defeated the enemy!")
    else:
        print("You defeated all the enemies! Congratulations!")



def simulate_battle(enemy, book_effects, bookbag, debug_mode):
    """Simulate a word battle against an enemy."""
    print("Starting battle...")  # Debugging statement
    attempts = 5  # Initialize attempts before any modifications
    increase_chance = 0  # Initialize increase_chance to ensure it is available for use
    word, difficulty = select_word(enemies[enemy], debug_mode)

    # Initialize keyboard for player feedback
    keyboard = {char: char for char in 'abcdefghijklmnopqrstuvwxyz'}
    
    # Display initial status of the Bookbag
    bookbag.display_books()
    
    # Player has multiple attempts to guess the word
    while attempts > 0:
        display_keyboard(keyboard)
        guess = input(f"Enter your {len(word)}-letter guess: ").strip().lower()
        
        # Validate the length of the guess
        if len(guess) != len(word):
            print(f"Your guess must be {len(word)} letters long.")
            continue
        
        # Check if the guess is correct
        if guess == word:
            print(f"Correct! You defeated the {enemy}!")
            # Allow the player to choose a book after a successful battle
            available_books = [book for book in book_pool if book['effect'] not in bookbag.get_effects()]
            if available_books:
                chosen_book = choose_book(available_books)
                if chosen_book:
                    bookbag.add_book(next(book for book in book_pool if book['effect'] == chosen_book))
            return True
        else:
            # Provide feedback and reduce the number of attempts
            feedback = give_feedback(guess, word, keyboard)
            print(f"Feedback: {feedback}")
            attempts -= 1
            print(f"{attempts} attempts remaining.")
    
    # If player runs out of attempts
    print(f"You failed to defeat the {enemy}. The word was: {word}.")
    return False

if __name__ == "__main__":
    main()





