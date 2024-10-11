from crewai_tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type
import json
import os

class DatabaseUpdateToolSchema(BaseModel):
    data: dict = Field(..., description="A dictionary containing all necessary information to update the database.")
    database_file: str = Field(default='db.json', description="Path to the database JSON file.")
    texts_file: str = Field(default='texts.json', description="Path to the texts JSON file.")

class DatabaseUpdateTool(BaseTool):
    name: str = "Database Update Tool"
    description: str = "Updates the JSON database with new entry, adhering to the specified structure, and saves texts separately."
    args_schema: Type[BaseModel] = DatabaseUpdateToolSchema

    def _run(self, data: dict, database_file: str = 'db.json', texts_file: str = 'texts.json', **kwargs):
        # data should be a dictionary containing all necessary info

        # Load existing database
        if not os.path.exists(database_file):
            return "Error: Database file does not exist."

        with open(database_file, 'r') as f:
            db = json.load(f)

        # Handle language
        language_id = data['language_id']

        # Handle voice
        voice_id = data['voice_id']

        # Handle name
        user_name = data.get('user_name')
        name_id = None
        if user_name:
            name_id = next(
                (index for (index, d) in enumerate(db['names']) if d["name"].lower() == user_name.lower()
                 and d["language_id"] == language_id),
                None
            )
            if name_id is None:
                name_id = len(db['names'])
                user_gender = data.get('user_gender', 'unknown')
                db['names'].append({
                    "name": user_name,
                    "gender": user_gender,
                    "language_id": language_id
                })

        # Handle category
        category_name = data['category']
        category_id = next(
            (index for (index, d) in enumerate(db['categories']) if d["name"].lower() == category_name.lower()
             and d["language_id"] == language_id),
            None
        )
        if category_id is None:
            category_id = len(db['categories'])
            db['categories'].append({
                "name": category_name,
                "language_id": language_id
            })

        # Handle TTS entry
        tts_entry = {
            "voice_id": voice_id,
            "category_id": category_id,
            "name_id": name_id,
            "language_id": language_id,
            "audio_file": data['tts_result']['s3_file_name'],
            "symbols": len(data['generated_text'])
        }
        tts_id = len(db['tts'])
        db['tts'].append(tts_entry)

        # Save database
        with open(database_file, 'w') as f:
            json.dump(db, f, indent=4)

        # Save text in texts.json
        if not os.path.exists(texts_file):
            texts_db = {}
        else:
            with open(texts_file, 'r') as f:
                texts_db = json.load(f)

        texts_db[str(tts_id)] = data['generated_text']

        with open(texts_file, 'w') as f:
            json.dump(texts_db, f, indent=4)

        return "Database and texts updated successfully."
