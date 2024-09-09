import os
import random
from tqdm import tqdm
import sys
import glob
import readline

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

def count_lines(file_path):
    with open(file_path, 'rb') as f:
        return sum(1 for _ in f)

def read_wordlist(file_path):
    words = []
    total_lines = count_lines(file_path)
    
    with tqdm(total=total_lines, unit='line', desc="Reading wordlist", ncols=80, 
              bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} lines [{elapsed}<{remaining}]') as pbar:
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():
                    words.append(line.strip())
                pbar.update(1)
    
    return words

def write_wordlist(words, file_path):
    with open(file_path, 'w') as f:
        f.write('\n'.join(words))

def split_list(words, n):
    k, m = divmod(len(words), n)
    return [words[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

def process_section(words, action):
    if action == 'reverse':
        return list(reversed(words))
    elif action == 'randomize':
        random.shuffle(words)
        return words
    else:
        return words

def get_action():
    while True:
        action = input(color.YELLOW + "Choose action (reverse/randomize/none): " + color.END).lower()
        if action in ['reverse', 'randomize', 'none']:
            return action
        print(color.RED + "Invalid action. Please choose 'reverse', 'randomize', or 'none'." + color.END)

def complete_path(text, state):
    """Tab completion function for file paths"""
    if '~' in text:
        text = os.path.expanduser(text)
    return [x for x in glob.glob(text+'*')][state]

def main():
    print(f"""
{color.YELLOW}--------------------    {color.CYAN}-------------------------
{color.CYAN}▗▖ ▗▖ ▗▄▖ ▗▄▄▖ ▗▄▄▄      {color.YELLOW}▗▄▄▖ ▗▄▖ ▗▖    ▗▄▖ ▗▄▄▄ 
{color.CYAN}▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌▐▌  █    {color.YELLOW}▐▌   ▐▌ ▐▌▐▌   ▐▌ ▐▌▐▌  █
{color.CYAN}▐▌ ▐▌▐▌ ▐▌▐▛▀▚▖▐▌  █    {color.YELLOW} ▝▀▚▖▐▛▀▜▌▐▌   ▐▛▀▜▌▐▌  █
{color.CYAN}▐▙█▟▌▝▚▄▞▘▐▌ ▐▌▐▙▄▄▀    {color.YELLOW}▗▄▄▞▘▐▌ ▐▌▐▙▄▄▖▐▌ ▐▌▐▙▄▄▀
{color.YELLOW}--------------------    {color.CYAN}-------------------------
{color.END}""")
    
    try:
        # Set up tab completion
        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(complete_path)
        # Get input file
        input_file = input(color.BLUE + "> Enter the path to the input wordlist file: " + color.END)
        while not os.path.exists(input_file):
            print(color.RED + "File not found. Please try again." + color.END)
            input_file = input(color.BLUE + "> Enter the path to the input wordlist file: " + color.END)

        # Read the input wordlist
        words = read_wordlist(input_file)

        # Get number of sections
        while True:
            try:
                num_sections = int(input(color.BLUE + "\n>> Enter the number of sections to split the wordlist into: " + color.END))
                if num_sections > 0:
                    break
                print(color.RED + "\nPlease enter a positive integer." + color.END)
            except ValueError:
                print(color.RED + "\nInvalid input. Please enter a positive integer." + color.END)

        # Split the wordlist into sections
        sections = split_list(words, num_sections)

        # Process each section
        input_filename = os.path.splitext(os.path.basename(input_file))[0]  # Get input filename without extension
        for i, section in enumerate(sections):
            print(color.YELLOW + f"\nSection {i+1}" + color.END)
            action = get_action()
            processed_section = process_section(section, action)
            
            # Create the output filename
            output_file = f"{input_filename}_section_{i+1}_{action}.txt"
            write_wordlist(processed_section, output_file)
            print(color.GREEN + f"Section {i+1} ({action}) written to {output_file}" + color.END)

        print(color.GREEN + "\nAll sections processed and saved.\n" + color.END)

    except KeyboardInterrupt:
        print(color.RED + "\n\nProgram interrupted by user. Exiting...\n" + color.END)
        sys.exit(0)

if __name__ == "__main__":
    main()