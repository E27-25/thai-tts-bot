"""Thai TTS engine using edge-tts (Microsoft Edge Text-to-Speech)."""

import os
import uuid
import asyncio
import logging
from pathlib import Path

import edge_tts

from config import Config

logger = logging.getLogger(__name__)


class TTSEngine:
    """Async wrapper around edge-tts for Thai speech synthesis."""

    def __init__(self, voice: str | None = None):
        self.voice = voice or Config.DEFAULT_VOICE
        # Use absolute path so ffmpeg can always find the files
        script_dir = Path(__file__).parent.resolve()
        self.audio_dir = script_dir / Config.AUDIO_DIR
        self.audio_dir.mkdir(exist_ok=True)

    async def synthesize(self, text: str, voice: str | None = None) -> str:
        """
        Convert Thai text to speech audio file.

        Args:
            text: Thai text to synthesize.
            voice: Optional voice name override.

        Returns:
            Path to the generated .mp3 file.
        """
        use_voice = voice or self.voice
        filename = f"tts_{uuid.uuid4().hex[:8]}.mp3"
        filepath = str(self.audio_dir / filename)

        logger.info(f"Synthesizing: '{text[:50]}...' with voice={use_voice}")

        try:
            communicate = edge_tts.Communicate(text, use_voice)
            await communicate.save(filepath)
            logger.info(f"Audio saved to {filepath}")
            return filepath
        except Exception as e:
            logger.warning(f"Failed with {use_voice}: {e}. Retrying with fallback voice...")
            
            # Fallback logic if the primary voice fails (some voices fail on mixed Thai/English words)
            fallback_voice = "th-TH-NiwatNeural" if use_voice != "th-TH-NiwatNeural" else "th-TH-PremwadeeNeural"
            try:
                communicate = edge_tts.Communicate(text, fallback_voice)
                await communicate.save(filepath)
                logger.info(f"Fallback Audio saved to {filepath} using {fallback_voice}")
                return filepath
            except Exception as fallback_e:
                logger.error(f"Fallback also failed: {fallback_e}")
                raise e # Raise the original error

    def cleanup(self, filepath: str) -> None:
        """Delete a generated audio file."""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.debug(f"Cleaned up {filepath}")
        except OSError as e:
            logger.warning(f"Failed to clean up {filepath}: {e}")

    def cleanup_all(self) -> None:
        """Delete all cached audio files."""
        if self.audio_dir.exists():
            for f in self.audio_dir.glob("tts_*.mp3"):
                try:
                    f.unlink()
                except OSError:
                    pass
            logger.info("Cleaned up all cached audio files")

    def set_voice(self, voice_key: str) -> str | None:
        """
        Set the voice by key name.

        Args:
            voice_key: Short name like 'premwadee', 'niwat', 'achara'.

        Returns:
            The full voice name if found, None otherwise.
        """
        voice_key = voice_key.lower().strip()
        if voice_key in Config.THAI_VOICES:
            self.voice = Config.THAI_VOICES[voice_key]
            logger.info(f"Voice changed to {self.voice}")
            return self.voice
        return None

    @staticmethod
    async def list_thai_voices() -> list[dict[str, str]]:
        """List all available Thai voices from edge-tts."""
        voices = await edge_tts.list_voices()
        thai_voices = [v for v in voices if v["Locale"].startswith("th-TH")]
        return thai_voices
