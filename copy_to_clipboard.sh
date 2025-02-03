#!/bin/bash

# Check if the folder argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <folder>"
  exit 1
fi

FOLDER=$1

# Check if the provided argument is a valid directory
if [ ! -d "$FOLDER" ]; then
  echo "Error: $FOLDER is not a valid directory."
  exit 1
fi

# Create a temporary file to store the contents
TMP_FILE=$(mktemp)

# Function to process files recursively
process_files() {
  local dir="$1"
  local rel_path="${2:-}"
  for item in "$dir"/*; do
    if [ -f "$item" ]; then
      # Exclude specific files
      if [[ "$(basename "$item")" != "copy_to_clipboard.sh" && "$(basename "$item")" != "__init__.py" ]]; then
        local file_path="$rel_path$(basename "$item")"
        echo "### File: $file_path" >> "$TMP_FILE"
        echo "" >> "$TMP_FILE"
        cat "$item" >> "$TMP_FILE"
        echo "" >> "$TMP_FILE"
        echo "### End of file: $file_path" >> "$TMP_FILE"
        echo "" >> "$TMP_FILE"
        echo "" >> "$TMP_FILE"
      fi
    elif [ -d "$item" ]; then
      # Process subdirectories, excluding 'app' and 'static'
      if [[ "$(basename "$item")" != "app" && "$(basename "$item")" != "static" ]]; then
        process_files "$item" "$rel_path$(basename "$item")/"
      fi
    fi
  done
}

# Start processing files from the given folder
process_files "$FOLDER"

# Copy the contents of the temporary file to the clipboard
if command -v xclip &> /dev/null; then
  cat "$TMP_FILE" | xclip -selection clipboard
elif command -v pbcopy &> /dev/null; then
  cat "$TMP_FILE" | pbcopy
else
  echo "Error: No clipboard utility found. Please install xclip or pbcopy."
  rm "$TMP_FILE"
  exit 1
fi

# Clean up
rm "$TMP_FILE"

echo "Contents of files in $FOLDER (excluding specified files and folders) have been copied to the clipboard with filenames."