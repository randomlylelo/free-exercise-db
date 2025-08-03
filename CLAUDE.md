# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Free Exercise DB - an open public domain exercise dataset with 800+ exercises in JSON format. The project is focused on data processing and includes:
- Individual JSON files for each exercise (in `/exercises/`)
- Exercise images organized by exercise ID  
- Build scripts for combining and processing exercise data
- Schema validation for data consistency

## Common Development Commands

### Data Processing & Validation
```bash
# Lint all JSON files against schema
make lint

# Check for duplicate exercise IDs
make check_dupes

# Combine all individual JSON files into single file
make dist/exercises.json

# Create newline-delimited JSON for PostgreSQL import
make dist/exercises.nd.json

# Convert to CSV format
make dist/exercises.csv
```

### Dependencies
- `jq` - Required for JSON processing (install with `brew install jq` on macOS)
- `check-jsonschema` - For schema validation (install with `pip install check-jsonschema`)
- `csvkit` - For CSV conversion (optional)

## Architecture & Key Concepts

### Exercise Data Structure
Each exercise is a separate JSON file in `/exercises/` that conforms to the schema defined in `schema.json`. Key fields include:
- `id`: Unique identifier (matches filename)
- `name`: Human-readable exercise name
- `force`: Type of force (pull/push/static) - can be null
- `level`: Difficulty (beginner/intermediate/expert)
- `mechanic`: Movement type (isolation/compound) - can be null
- `equipment`: Required equipment - can be null
- `primaryMuscles` & `secondaryMuscles`: Arrays of muscle groups
- `instructions`: Array of instruction steps
- `category`: Exercise category (strength/cardio/stretching/etc)
- `images`: Array of relative image paths

### Image Organization
- Images stored in `/exercises/{exercise_id}/` directories
- Named sequentially: `0.jpg`, `1.jpg`, etc.
- Can be accessed via GitHub raw URLs for remote usage

### Data Processing Pipeline
1. Individual JSON files are source of truth
2. `make dist/exercises.json` combines them into single file
3. Schema validation ensures data consistency
4. Multiple output formats supported (JSON, NDJSON, CSV)

## Development Workflow

When modifying exercise data:
1. Edit individual JSON files in `/exercises/`
2. Run `make lint` to validate against schema
3. Run `make check_dupes` to ensure no duplicate IDs
4. Run `make dist/exercises.json` to rebuild combined file

## Useful Implementation Notes

### Search Implementation
If implementing search functionality, the following fields work well for text search:
- `id` - exercise ID
- `name` - exercise name
- `instructions` - exercise instructions (array of strings)

### Data Processing Tips
- The combined `dist/exercises.json` file is an array of all exercise objects
- Each exercise object is self-contained with all necessary data
- Images can be referenced by prepending `https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/` to the image paths

## Important Notes

- Some fields (force, mechanic, equipment) can be null due to incomplete data
- Images can be dynamically resized using services like imagekit.io
- There are ~25 duplicate images that could be consolidated
- The schema allows for future extensibility while maintaining backward compatibility