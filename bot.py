"""
Thai TTS Discord Bot
====================
Discord bot that speaks Thai in voice channels.
Uses edge-tts for speech synthesis and Ollama for chat.

Commands:
    !join   - Join voice channel
    !leave  - Leave voice channel
    !speak  - Convert Thai text to speech
    !chat   - Chat with Ollama and speak the response
    !voice  - List or change Thai voice
    !stop   - Stop current audio
    !help_tts - Show help message
"""

import asyncio
import logging
import os
import sys

import discord
from discord.ext import commands

# Load opus library for voice support (required on macOS)
if not discord.opus.is_loaded():
    try:
        discord.opus.load_opus("/opt/homebrew/lib/libopus.dylib")
    except Exception:
        # Try common paths
        for path in ["/usr/local/lib/libopus.dylib", "libopus.so", "libopus.0.dylib"]:
            try:
                discord.opus.load_opus(path)
                break
            except Exception:
                continue

from config import Config
from tts_engine import TTSEngine
from ollama_chat import OllamaChat
from music_engine import MusicEngine
import re

# ── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(name)-16s │ %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("bot")

# ── Bot Setup ────────────────────────────────────────────────────────────────

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(
    command_prefix=Config.COMMAND_PREFIX,
    intents=intents,
    help_command=None,  # We define our own
)

# ── Shared State ─────────────────────────────────────────────────────────────

tts = TTSEngine()
ollama = OllamaChat()
audio_queue: asyncio.Queue[dict] = asyncio.Queue()


# ── Events ───────────────────────────────────────────────────────────────────


@bot.event
async def on_ready():
    """Called when the bot is ready."""
    logger.info(f"✅ Bot is ready: {bot.user} (ID: {bot.user.id})")
    logger.info(f"🔊 Default voice: {tts.voice}")
    logger.info(f"🤖 Ollama model: {ollama.model}")

    # Check Ollama availability
    if await ollama.is_available():
        logger.info(f"✅ Ollama is running with model '{ollama.model}'")
    else:
        logger.warning(
            f"⚠️  Ollama not available or model '{ollama.model}' not found. "
            f"!chat command won't work. Run: ollama pull {ollama.model}"
        )

    # Start the audio queue worker
    bot.loop.create_task(audio_queue_worker())


# ── Audio Queue Worker ───────────────────────────────────────────────────────


async def audio_queue_worker():
    """Process audio files from the queue sequentially."""
    while True:
        item = await audio_queue.get()
        ctx = item["ctx"]
        try:
            await _play_audio(item)
        except Exception as e:
            logger.error(f"Error playing audio: {e}")
            await ctx.send(f"❌ เล่นเสียงไม่ได้: {e}")
        finally:
            if item.get("type") == "tts" and "filepath" in item:
                tts.cleanup(item["filepath"])
            audio_queue.task_done()


async def _play_audio(item: dict):
    """Play an audio item in the voice channel."""
    ctx = item["ctx"]
    vc = ctx.voice_client
    if not vc or not vc.is_connected():
        await ctx.send("❌ บอทไม่ได้อยู่ในห้องเสียง ใช้คำสั่ง `!join` ก่อน")
        return

    # Wait if something is already playing
    while vc.is_playing():
        await asyncio.sleep(0.5)

    is_music = item.get("type") == "music"
    source_url = item.get("url") if is_music else item.get("filepath")

    if not is_music and not os.path.exists(source_url):
        logger.error(f"Audio file not found: {source_url}")
        await ctx.send("❌ ไม่พบไฟล์เสียง")
        return

    logger.info(f"▶️  Playing: {item.get('display_text')}")

    # Set up FFmpeg options
    ffmpeg_before = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5" if is_music else "-nostdin"
    
    # Add start time and duration if provided
    start = item.get("start")
    duration = item.get("duration")
    
    if start:
        ffmpeg_before += f" -ss {start}"
    
    ffmpeg_options = "-vn -loglevel warning"
    if duration:
        ffmpeg_options += f" -t {duration}"

    ffmpeg_opts = {
        "before_options": ffmpeg_before,
        "options": ffmpeg_options,
    }

    try:
        source = discord.FFmpegPCMAudio(source_url, **ffmpeg_opts)
        source = discord.PCMVolumeTransformer(source, volume=0.5 if is_music else 2.0)
    except Exception as e:
        logger.error(f"Failed to create audio source: {e}", exc_info=True)
        await ctx.send(f"❌ สร้างแหล่งเสียงไม่ได้: {e}")
        return

    play_done = asyncio.Event()
    play_error: list[Exception] = []

    def after_play(error):
        if error:
            play_error.append(error)
            logger.error(f"Playback error: {error}")
        bot.loop.call_soon_threadsafe(play_done.set)

    try:
        vc.play(source, after=after_play)
        
        now_playing = f"🎶 **กำลังเล่น:** {item['display_text']}" if is_music else None
        if now_playing:
            await ctx.send(now_playing)
            
        logger.info(f"▶️  Now playing: '{item['display_text'][:40]}...'")
        await play_done.wait()

        if play_error:
            raise play_error[0]

        logger.info("⏹️  Finished playing")
    except Exception as e:
        logger.error(f"Playback failed: {e}", exc_info=True)
        # Fallback: send as audio file attachment
        if not is_music:
            try:
                await ctx.send("⚠️ เล่นในห้องเสียงไม่ได้ ส่งเป็นไฟล์แทน:", file=discord.File(source_url))
            except Exception:
                await ctx.send(f"❌ เล่นเสียงไม่ได้: {e}")
        else:
            await ctx.send(f"❌ เล่นเพลงไม่ได้: {e}")


# ── Helper ───────────────────────────────────────────────────────────────────


async def ensure_voice(ctx: commands.Context) -> bool:
    """Ensure the bot is in a voice channel. Returns True if connected."""
    if ctx.voice_client and ctx.voice_client.is_connected():
        return True

    # Auto-join if the user is in a voice channel
    if ctx.author.voice and ctx.author.voice.channel:
        await ctx.author.voice.channel.connect()
        return True

    await ctx.send("❌ คุณต้องอยู่ในห้องเสียงก่อน หรือใช้คำสั่ง `!join`")
    return False


# ── Commands ─────────────────────────────────────────────────────────────────


@bot.command(name="join")
async def cmd_join(ctx: commands.Context):
    """เข้าร่วมห้องเสียงที่คุณอยู่"""
    if not ctx.author.voice:
        await ctx.send("❌ คุณต้องอยู่ในห้องเสียงก่อน")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client:
        if ctx.voice_client.channel == channel:
            await ctx.send(f"✅ อยู่ในห้อง **{channel.name}** แล้ว")
            return
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()

    await ctx.send(f"🔊 เข้าร่วมห้อง **{channel.name}** แล้ว")
    logger.info(f"Joined voice channel: {channel.name}")


@bot.command(name="leave")
async def cmd_leave(ctx: commands.Context):
    """ออกจากห้องเสียง"""
    if ctx.voice_client:
        channel_name = ctx.voice_client.channel.name
        await ctx.voice_client.disconnect()
        await ctx.send(f"👋 ออกจากห้อง **{channel_name}** แล้ว")
        logger.info(f"Left voice channel: {channel_name}")
    else:
        await ctx.send("❌ บอทไม่ได้อยู่ในห้องเสียง")


@bot.command(name="speak", aliases=["s", "พูด"])
async def cmd_speak(ctx: commands.Context, *, text: str):
    """แปลงข้อความภาษาไทยเป็นเสียงพูด

    Usage: !speak สวัสดีครับ
    """
    if len(text) > Config.MAX_TEXT_LENGTH:
        await ctx.send(
            f"❌ ข้อความยาวเกินไป (สูงสุด {Config.MAX_TEXT_LENGTH} ตัวอักษร)"
        )
        return

    if not await ensure_voice(ctx):
        return

    # Show typing indicator
    async with ctx.typing():
        try:
            filepath = await tts.synthesize(text)
        except Exception as e:
            await ctx.send(f"❌ สร้างเสียงไม่ได้: {e}")
            logger.error(f"TTS error: {e}")
            return

    await ctx.message.add_reaction("🔊")
    await audio_queue.put({"ctx": ctx, "type": "tts", "filepath": filepath, "display_text": text})


@bot.command(name="chat", aliases=["c", "ถาม"])
async def cmd_chat(ctx: commands.Context, *, text: str):
    """ถาม Ollama แล้วพูดคำตอบออกเสียง

    Usage: !chat วันนี้อากาศเป็นยังไง
    """
    if not await ensure_voice(ctx):
        return

    async with ctx.typing():
        # Step 1: Get response from Ollama
        try:
            response = await ollama.generate(text)
        except ConnectionError as e:
            await ctx.send(f"❌ {e}")
            return
        except RuntimeError as e:
            await ctx.send(f"❌ Ollama error: {e}")
            return

        if not response:
            await ctx.send("❌ Ollama ตอบกลับว่างเปล่า")
            return

        # Show the text response
        await ctx.send(f"🤖 **{response}**")

        # Step 2: Convert response to speech
        try:
            filepath = await tts.synthesize(response)
        except Exception as e:
            await ctx.send(f"❌ สร้างเสียงไม่ได้: {e}")
            logger.error(f"TTS error: {e}")
            return

    await audio_queue.put({"ctx": ctx, "type": "tts", "filepath": filepath, "display_text": response})


@bot.command(name="voice", aliases=["v", "เสียง"])
async def cmd_voice(ctx: commands.Context, voice_name: str | None = None):
    """เปลี่ยนเสียงพูด หรือดูรายชื่อเสียงที่มี

    Usage:
        !voice           - แสดงรายชื่อเสียง
        !voice premwadee - เปลี่ยนเป็นเสียง Premwadee
        !voice niwat     - เปลี่ยนเป็นเสียง Niwat
    """
    if voice_name is None:
        # List available voices
        lines = ["🎙️ **เสียงที่มีให้เลือก:**\n"]
        for key, full_name in Config.THAI_VOICES.items():
            marker = " ← ใช้อยู่" if full_name == tts.voice else ""
            gender = "👩" if "Neural" in full_name and key != "niwat" else "👨"
            lines.append(f"  {gender} `{key}` — {full_name}{marker}")
        lines.append(f"\nใช้: `{Config.COMMAND_PREFIX}voice <ชื่อ>` เพื่อเปลี่ยน")
        await ctx.send("\n".join(lines))
        return

    result = tts.set_voice(voice_name)
    if result:
        await ctx.send(f"✅ เปลี่ยนเสียงเป็น **{result}** แล้ว")
    else:
        keys = ", ".join(Config.THAI_VOICES.keys())
        await ctx.send(f"❌ ไม่พบเสียง `{voice_name}`\nเสียงที่มี: {keys}")


@bot.command(name="stop", aliases=["หยุด"])
async def cmd_stop(ctx: commands.Context):
    """หยุดเล่นเสียงและล้างคิวทั้งหมด"""
    # Clear the queue
    while not audio_queue.empty():
        try:
            item = audio_queue.get_nowait()
            if item.get("type") == "tts" and "filepath" in item:
                tts.cleanup(item["filepath"])
            audio_queue.task_done()
        except asyncio.QueueEmpty:
            break

    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏹️ หยุดเล่นและล้างคิวทั้งหมดแล้ว")
    else:
        await ctx.send("⏹️ ล้างคิวทั้งหมดแล้ว")


@bot.command(name="skip", aliases=["ข้าม"])
async def cmd_skip(ctx: commands.Context):
    """ข้ามเพลง/เสียงที่กำลังเล่นอยู่"""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭️ ข้ามแล้ว")
    else:
        await ctx.send("❌ ไม่มีเสียงกำลังเล่นอยู่")


@bot.command(name="queue", aliases=["q", "คิว"])
async def cmd_queue(ctx: commands.Context):
    """แสดงคิวเสียงและเพลงที่กำลังรอเล่น"""
    if audio_queue.empty():
        await ctx.send("📭 คิวว่างเปล่า")
        return

    # Hacky way to peek the queue in asyncio
    items = list(audio_queue._queue)
    
    embed = discord.Embed(
        title="📋 คิวเสียง",
        color=0x1E90FF,
    )
    
    desc = ""
    for i, item in enumerate(items, 1):
        icon = "🎶" if item.get("type") == "music" else "🔊"
        desc += f"{i}. {icon} {item['display_text']}\n"
    
    embed.description = desc
    await ctx.send(embed=embed)


@bot.command(name="play", aliases=["p", "เล่น"])
async def cmd_play(ctx: commands.Context, *, query: str):
    """เล่นเพลงจาก YouTube
    
    สามารถระบุเวลาเริ่มและระยะเวลาได้โดยใช้ start= และ duration=
    เช่น: !play เพลงรัก start=01:30 duration=30
    หรือ: !play เพลงรัก 01:30 30
    """
    if not await ensure_voice(ctx):
        return

    # Parse start and duration
    start = None
    duration = None
    
    # Check for start=... duration=... syntax
    start_match = re.search(r'start=([0-9:]+)', query)
    duration_match = re.search(r'duration=([0-9:]+)', query)
    
    if start_match:
        start = start_match.group(1)
        query = query.replace(start_match.group(0), '')
    
    if duration_match:
        duration = duration_match.group(1)
        query = query.replace(duration_match.group(0), '')
        
    # If explicit tags not found, try to match shorthand at the end: !play query [start] [duration]
    if not start and not duration:
        parts = query.split()
        if len(parts) >= 2 and re.match(r'^[0-9:]+$', parts[-1]):
            # Has at least one time string at the end
            if len(parts) >= 3 and re.match(r'^[0-9:]+$', parts[-2]):
                # Has two time strings: query start duration
                duration = parts[-1]
                start = parts[-2]
                query = " ".join(parts[:-2])
            else:
                # Has one time string: query start
                start = parts[-1]
                query = " ".join(parts[:-1])
                
    query = query.strip()
    if not query:
        await ctx.send("❌ กรุณาระบุชื่อเพลงหรือ URL")
        return

    async with ctx.typing():
        info = await MusicEngine.extract_info(query)
        
        if not info or not info.get("url"):
            await ctx.send(f"❌ ค้นหาเพลง `{query}` ไม่พบ")
            return
            
        title = info.get("title", query)
        
        # Build display text with time info if provided
        time_info = ""
        if start or duration:
            time_info = f" [เริ่ม: {start or '0'} | นาน: {duration or 'จนจบ'}]"
            
        display_text = f"{title}{time_info}"

        await audio_queue.put({
            "ctx": ctx, 
            "type": "music", 
            "url": info["url"], 
            "display_text": display_text,
            "start": start,
            "duration": duration
        })
        
        await ctx.send(f"✅ เพิ่มลงคิว: **{title}**")


@bot.command(name="help_tts", aliases=["ช่วย"])
async def cmd_help(ctx: commands.Context):
    """แสดงคำสั่งทั้งหมด"""
    p = Config.COMMAND_PREFIX
    embed = discord.Embed(
        title="🇹🇭 Thai TTS Bot — คำสั่ง",
        description="บอทแปลงข้อความภาษาไทยเป็นเสียงพูด",
        color=0x1E90FF,
    )
    embed.add_field(
        name="🔊 เสียงพูด",
        value=(
            f"`{p}speak <ข้อความ>` — แปลงข้อความเป็นเสียง\n"
            f"`{p}chat <คำถาม>` — ถาม AI แล้วพูดคำตอบ\n"
            f"`{p}stop` — หยุดเล่นเสียง"
        ),
        inline=False,
    )
    embed.add_field(
        name="🎙️ ห้องเสียง",
        value=(
            f"`{p}join` — เข้าร่วมห้องเสียง\n"
            f"`{p}leave` — ออกจากห้องเสียง"
        ),
        inline=False,
    )
    embed.add_field(
        name="⚙️ ตั้งค่า",
        value=(
            f"`{p}voice` — ดู/เปลี่ยนเสียงพูด\n"
            f"`{p}help_tts` — แสดงคำสั่งนี้"
        ),
        inline=False,
    )
    embed.set_footer(text="Powered by edge-tts + Ollama")
    await ctx.send(embed=embed)


# ── Error Handling ───────────────────────────────────────────────────────────


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    """Global error handler."""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ ขาด argument: `{error.param.name}`\nลองใช้ `!help_tts`")
    elif isinstance(error, commands.CommandNotFound):
        pass  # Ignore unknown commands
    else:
        logger.error(f"Command error: {error}")
        await ctx.send(f"❌ เกิดข้อผิดพลาด: {error}")


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    """Entry point."""
    errors = Config.validate()
    if errors:
        for e in errors:
            logger.error(f"❌ Config error: {e}")
        logger.error("Create a .env file with DISCORD_TOKEN=your_token_here")
        sys.exit(1)

    logger.info("🚀 Starting Thai TTS Discord Bot...")
    logger.info(f"   Model: {Config.OLLAMA_MODEL}")
    logger.info(f"   Voice: {Config.DEFAULT_VOICE}")
    logger.info(f"   Prefix: {Config.COMMAND_PREFIX}")

    bot.run(Config.DISCORD_TOKEN, log_handler=None)


if __name__ == "__main__":
    main()
