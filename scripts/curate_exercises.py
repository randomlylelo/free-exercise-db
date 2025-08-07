#!/usr/bin/env python3
"""
Final exercise curation script - targets 200-250 exercises for beginners
Keeps equipment variations but removes overly complex exercises
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

class ExerciseCurator:
    def __init__(self):
        # Use relative paths since script is now in free-exercise-db/scripts/
        script_dir = Path(__file__).parent
        self.input_dir = script_dir.parent / 'exercises'
        self.output_dir = script_dir.parent / 'dist'
        self.exercises = []
        
    def load_exercises(self):
        """Load all exercises from JSON files"""
        for file_path in self.input_dir.glob('*.json'):
            try:
                with open(file_path, 'r') as f:
                    exercise = json.load(f)
                    self.exercises.append(exercise)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
    
    def should_exclude(self, exercise: Dict) -> bool:
        """Determine if an exercise should be excluded"""
        name = exercise.get('name', '').lower()
        
        # Exclude expert level exercises
        if exercise.get('level') == 'expert':
            return True
        
        # Exclude non-strength/cardio/stretching categories
        category = exercise.get('category', '')
        if category not in ['strength', 'cardio', 'stretching', 'plyometrics']:
            return True
        
        # Exclude powerlifting/olympic/strongman specific
        exclude_patterns = [
            'powerlifting', 'olympic', 'strongman',
            'snatch', 'clean and jerk', 'clean and press',
            'muscle up', 'handstand', 'human flag',
            'pistol', 'bulgarian split', 'nordic',
            'glute ham raise', 'zercher', 'jefferson',
            'sumo deadlift', 'deficit deadlift',
            'with chains', 'with bands', 'band assisted',
            'sled', 'prowler', 'farmers walk', 'yoke',
            'atlas stone', 'tire flip', 'battle rope',
            'sledgehammer', 'sandbag', 'log press',
            'behind the neck', 'behind neck', 'guillotine',
            'jerk', 'hang clean', 'hang snatch',
            'kipping', 'butterfly pull',
            'scorpion', 'turkish get', 'windmill'
        ]
        
        for pattern in exclude_patterns:
            if pattern in name:
                return True
        
        # Exclude overly specific equipment
        equipment = exercise.get('equipment', '')
        if equipment in ['other', 'n/a']:
            # Check if it's a basic bodyweight exercise
            if 'body only' not in str(exercise.get('equipment', '')).lower():
                return True
        
        return False
    
    def simplify_name(self, exercise: Dict) -> str:
        """Simplify exercise name while keeping equipment info"""
        name = exercise.get('name', '')
        equipment = exercise.get('equipment', '')
        
        # Remove specific grip widths
        name = re.sub(r' - Medium Grip| - Wide Grip| - Close Grip', '', name)
        name = re.sub(r' Medium Grip| Wide Grip| Narrow Grip', '', name)
        
        # Keep Close-Grip as a distinct variation for triceps
        if 'Close-Grip' in name and 'tricep' in str(exercise.get('primaryMuscles', [])).lower():
            name = name  # Keep it
        elif 'Close Grip' in name or 'Close-Grip' in name:
            name = re.sub(r'Close[- ]Grip ', '', name)
        
        # Remove "With" phrases except important ones
        name = re.sub(r' With Bands| With Chains', '', name)
        name = re.sub(r' - With .*', '', name)
        
        # Standardize equipment naming
        equipment_map = {
            'barbell': 'Barbell',
            'dumbbell': 'Dumbbell',
            'cable': 'Cable',
            'machine': 'Machine',
            'kettlebells': 'Kettlebell',
            'e-z curl bar': 'EZ-Bar',
            'exercise ball': 'Exercise Ball',
            'medicine ball': 'Medicine Ball',
            'bands': 'Band'
        }
        
        # Add equipment prefix if not present
        if equipment and equipment != 'body only':
            eq_name = equipment_map.get(equipment, '')
            if eq_name and eq_name.lower() not in name.lower():
                # For standard exercises, add equipment prefix
                base_exercises = ['curl', 'press', 'row', 'squat', 'deadlift', 
                                'raise', 'extension', 'fly', 'pullover']
                if any(ex in name.lower() for ex in base_exercises):
                    name = f"{eq_name} {name}"
        
        # Clean up the name
        name = re.sub(r'\s+', ' ', name).strip()
        
        # Special case renamings for clarity
        renames = {
            'Barbell Bench Press': 'Barbell Bench Press',
            'Barbell Bench Press Medium': 'Barbell Bench Press',
            'Dumbbell Bench Press': 'Dumbbell Bench Press',
            'Barbell Curl': 'Barbell Curl',
            'Dumbbell Curl': 'Dumbbell Curl',
            'Alternate Dumbbell Curl': 'Dumbbell Curl',
            'Dumbbell Alternate Bicep Curl': 'Dumbbell Curl',
            'Barbell Squat': 'Barbell Back Squat',
            'Barbell Full Squat': 'Barbell Back Squat',
            'Front Barbell Squat': 'Barbell Front Squat',
            'Lying Leg Curls': 'Machine Lying Leg Curl',
            'Seated Leg Curl': 'Machine Seated Leg Curl',
            'Leg Extensions': 'Machine Leg Extension',
            'Lat Pulldown': 'Cable Lat Pulldown',
            'Wide Grip Lat Pulldown': 'Cable Lat Pulldown',
            'Close Grip Lat Pulldown': 'Cable Lat Pulldown',
            'Push Ups': 'Push-ups',
            'Pushups': 'Push-ups',
            'Pull Ups': 'Pull-ups',
            'Pullups': 'Pull-ups',
            'Chin Up': 'Chin-ups',
            'Chin-Up': 'Chin-ups'
        }
        
        for old, new in renames.items():
            if name == old or name.replace('-', ' ') == old:
                name = new
                break
        
        return name
    
    def deduplicate(self, exercises: List[Dict]) -> List[Dict]:
        """Remove duplicate exercises, keeping best version"""
        unique = {}
        
        for ex in exercises:
            # Create key from simplified name
            key = (ex['name'], ex.get('equipment', ''))
            
            if key not in unique:
                unique[key] = ex
            else:
                # Keep the one with better data
                current = unique[key]
                
                # Prefer beginner over intermediate
                if ex.get('level') == 'beginner' and current.get('level') != 'beginner':
                    unique[key] = ex
                # Prefer one with more instructions
                elif len(ex.get('instructions', [])) > len(current.get('instructions', [])):
                    unique[key] = ex
        
        return list(unique.values())
    
    def categorize_for_app(self, exercise: Dict) -> str:
        """Categorize exercise for the app"""
        primary_muscles = exercise.get('primaryMuscles', [])
        name = exercise.get('name', '').lower()
        
        # Map muscles to app categories
        if any(m in ['chest', 'pectorals'] for m in primary_muscles):
            return 'chest'
        elif any(m in ['lats', 'middle back', 'lower back', 'traps'] for m in primary_muscles):
            return 'back'
        elif any(m in ['shoulders', 'delts'] for m in primary_muscles):
            return 'shoulders'
        elif 'biceps' in primary_muscles:
            return 'biceps'
        elif 'triceps' in primary_muscles:
            return 'triceps'
        elif any(m in ['quadriceps', 'quads'] for m in primary_muscles):
            return 'legs_quad'
        elif 'hamstrings' in primary_muscles:
            return 'legs_hamstring'
        elif 'glutes' in primary_muscles:
            return 'legs_glute'
        elif 'calves' in primary_muscles:
            return 'legs_calf'
        elif any(m in ['abdominals', 'abs', 'obliques'] for m in primary_muscles):
            return 'core'
        elif 'forearms' in primary_muscles:
            return 'forearms'
        elif exercise.get('category') == 'cardio':
            return 'cardio'
        elif exercise.get('category') == 'stretching':
            return 'stretching'
        else:
            return 'other'
    
    def select_best_per_category(self, exercises: List[Dict]) -> List[Dict]:
        """Select best exercises per category with limits"""
        categorized = {}
        
        # Categorize all exercises
        for ex in exercises:
            cat = self.categorize_for_app(ex)
            if cat not in categorized:
                categorized[cat] = []
            categorized[cat].append(ex)
        
        # Target distribution (total ~220 exercises)
        limits = {
            'chest': 25,
            'back': 30,
            'shoulders': 20,
            'biceps': 15,
            'triceps': 15,
            'legs_quad': 25,
            'legs_hamstring': 15,
            'legs_glute': 10,
            'legs_calf': 8,
            'core': 25,
            'forearms': 5,
            'cardio': 10,
            'stretching': 15,
            'other': 5
        }
        
        selected = []
        
        for category, limit in limits.items():
            if category in categorized:
                cat_exercises = categorized[category]
                
                # Sort by priority
                cat_exercises.sort(key=lambda x: (
                    0 if x.get('level') == 'beginner' else 1,
                    0 if x.get('equipment') == 'body only' else 1,
                    0 if x.get('equipment') == 'dumbbell' else 2,
                    0 if x.get('equipment') == 'barbell' else 3,
                    len(x.get('name', ''))
                ))
                
                # Ensure variety of equipment
                equipment_count = {}
                for ex in cat_exercises[:limit * 2]:  # Look at more exercises
                    eq = ex.get('equipment', 'none')
                    if equipment_count.get(eq, 0) < limit // 3 + 2:
                        selected.append(ex)
                        equipment_count[eq] = equipment_count.get(eq, 0) + 1
                        
                        if len([e for e in selected if self.categorize_for_app(e) == category]) >= limit:
                            break
        
        return selected
    
    def curate(self):
        """Main curation process"""
        print("Loading exercises...")
        self.load_exercises()
        print(f"Loaded {len(self.exercises)} exercises")
        
        # Filter out excluded exercises
        filtered = []
        for ex in self.exercises:
            if not self.should_exclude(ex):
                # Simplify the name
                ex['original_name'] = ex['name']
                ex['name'] = self.simplify_name(ex)
                ex['app_category'] = self.categorize_for_app(ex)
                filtered.append(ex)
        
        print(f"After filtering: {len(filtered)} exercises")
        
        # Remove duplicates
        deduped = self.deduplicate(filtered)
        print(f"After deduplication: {len(deduped)} exercises")
        
        # Select best per category
        final = self.select_best_per_category(deduped)
        print(f"Final selection: {len(final)} exercises")
        
        # Sort by category and name
        final.sort(key=lambda x: (x.get('app_category', ''), x.get('name', '')))
        
        return final
    
    def save(self, exercises: List[Dict]):
        """Save curated exercises"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save main file
        output_file = self.output_dir / 'exercises.json'
        with open(output_file, 'w') as f:
            json.dump(exercises, f, indent=2)
        
        print(f"\nSaved {len(exercises)} exercises to {output_file}")
        
        # Save summary
        summary = {}
        for ex in exercises:
            cat = ex.get('app_category', 'other')
            if cat not in summary:
                summary[cat] = []
            summary[cat].append(f"{ex['name']} ({ex.get('equipment', 'none')})")
        
        print("\nCategory breakdown:")
        for cat in sorted(summary.keys()):
            print(f"  {cat}: {len(summary[cat])} exercises")
        
        # Save detailed summary
        with open(self.output_dir / 'summary.txt', 'w') as f:
            for cat in sorted(summary.keys()):
                f.write(f"\n{cat.upper()} ({len(summary[cat])} exercises)\n")
                f.write("-" * 50 + "\n")
                for name in sorted(summary[cat]):
                    f.write(f"  • {name}\n")


def main():
    curator = ExerciseCurator()
    exercises = curator.curate()
    curator.save(exercises)


if __name__ == '__main__':
    main()