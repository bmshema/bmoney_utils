#!/bin/bash
# Checks for updated appimages downloaded from an application and updates the desktop shortcut file

# Define the path to the AppImage and the desktop shortcut file
APPIMAGE_DIR="/home/location/to/your_appimage"
DESKTOP_FILE="/usr/share/applications/<your_program>.desktop"

# Find the latest AppImage by sorting them by version and taking the latest
latest_appimage=$(ls -1v $APPIMAGE_DIR/cursor-*.AppImage | tail -n 1)

# Extract the full path of the latest AppImage
latest_exec_path=$(echo $latest_appimage)

# Check if we need to update the desktop file
current_exec_path=$(grep 'Exec=' $DESKTOP_FILE | cut -d '=' -f 2-)

if [ "$latest_exec_path" != "$current_exec_path" ]; then
  # Update the desktop file
  sudo sed -i "s|Exec=.*|Exec=$latest_exec_path|" $DESKTOP_FILE
  echo "$(date '+%Y-%m-%d %H:%M:%S') Updated cursor.desktop to use latest AppImage: $latest_exec_path" >> /var/log/cron.logs
else
  echo "$(date '+%Y-%m-%d %H:%M:%S') No update needed. The latest AppImage is already in use." >> /var/log/cron.logs
fi

# Cron job for once daily at 0300
# sudo crontab -e
# 0 3 * * * /home/path/to/your/appimage_updater.sh >> /var/log/cron.logs
