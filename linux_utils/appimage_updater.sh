#!/bin/bash
# Checks for updated appimages downloaded from an application and updates the desktop shortcut file

# Define the path to the AppImage and the desktop shortcut file
APPIMAGE_DIR="/home/location/to/your_appimage"
DESKTOP_FILE="/usr/share/applications/<your_program>.desktop"
# Extract the shortcut filename for logging
APP_FILE=$(basename "$DESKTOP_FILE")

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1" >> /var/log/cron.logs
}

# Find the latest AppImage by sorting them by version and taking the latest
latest_appimage=$(ls -1v $APPIMAGE_DIR/*.AppImage | tail -n 1)

# Extract the full path of the latest AppImage
latest_exec_path=$(echo $latest_appimage)

# Check if we need to update the desktop file
current_exec_path=$(grep 'Exec=' $DESKTOP_FILE | cut -d '=' -f 2-)

log_message "Checking for updates to $APP_FILE"
log_message "Current AppImage: $current_exec_path"
log_message "Latest AppImage: $latest_exec_path"

if [ "$latest_exec_path" != "$current_exec_path" ]; then
    # Update the desktop file
    if sudo sed -i "s|Exec=.*|Exec=$latest_exec_path|" $DESKTOP_FILE; then
        log_message "Successfully updated $APP_FILE to use latest AppImage: $latest_exec_path"
    else
        log_message "Failed to update $APP_FILE. Error occurred."
    fi
  
    # Verification step
    if grep -q "Exec=$latest_exec_path" $DESKTOP_FILE; then
        log_message "Verified: $APP_FILE now uses the latest AppImage."
    else
        log_message "Warning: $APP_FILE update could not be verified."
    fi
else
    log_message "No update needed for $APP_FILE. The latest AppImage is already in use."
fi

# Cron job for once daily at 0300
# sudo crontab -e
# 0 3 * * * /home/path/to/your/appimage_updater.sh >> /var/log/cron.logs
