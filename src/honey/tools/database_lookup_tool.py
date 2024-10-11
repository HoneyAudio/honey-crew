from crewai_tools import BaseTool
import json
import os

class DatabaseLookupTool(BaseTool):
    name: str = "Database Lookup Tool"
    description: str = "Looks up the database to check if a voice with the specified gender and language exists. Returns the voice IDs if exists."

    def _run(self, voice_gender: str, language: str, database_file: str = 'db.json', **kwargs):
        # data should be a dictionary containing all necessary info
        if not os.path.exists(database_file) or os.path.getsize(database_file) == 0:
            # Initialize with default data if file doesn't exist or is empty
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
                        "elevenlabs_voice_id": "K8lgMMdmFr7QoEooafEf",
                        "gender": "female",
                        "language_id": 0
                    },
                    {
                        "name": "Alex",
                        "elevenlabs_voice_id": "UvSWlWKwkwKAshx25ieK",
                        "gender": "male",
                        "language_id": 0
                    }
                ],
                "names": [],
                "categories": [],
                "tts": []
            }
        else:
            with open(database_file, 'r') as f:
                db = json.load(f)
        
        # Find the language
        language_entry = next((d for d in db['languages'] if d["name"].lower() == language.lower()), None)
        if language_entry is None:
            return {"error": f"Voice with gender '{voice_gender}' in language '{language}' not available."}

        language_id = db['languages'].index(language_entry)

        # Find the voice
        voice_entry = next((d for d in db['voices'] if d["gender"].lower() == voice_gender.lower() and d["language_id"] == language_id), None)
        if voice_entry is None:
            return {"error": f"Voice with gender '{voice_gender}' in language '{language}' not available."}

        voice_id = db['voices'].index(voice_entry)
        elevenlabs_voice_id = voice_entry['elevenlabs_voice_id']

        return {
            'voice_id': voice_id,
            'elevenlabs_voice_id': elevenlabs_voice_id,
            'language_id': language_id
        }
