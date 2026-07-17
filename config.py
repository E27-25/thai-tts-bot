"""Configuration management for Thai TTS Discord Bot."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Bot configuration loaded from environment variables."""

    # Discord
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")
    COMMAND_PREFIX: str = os.getenv("COMMAND_PREFIX", "!")

    # Ollama
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")

    # TTS
    DEFAULT_VOICE: str = os.getenv("DEFAULT_VOICE", "th-TH-PremwadeeNeural")

    # Available Thai voices from edge-tts
    THAI_VOICES: dict[str, str] = {
        "premwadee": "th-TH-PremwadeeNeural",  # Female
        "niwat": "th-TH-NiwatNeural",          # Male
        "achara": "th-TH-AcharaNeural",         # Female
    }

    # System prompt for Ollama (instructs the model to respond in Thai)
    SYSTEM_PROMPT: str = os.getenv(
        "SYSTEM_PROMPT",
        "คุณเป็นผู้ช่วย AI ที่ตอบเป็นภาษาไทยเสมอ ตอบสั้นกระชับไม่เกิน 2-3 ประโยค "
        "เพราะคำตอบจะถูกแปลงเป็นเสียงพูด อย่าใช้ emoji หรือสัญลักษณ์พิเศษ"
    )

    # Audio
    AUDIO_DIR: str = os.getenv("AUDIO_DIR", "audio_cache")
    MAX_TEXT_LENGTH: int = int(os.getenv("MAX_TEXT_LENGTH", "500"))

    @classmethod
    def validate(cls) -> list[str]:
        """Validate required configuration. Returns list of errors."""
        errors = []
        if not cls.DISCORD_TOKEN:
            errors.append("DISCORD_TOKEN is not set. Create a .env file with your bot token.")
        return errors
