# bmoney_utils
...for stuff and things
## Linux Utils:
### appimage_updater.sh: 
Checks for updated AppImage files in a specified directory, updates the corresponding desktop shortcut file if a newer version is found, and logs the action. It's designed to be run as a daily cron job to keep the application up-to-date.<br />   
*This primarily applies to software that automatically downloads its own updated AppImages, but can still be used otherwise.*  
<br />
If using this with multiple apps, put this program in separate directories with each software's appimage.
#### Usage:
- Change these two variables to reflect file locations on your system
```bash
APPIMAGE_DIR="/home/location/to/your_appimage"
DESKTOP_FILE="/usr/share/applications/<your_program>.desktop"
``` 
- Add to cron table. Example for once daily at 0300
```bash
$ sudo crontab -e

0 3 * * * /home/path/to/your/appimage_updater.sh >> /var/log/cron.logs
```
## Passwords:
### make_words.py: 
Generates customizable wordlists for password-related tasks. It allows users to specify character sets, word lengths, and optional custom strings, then creates all possible combinations of these parameters.
### word_salad.py:
Processes input wordlists by splitting them smaller worlists and applying user-specified actions (reverse, randomize, or none) to each section, then saves the resulting wordlists as separate output files.
### psk_extract.py:
Extracts sequences of characters between 8 and 63 ASCII-encoded characters from input wordlist(s) and saved to new file.