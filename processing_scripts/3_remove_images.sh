#!/bin/bash

# Script to remove the "images" field from all exercise JSON files

EXERCISES_DIR="exercises"
BACKUP_DIR="exercises_backup_images"

# Create backup directory
echo "Creating backup directory..."
mkdir -p "$BACKUP_DIR"

# Function to remove images field from a JSON file
remove_images() {
    local file="$1"
    local filename=$(basename "$file")
    
    # Check if images field exists
    if ! jq -e '.images' "$file" > /dev/null 2>&1; then
        echo "  - No images field in $filename"
        return 0
    fi
    
    # Remove images field
    jq 'del(.images)' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
    
    if [ $? -eq 0 ]; then
        echo "  ✓ Removed images from $filename"
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
echo "Removing images field from exercise files..."
count=0
failed=0
skipped=0

for json_file in "$EXERCISES_DIR"/*.json; do
    if [ -f "$json_file" ]; then
        remove_images "$json_file"
        result=$?
        if [ $result -eq 0 ]; then
            if jq -e '.images' "$json_file" > /dev/null 2>&1; then
                ((skipped++))
            else
                ((count++))
            fi
        else
            ((failed++))
        fi
    fi
done

echo ""
echo "Summary:"
echo "  Total files processed: $total_files"
echo "  Successfully removed images: $count"
echo "  Files without images field: $skipped"
echo "  Failed: $failed"
echo "  Backup created in: $BACKUP_DIR"

# Offer to validate against schema
echo ""
echo "To validate the updated files against the schema, run:"
echo "  make lint"