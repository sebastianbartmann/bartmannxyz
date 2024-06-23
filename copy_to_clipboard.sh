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

# Concatenate the contents of all files in the folder to the temporary file
for file in "$FOLDER"/*; do
  if [ -f "$file" ]; then
    cat "$file" >> "$TMP_FILE"
    echo "" >> "$TMP_FILE"  # Add a newline between files for clarity
  fi
done

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

echo "Contents of all files in $FOLDER have been copied to the clipboard."
