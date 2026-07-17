"""YouTube music extraction using yt-dlp."""

import asyncio
import logging
import yt_dlp

logger = logging.getLogger(__name__)

# yt-dlp options for best audio extraction without downloading the video
YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "extractaudio": True,
    "audioformat": "mp3",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

class MusicEngine:
    @staticmethod
    async def extract_info(query: str) -> dict | None:
        """
        Extract video information and stream URL using yt-dlp.
        
        Args:
            query: YouTube URL or search query.
            
        Returns:
            A dictionary containing video data, or None if extraction fails.
        """
        # If it's not a URL, make it a search query
        if not query.startswith("http"):
            query = f"ytsearch:{query}"

        try:
            # Run in executor to prevent blocking the event loop
            data = await asyncio.to_thread(ytdl.extract_info, query, download=False)
        except Exception as e:
            logger.error(f"yt-dlp extraction error for query '{query}': {e}")
            return None

        if "entries" in data:
            # Take first item from a playlist/search
            data = data["entries"][0]

        return {
            "url": data.get("url"),
            "title": data.get("title"),
            "webpage_url": data.get("webpage_url"),
            "duration": data.get("duration"),
        }
