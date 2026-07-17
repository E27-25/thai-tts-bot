"""Ollama integration for Thai chat responses."""

import logging

import aiohttp

from config import Config

logger = logging.getLogger(__name__)


class OllamaChat:
    """Async client for Ollama's generate API."""

    def __init__(self, model: str | None = None, base_url: str | None = None):
        self.model = model or Config.OLLAMA_MODEL
        self.base_url = (base_url or Config.OLLAMA_URL).rstrip("/")
        self.system_prompt = Config.SYSTEM_PROMPT

    async def generate(self, prompt: str) -> str:
        """
        Send a prompt to Ollama and get a Thai response.

        Args:
            prompt: User's message in Thai (or any language).

        Returns:
            Generated text response from the model.

        Raises:
            ConnectionError: If Ollama is not running.
            RuntimeError: If the API returns an error.
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": self.system_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 256,  # Keep responses short for TTS
            },
        }

        logger.info(f"Sending to Ollama ({self.model}): '{prompt[:50]}...'")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=60)) as resp:
                    if resp.status != 200:
                        error_text = await resp.text()
                        raise RuntimeError(
                            f"Ollama API error (HTTP {resp.status}): {error_text}"
                        )
                    data = await resp.json()
                    response_text = data.get("response", "").strip()
                    logger.info(f"Ollama response: '{response_text[:80]}...'")
                    return response_text

        except aiohttp.ClientConnectorError:
            raise ConnectionError(
                f"ไม่สามารถเชื่อมต่อกับ Ollama ได้ที่ {self.base_url}\n"
                f"กรุณาตรวจสอบว่า Ollama กำลังทำงานอยู่ (ollama serve)"
            )

    async def is_available(self) -> bool:
        """Check if Ollama is running and the model is available."""
        try:
            async with aiohttp.ClientSession() as session:
                # Check if Ollama is running
                async with session.get(
                    f"{self.base_url}/api/tags",
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as resp:
                    if resp.status != 200:
                        return False
                    data = await resp.json()
                    models = [m["name"] for m in data.get("models", [])]
                    # Check if model name matches (with or without :latest tag)
                    model_available = any(
                        m == self.model or m.startswith(f"{self.model}:")
                        for m in models
                    )
                    if not model_available:
                        logger.warning(
                            f"Model '{self.model}' not found. "
                            f"Available: {models}. "
                            f"Run: ollama pull {self.model}"
                        )
                    return model_available
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return False
