#!/usr/bin/env python
import json
import os
import sys
from honey.crew import HoneyCrew

def run():
    # Collect user inputs
    language = input("Enter the language (default is English): ").strip() or 'English'
    voice_gender = input("Enter the voice gender (male/female, default is female): ").strip().lower() or 'female'
    user_name = input("Enter your name (optional): ").strip() or None
    user_gender = input("Enter your gender (male/female, optional): ").strip().lower() or None
    category = input("Enter the category (e.g., support, motivation, consolation): ").strip() or None

    # Check if language and voice exist in the database
    database_file = 'db.json'
    if not os.path.exists(database_file):
        # Initialize database with default values
        db = {
            "languages": [
                {
                    "name": "English",
                    "code": "en"
                }
            ],
            "voices": [
                {
                    "name": "Alice",
                    "elevenlabs_voice_id": "YOUR_FEMALE_VOICE_ID",
                    "gender": "female",
                    "language_id": 0
                },
                {
                    "name": "Alex",
                    "elevenlabs_voice_id": "YOUR_MALE_VOICE_ID",
                    "gender": "male",
                    "language_id": 0
                }
            ],
            "names": [],
            "categories": [],
            "tts": []
        }
        with open(database_file, 'w') as f:
            json.dump(db, f, indent=4)
    else:
        with open(database_file, 'r') as f:
            db = json.load(f)

    # Check if language exists
    language_entry = next((d for d in db['languages'] if d["name"].lower() == language.lower()), None)
    if language_entry is None:
        print(f"Error: Language '{language}' not found in the database.")
        sys.exit(1)
    language_id = db['languages'].index(language_entry)

    # Check if voice exists
    voice_entry = next(
        (d for d in db['voices'] if d["gender"].lower() == voice_gender.lower() and d["language_id"] == language_id),
        None
    )
    if voice_entry is None:
        print(f"Error: Voice with gender '{voice_gender}' in language '{language}' not found in the database.")
        sys.exit(1)

    # Add voice and language IDs to inputs
    inputs = {
        'language': language,
        'language_id': language_id,
        'voice_gender': voice_gender,
        'voice_id': db['voices'].index(voice_entry),
        'elevenlabs_voice_id': voice_entry['elevenlabs_voice_id'],
        'user_name': user_name,
        'user_gender': user_gender,
        'category': category,
    }

    result = HoneyCrew().crew().kickoff(inputs=inputs)
    print("\n\n########################")
    print("## Here is the Result")
    print("########################\n")
    print(result)

if __name__ == "__main__":
    run()
