#!/bin/bash

# Directly set the environment variables
export DB_HOST=$(grep -E '^DB_HOST=' /mnt/c/Users/Karolis/Documents/Github\ repository/kmicku-DE2v2.2.5/kmicku-DE2v2.2.5/configs/.env | cut -d '=' -f2 | tr -d '\r\n')
export DB_PORT=$(grep -E '^DB_PORT=' /mnt/c/Users/Karolis/Documents/Github\ repository/kmicku-DE2v2.2.5/kmicku-DE2v2.2.5/configs/.env | cut -d '=' -f2 | tr -d '\r\n')
export DB_NAME=$(grep -E '^DB_NAME=' /mnt/c/Users/Karolis/Documents/Github\ repository/kmicku-DE2v2.2.5/kmicku-DE2v2.2.5/configs/.env | cut -d '=' -f2 | tr -d '\r\n')
export DB_USER=$(grep -E '^DB_USER=' /mnt/c/Users/Karolis/Documents/Github\ repository/kmicku-DE2v2.2.5/kmicku-DE2v2.2.5/configs/.env | cut -d '=' -f2 | tr -d '\r\n')
export DB_PASSWORD=$(grep -E '^DB_PASSWORD=' /mnt/c/Users/Karolis/Documents/Github\ repository/kmicku-DE2v2.2.5/kmicku-DE2v2.2.5/configs/.env | cut -d '=' -f2 | tr -d '\r\n')

# Set the directory where backups will be stored
BACKUP_DIR="/mnt/c/Users/Karolis/Documents/Github repository/kmicku-DE2v2.2.5/kmicku-DE2v2.2.5/backups"
LOG_FILE="$BACKUP_DIR/backup_log.txt"

# Ensure the log file is writable
touch "$LOG_FILE"
if [ $? -ne 0 ]; then
    echo "Error: Cannot write to log file $LOG_FILE. Check permissions." >&2
    exit 1
fi

# Ensure backup directory exists
if [ ! -d "$BACKUP_DIR" ]; then
    echo "$(date): Backup directory does not exist. Creating..." >> "$LOG_FILE"
    mkdir -p "$BACKUP_DIR"
fi

# Set the name for the backup file
BACKUP_FILE="db_backup_$(date +%Y%m%d%H%M%S).sql"

# Log start time
echo "$(date): Starting backup" >> "$LOG_FILE"

# Print environment variables for debugging
echo "DB_HOST='$DB_HOST'" >> "$LOG_FILE"
echo "DB_PORT='$DB_PORT'" >> "$LOG_FILE"
echo "DB_NAME='$DB_NAME'" >> "$LOG_FILE"
echo "DB_USER='$DB_USER'" >> "$LOG_FILE"
echo "DB_PASSWORD='$DB_PASSWORD'" >> "$LOG_FILE"

# Count the number of backup files
backup_count=$(ls -1q "$BACKUP_DIR"/db_backup_*.sql 2>/dev/null | wc -l)

# If there are 24 or more backups, delete the oldest one
if [ "$backup_count" -ge 24 ]; then
    oldest_backup=$(ls -tp "$BACKUP_DIR"/db_backup_*.sql | grep -v '/$' | tail -n 1)
    echo "$(date): Deleting oldest backup: $oldest_backup" >> "$LOG_FILE"
    rm "$oldest_backup"
fi

# Command to backup the database
echo "$(date): Running pg_dump..." >> "$LOG_FILE"
export PGPASSWORD="$DB_PASSWORD"
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -F p -f "$BACKUP_DIR/$BACKUP_FILE" "$DB_NAME" >> "$LOG_FILE" 2>&1

# Check if the backup was successful
if [ $? -eq 0 ]; then
    echo "$(date): Backup completed successfully. File: $BACKUP_FILE" >> "$LOG_FILE"
else
    echo "$(date): Backup failed" >> "$LOG_FILE"
    # Remove the failed backup file if it was created
    [ -f "$BACKUP_DIR/$BACKUP_FILE" ] && rm "$BACKUP_DIR/$BACKUP_FILE"
fi

# Log cleanup action
echo "$(date): Old backups cleaned up" >> "$LOG_FILE"
