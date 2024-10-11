from crewai_tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from elevenlabs_s3 import VoiceSettings, text_to_speech
import os

class ElevenLabsTTSToolSchema(BaseModel):
    text: str = Field(..., description="The text to convert to speech.")
    elevenlabs_voice_id: str = Field(..., description="The ElevenLabs voice ID to use for TTS.")

class ElevenLabsTTSTool(BaseTool):
    name: str = "ElevenLabs TTS Tool"
    description: str = "Converts text to speech using ElevenLabs TTS and uploads to AWS S3."
    args_schema: Type[BaseModel] = ElevenLabsTTSToolSchema

    def _run(self, text: str, elevenlabs_voice_id: str, **kwargs):
        result = text_to_speech(
            text=text,
            elevenlabs_api_key=os.environ.get("ELEVENLABS_API_KEY"),
            output_folder="audio_files",
            aws_s3_bucket_name=os.environ.get("AWS_S3_BUCKET_NAME"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            aws_region_name=os.environ.get("AWS_REGION_NAME"),
            voice_id=elevenlabs_voice_id,
            voice_settings=VoiceSettings(
                stability=0.1,
                similarity_boost=0.3,
                style=0.2,
            )
        )
        return result
