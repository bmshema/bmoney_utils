import os
import sys
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

def is_valid_psk(line):
    return 8 <= len(line.strip()) <= 63 and all(32 <= ord(char) <= 126 for char in line.strip())

def process_wordlist(input_file):
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"{base_name}_PSKs.txt"
    
    valid_psks = []
    total_lines = sum(1 for _ in open(input_file, 'r'))
    
    with tqdm(total=total_lines, desc="Processing", unit="line") as pbar:
        with open(input_file, 'r') as infile:
            for line in infile:
                if is_valid_psk(line):
                    valid_psks.append(line.strip())
                pbar.update(1)
    
    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(valid_psks))
    
    return len(valid_psks), output_file

def main():
    print(f"""
{color.YELLOW}---------------    {color.YELLOW}------------------------------------
{color.BLUE}▗▄▄▖  ▗▄▄▖▗▖ ▗▖    {color.BLUE}▗▄▄▄▖▗▖  ▗▖▗▄▄▄▖▗▄▄▖  ▗▄▖  ▗▄▄▖▗▄▄▄▖
{color.BLUE}▐▌ ▐▌▐▌   ▐▌▗▞▘    {color.BLUE}▐▌    ▝▚▞▘   █  ▐▌ ▐▌▐▌ ▐▌▐▌     █  
{color.BLUE}▐▛▀▘  ▝▀▚▖▐▛▚▖     {color.BLUE}▐▛▀▀▘  ▐▌    █  ▐▛▀▚▖▐▛▀▜▌▐▌     █  
{color.BLUE}▐▌   ▗▄▄▞▘▐▌ ▐▌    {color.BLUE}▐▙▄▄▖▗▞▘▝▚▖  █  ▐▌ ▐▌▐▌ ▐▌▝▚▄▄▖  █  
{color.YELLOW}---------------    {color.YELLOW}------------------------------------
{color.END}""")
    
    if len(sys.argv) < 2:
        print(color.RED + "Provide at least one input file.\n" + color.END)
        sys.exit(1)
    
    total_extracted = 0
    files_processed = 0
    file_stats = []

    try:
        for input_file in sys.argv[1:]:
            if not os.path.exists(input_file):
                print(color.RED + f"File not found: {input_file}" + color.END)
                continue
            
            print(color.BLUE + f"\nProcessing {input_file}..." + color.END)
            psk_count, output_file = process_wordlist(input_file)
            print(color.GREEN + f"Extracted {psk_count} valid PSKs to {output_file}" + color.END)
            
            total_extracted += psk_count
            files_processed += 1
            
            # Count total words in input file
            with open(input_file, 'r') as f:
                total_words = sum(1 for _ in f)
            
            file_stats.append((input_file, total_words, psk_count, output_file))
    
    except KeyboardInterrupt:
        print(color.RED + "\nOperation cancelled..." + color.END)
    
    # Prompt to merge extracted words if more than one wordlist was processed
    if files_processed > 1:
        merge_prompt = input(color.YELLOW + "\nWould you like to merge all extracted words into one list? (y/n): " + color.END).lower()
        if merge_prompt == 'y':
            merged_filename = input(color.YELLOW + "Enter filename for the merged list: " + color.END)
            merged_words = set()
            for _, _, _, output_file in file_stats:
                with open(output_file, 'r') as f:
                    merged_words.update(f.read().splitlines())
            
            with open(merged_filename, 'w') as f:
                f.write('\n'.join(sorted(merged_words)))
            
            print(color.GREEN + f"\nMerged {len(merged_words)} unique words into {merged_filename}\n" + color.END)

if __name__ == "__main__":
    main()