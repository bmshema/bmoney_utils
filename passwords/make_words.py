import itertools
import string
import time
from tqdm import tqdm

class color:
   PURPLE = '\033[1;35;48m'
   CYAN = '\033[1;36;48m'
   BOLD = '\033[1;37;48m'
   BLUE = '\033[1;34;48m'
   GREEN = '\033[1;32;48m'
   YELLOW = '\033[1;33;48m'
   RED = '\033[1;31;48m'
   BLACK = '\033[1;30;48m'
   UNDERLINE = '\033[4;37;48m'
   END = '\033[1;37;0m'


def generate_wordlist(min_length, max_length, char_set, custom_strings, custom_position):
    wordlist = []
    total_combinations = sum(len(char_set) ** length for length in range(min_length, max_length + 1))
    if custom_strings:
        total_combinations *= len(custom_strings)
        if custom_position == 'both':
            total_combinations *= 2

    with tqdm(total=total_combinations, unit='word', desc="Generating", ncols=80, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
        for length in range(min_length, max_length + 1):
            for combo in itertools.product(char_set, repeat=length):
                word = ''.join(combo)
                if custom_strings:
                    if custom_position == 'start':
                        wordlist.extend([custom + word for custom in custom_strings])
                        pbar.update(len(custom_strings))
                    elif custom_position == 'end':
                        wordlist.extend([word + custom for custom in custom_strings])
                        pbar.update(len(custom_strings))
                    else:  # both
                        wordlist.extend([custom + word for custom in custom_strings])
                        wordlist.extend([word + custom for custom in custom_strings])
                        pbar.update(2 * len(custom_strings))
                else:
                    wordlist.append(word)
                    pbar.update(1)
    return wordlist

def main():
    print(color.BLUE + """
▗▖  ▗▖▗▄▖ ▗▖ ▗▖     ▗▄▖ ▗▖  ▗▖▗▄▄▄     ▗▖  ▗▖▗▄▖ ▗▖ ▗▖▗▄▄▖     ▗▖ ▗▖ ▗▄▖ ▗▄▄▖ ▗▄▄▄  ▗▄▄▖
 ▝▚▞▘▐▌ ▐▌▐▌ ▐▌    ▐▌ ▐▌▐▛▚▖▐▌▐▌  █     ▝▚▞▘▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌    ▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌▐▌  █▐▌   
  ▐▌ ▐▌ ▐▌▐▌ ▐▌    ▐▛▀▜▌▐▌ ▝▜▌▐▌  █      ▐▌ ▐▌ ▐▌▐▌ ▐▌▐▛▀▚▖    ▐▌ ▐▌▐▌ ▐▌▐▛▀▚▖▐▌  █ ▝▀▚▖
  ▐▌ ▝▚▄▞▘▝▚▄▞▘    ▐▌ ▐▌▐▌  ▐▌▐▙▄▄▀      ▐▌ ▝▚▄▞▘▝▚▄▞▘▐▌ ▐▌    ▐▙█▟▌▝▚▄▞▘▐▌ ▐▌▐▙▄▄▀▗▄▄▞▘
""" + color.END)
    
    char_set = ""
    options = [
        ("Digits", string.digits),
        ("Lowercase letters", string.ascii_lowercase),
        ("Uppercase letters", string.ascii_uppercase),
        ("Special characters", string.punctuation)
    ]
    
    print(color.YELLOW + "Select character sets (enter option number(s) separated by space):" + color.END)
    for i, (name, _) in enumerate(options, 1):
        print(f"{i}. {name}")
    
    selections = input(color.YELLOW + "\nEnter your choices: " + color.END).split()
    for selection in selections:
        if selection.isdigit() and 1 <= int(selection) <= len(options):
            char_set += options[int(selection) - 1][1]
    
    if not char_set:
        print(color.RED + "No valid selection. Using digits." + color.END)
        char_set = string.digits

    length_input = input(color.YELLOW + "\nEnter length or range (e.g., 4 or 4-8): " + color.END)
    if '-' in length_input:
        min_length, max_length = map(int, length_input.split('-'))
    else:
        min_length = max_length = int(length_input)

    custom_strings = input(color.YELLOW + "\nEnter custom strings to add (comma-separated, or press Enter to skip): " + color.END).split(',')
    custom_strings = [s.strip() for s in custom_strings if s.strip()]

    if custom_strings:
        print(color.YELLOW + "\nWhere should custom strings be added?" + color.END)
        print("1. At the start of each word")
        print("2. At the end of each word")
        print("3. Both start and end")
        custom_position = input(color.YELLOW + "\nEnter your choice (1/2/3): " + color.END)
        print("\n")
        if custom_position == '1':
            custom_position = 'start'
        elif custom_position == '2':
            custom_position = 'end'
        else:
            custom_position = 'both'
    else:
        custom_position = None

    start_time = time.time()
    wordlist = generate_wordlist(min_length, max_length, char_set, custom_strings, custom_position)
    end_time = time.time()

    print(color.GREEN + f"\nGenerated {len(wordlist)} words in {end_time - start_time:.2f} seconds." + color.END)
    save = input(color.YELLOW + "Save to file? (y/n): " + color.END).lower()
    if save == 'y':
        filename = input(color.YELLOW + "\nEnter filename: " + color.END)
        with open(filename, 'w') as f:
            f.write('\n'.join(wordlist))
        print(f"Wordlist saved to {filename}")

if __name__ == "__main__":
    main()