# Exercise Database Curation

This directory contains scripts and tools to curate the exercise database for beginner-focused workout apps.

## Overview

The original database contains 873 exercises, which is overwhelming for beginners. Our curation process reduces this to ~200 carefully selected exercises while maintaining:

- Equipment variations (Barbell, Dumbbell, Cable, Machine, Bodyweight)
- Comprehensive muscle group coverage
- Beginner-safe exercise selection
- Clear, consistent naming

## Files

- **`scripts/curate_exercises.py`** - Main curation script
- **`dist/exercises.json`** - Curated exercise database (208 exercises)
- **`dist/summary.txt`** - Detailed breakdown by category

## Usage

```bash
# Run curation script (from free-exercise-db directory)
python3 scripts/curate_exercises.py

# Output will be generated in dist/ directory
```

## Curation Criteria

### ✅ Exercises We Keep
- Beginner and intermediate level exercises
- Core movement patterns for all major muscle groups
- Equipment variations that are commonly available
- Exercises with clear, comprehensive instructions

### ❌ Exercises We Remove
- Expert-level exercises
- Overly specific grip/stance variations
- Powerlifting/Olympic lifting specialized movements  
- Equipment requiring bands, chains, or specialty gear
- Complex alternating or single-arm variations
- Advanced techniques that could be dangerous for beginners

## Results

The curated database contains **208 exercises** across these categories:

- **Legs (Quads)**: 25 exercises
- **Back**: 30 exercises  
- **Chest**: 25 exercises
- **Core**: 24 exercises
- **Shoulders**: 20 exercises
- **Legs (Hamstring)**: 15 exercises
- **Biceps**: 15 exercises
- **Triceps**: 15 exercises
- **Legs (Glute)**: 10 exercises
- **Legs (Calf)**: 8 exercises
- **Stretching**: 11 exercises
- **Forearms**: 5 exercises
- **Other**: 5 exercises

## Integration

To use the curated exercises in your app, copy the generated file:

```bash
cp dist/exercises.json /path/to/your/app/Resources/Data/exercises.json
```

The curated exercises maintain the same JSON structure as the original database, ensuring compatibility with existing apps.