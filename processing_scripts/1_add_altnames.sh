#!/bin/bash

# Script to add altNames field to all exercise JSON files

EXERCISES_DIR="exercises"
BACKUP_DIR="exercises_backup"

# Create backup directory
echo "Creating backup directory..."
mkdir -p "$BACKUP_DIR"

# Function to add altNames field to a JSON file
add_altnames() {
    local file="$1"
    local filename=$(basename "$file")
    
    # Check if altNames already exists
    if jq -e '.altNames' "$file" > /dev/null 2>&1; then
        echo "  ✓ altNames already exists in $filename"
        return 0
    fi
    
    # Add altNames field as empty array
    jq '. + {"altNames": []}' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
    
    if [ $? -eq 0 ]; then
        echo "  ✓ Added altNames to $filename"
    else
        echo "  ✗ Failed to update $filename"
        return 1
    fi
}

# Count total files
total_files=$(find "$EXERCISES_DIR" -name "*.json" -type f | wc -l)
echo "Found $total_files exercise JSON files"

# Backup all JSON files first
echo "Creating backup of all exercise files..."
cp -r "$EXERCISES_DIR"/*.json "$BACKUP_DIR"/ 2>/dev/null

# Process all JSON files
echo "Adding altNames field to exercise files..."
count=0
failed=0

for json_file in "$EXERCISES_DIR"/*.json; do
    if [ -f "$json_file" ]; then
        add_altnames "$json_file"
        if [ $? -eq 0 ]; then
            ((count++))
        else
            ((failed++))
        fi
    fi
done

echo ""
echo "Summary:"
echo "  Total files processed: $total_files"
echo "  Successfully updated: $count"
echo "  Failed: $failed"
echo "  Backup created in: $BACKUP_DIR"

# Offer to validate against schema
echo ""
echo "To validate the updated files against the schema, run:"
echo "  make lint"