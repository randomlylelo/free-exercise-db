#!/bin/bash

# Script to reorder JSON fields to place altNames after name

EXERCISES_DIR="exercises"

# Function to reorder fields in a JSON file
reorder_json() {
    local file="$1"
    local filename=$(basename "$file")
    
    # Use jq to reorder fields with altNames after name
    jq '{
        name: .name,
        altNames: .altNames,
        force: .force,
        level: .level,
        mechanic: .mechanic,
        equipment: .equipment,
        primaryMuscles: .primaryMuscles,
        secondaryMuscles: .secondaryMuscles,
        instructions: .instructions,
        category: .category,
        images: .images,
        id: .id
    }' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
    
    if [ $? -eq 0 ]; then
        echo "  ✓ Reordered fields in $filename"
    else
        echo "  ✗ Failed to reorder $filename"
        return 1
    fi
}

# Count total files
total_files=$(find "$EXERCISES_DIR" -name "*.json" -type f | wc -l)
echo "Found $total_files exercise JSON files"

# Process all JSON files
echo "Reordering fields in exercise files..."
count=0
failed=0

for json_file in "$EXERCISES_DIR"/*.json; do
    if [ -f "$json_file" ]; then
        reorder_json "$json_file"
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
echo "  Successfully reordered: $count"
echo "  Failed: $failed"