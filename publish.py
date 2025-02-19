import os
import re
import asyncio
import json
import requests
import logging
from typing import Dict, List, Tuple
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            f'podcast_generation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        ),
    ],
)
logger = logging.getLogger(__name__)

# Get API key from environment variable
API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
BASE_URL = "https://api.elevenlabs.io/v1"

# Define voice settings for different roles
VOICE_SETTINGS = {
    "host": {
        "voice_id": "ThT5KcBeYPX3keUQqHPh",  # Josh voice
        "name": "Michael Sullivan",
        "model_id": "eleven_monolingual_v1",
        "settings": {
            "stability": 0.71,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True,
        },
    },
    "sound_effects": {
        "intro_music": "sfx_intro",
        "outro_music": "sfx_outro",
        "transition": "sfx_transition",
    },
}


async def parse_script(script_path: str) -> List[Dict]:
    """Parse the podcast script and extract segments with voice and emotion markers."""
    logger.info(f"Starting to parse script: {script_path}")
    segments = []

    with open(script_path, "r") as file:
        content = file.read()
        logger.debug(f"Read {len(content)} characters from script file")

    # Split into segments based on speaker changes and sound effects
    pattern = r"\[(.*?)\]|\w+:\s*\((.*?)\)(.*?)(?=\[|\w+:|$)"
    matches = re.finditer(pattern, content, re.DOTALL)

    for match in matches:
        if match.group(1):  # Sound effect/music marker
            segment = {
                "type": "sound_effect",
                "name": match.group(1).lower().replace(" ", "_"),
            }
            logger.debug(f"Found sound effect: {segment['name']}")
        elif match.group(2) and match.group(3):  # Voice line with emotion
            segment = {
                "type": "speech",
                "speaker": match.group(0).split(":")[0].strip(),
                "emotion": match.group(2).strip(),
                "text": match.group(3).strip(),
            }
            logger.debug(
                f"Found speech segment - Speaker: {segment['speaker']}, Emotion: {segment['emotion']}"
            )
        segments.append(segment)

    logger.info(f"Parsed {len(segments)} segments from script")
    return segments


async def generate_audio_segment(segment: Dict) -> bytes:
    """Generate audio for a single segment using ElevenLabs API."""
    if segment["type"] == "sound_effect":
        logger.debug(f"Skipping sound effect generation for: {segment['name']}")
        return b""

    logger.info(
        f"Generating audio for segment - Emotion: {segment.get('emotion', 'neutral')}"
    )
    logger.debug(f"Text to generate: {segment['text'][:50]}...")

    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}

    # Adjust settings based on emotion
    settings = VOICE_SETTINGS["host"]["settings"].copy()
    if "emotion" in segment:
        emotion_settings = {
            "cheerful": {"stability": 0.7, "similarity_boost": 0.8, "style": 0.3},
            "dramatic": {"stability": 0.6, "similarity_boost": 0.7, "style": 0.4},
            "excited": {"stability": 0.65, "similarity_boost": 0.85, "style": 0.5},
            "thoughtful": {"stability": 0.8, "similarity_boost": 0.6, "style": 0.2},
        }
        settings.update(emotion_settings.get(segment["emotion"].lower(), {}))
        logger.debug(f"Applied {segment['emotion']} voice settings")

    data = {
        "text": segment["text"],
        "model_id": VOICE_SETTINGS["host"]["model_id"],
        "voice_settings": settings,
    }

    try:
        logger.debug("Sending request to ElevenLabs API")
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: requests.post(
                f"{BASE_URL}/text-to-speech/{VOICE_SETTINGS['host']['voice_id']}",
                headers=headers,
                json=data,
            ),
        )

        if response.status_code == 200:
            audio_size = len(response.content)
            logger.info(f"Successfully generated audio segment ({audio_size} bytes)")
            return response.content
        else:
            logger.error(f"API Error: {response.status_code} - {response.text}")
            return b""

    except Exception as e:
        logger.error(f"Error generating audio for segment: {e}", exc_info=True)
        return b""


async def create_podcast(script_path: str, output_path: str):
    """Create a podcast from the script."""
    logger.info(f"Starting podcast creation from {script_path}")
    start_time = datetime.now()

    # Parse the script
    segments = await parse_script(script_path)

    # Generate audio for each segment
    full_audio = b""
    total_segments = len(segments)

    for i, segment in enumerate(segments, 1):
        logger.info(f"Processing segment {i}/{total_segments}")
        audio = await generate_audio_segment(segment)
        full_audio += audio

        # Add small pause between segments
        if segment["type"] == "speech":
            full_audio += b"\x00" * 4410  # 0.1s silence at 44.1kHz
            logger.debug("Added pause after speech segment")

    # Save the final audio
    if full_audio:
        with open(output_path, "wb") as f:
            f.write(full_audio)
        duration = datetime.now() - start_time
        logger.info(f"Podcast saved to {output_path}")
        logger.info(f"Total processing time: {duration}")
    else:
        logger.error("No audio was generated")


async def main():
    """Main function to handle script execution."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Create a podcast from a script using ElevenLabs API"
    )
    parser.add_argument("script_path", help="Path to the podcast script file")
    parser.add_argument(
        "--output",
        default="podcast_output.mp3",
        help="Output path for the generated podcast (default: podcast_output.mp3)",
    )

    args = parser.parse_args()

    if not API_KEY:
        raise ValueError("ELEVEN_LABS_API_KEY environment variable is not set")

    await create_podcast(args.script_path, args.output)


if __name__ == "__main__":
    asyncio.run(main())
