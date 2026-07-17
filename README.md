<div align="center">

<img src="https://media.tenor.com/lfDATg4Bhc0AAAAC/happy-cat.gif" alt="Happy Cat" width="300" style="border-radius: 15px;" />
<br/><br/>

<!-- Cute Typing SVG Header -->
<img src="https://readme-typing-svg.demolab.com?font=Nunito&weight=800&size=40&pause=1000&color=F472B6&center=true&vCenter=true&width=800&lines=Thai+TTS+and+Music+Bot;Powered+by+Ollama+AI;Seamless+YouTube+Music;Your+Cute+Discord+Helper" alt="Typing Animation" />

<p align="center">
  <b>A smart, ultra-cute Discord bot combining AI Chat, Thai Text-to-Speech, and Music Streaming! 🐾✨</b>
</p>

<!-- Cute Tech Stack Badges -->
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-FFB6C1?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Discord.py-2.4+-FF9AA2?style=flat-square&logo=discord&logoColor=white" alt="Discord.py" />
  <img src="https://img.shields.io/badge/Edge--TTS-Voice-FFDAC1?style=flat-square&logo=microsoft&logoColor=white" alt="Edge-TTS" />
  <img src="https://img.shields.io/badge/Ollama-AI-E2F0CB?style=flat-square&logo=ollama&logoColor=gray" alt="Ollama" />
  <img src="https://img.shields.io/badge/yt--dlp-Music-B5EAD7?style=flat-square&logo=youtube&logoColor=white" alt="yt-dlp" />
</p>

<img src="https://media.tenor.com/lZ6OQk3V0tQAAAAC/aesthetic-cat.gif" alt="Aesthetic Cat" width="250" style="border-radius: 15px; margin: 20px 0;" />

</div>

---

## 🌸 Core Features 🐾

<table width="100%" style="border-collapse: collapse;">
  <tr>
    <td width="50%" align="center">
      <img src="https://media.tenor.com/W2O-L0tXWb4AAAAC/pixel-cat.gif" alt="Feature Cat 1" width="100" style="border-radius: 10px;" />
      <h3>🗣️ Advanced Thai TTS</h3>
      <p>High-fidelity Thai text-to-speech using Microsoft Edge Neural voices. Switch between male and female voices on the fly! 😸</p>
    </td>
    <td width="50%" align="center">
      <img src="https://media.tenor.com/13_RSEKz5dEAAAAC/cat-pixel.gif" alt="Feature Cat 2" width="100" style="border-radius: 10px;" />
      <h3>🤖 Local AI Integration</h3>
      <p>Talk to Ollama LLMs directly in your voice channel. The bot processes your questions and reads the answers out loud! ✨</p>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <img src="https://media.tenor.com/3T9jHhW9yTEAAAAC/cat-pixel.gif" alt="Feature Cat 3" width="100" style="border-radius: 10px;" />
      <h3>🎵 Music Streaming</h3>
      <p>Built-in <code>yt-dlp</code> integration for high-quality YouTube audio. Supports precise start times and durations for perfect playback! 🎶</p>
    </td>
    <td width="50%" align="center">
      <img src="https://media.tenor.com/2m65s7T-e0UAAAAC/pixel-cat.gif" alt="Feature Cat 4" width="100" style="border-radius: 10px;" />
      <h3>📋 Intelligent Audio Queue</h3>
      <p>A unified async queue system that flawlessly handles the transition between AI speech and music streams without overlapping! 🐾</p>
    </td>
  </tr>
</table>

---

## 🚀 Quick Setup 🧶

### Prerequisites
1. **Python 3.10+** 🐍
2. **FFmpeg** (`brew install ffmpeg`) 🎬
3. **Ollama** (`brew install ollama` and `ollama pull llama3.2`) 🧠

### Installation

```bash
git clone https://github.com/E27-25/thai-tts-bot.git
cd thai-tts-bot

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env and add your DISCORD_TOKEN 🔑
```

### Execution
```bash
python bot.py
```

<div align="center">
  <img src="https://media.tenor.com/bK1qz1-U8xUAAAAC/pixel-cat.gif" alt="Window Cat" width="250" style="border-radius: 15px; margin-top: 20px; margin-bottom: 20px;" />
</div>

---

## 🎀 Command Reference 🐈

<div align="center">

| Command | Arguments | Description |
|:---|:---|:---|
| 🐾 <kbd>!speak</kbd> / <kbd>!s</kbd> | `<text>` | Converts Thai text to neural speech in the current voice channel. |
| 🐾 <kbd>!chat</kbd> / <kbd>!c</kbd> | `<query>` | Queries Ollama and reads the response aloud. |
| 🐾 <kbd>!play</kbd> / <kbd>!p</kbd> | `<url>` `[start]` `[duration]` | Streams YouTube audio. (e.g., `!play เพลงแมว 01:30 30`) |
| 🐾 <kbd>!skip</kbd> | | Skips the currently playing audio stream. |
| 🐾 <kbd>!queue</kbd> / <kbd>!q</kbd> | | Displays the current pending audio queue. |
| 🐾 <kbd>!voice</kbd> / <kbd>!v</kbd> | `[voice_name]` | Changes the active TTS voice. Leave blank to view options. |
| 🐾 <kbd>!stop</kbd> | | Immediately halts playback and clears the entire queue. |
| 🐾 <kbd>!join</kbd> / <kbd>!leave</kbd> | | Manually control the bot's voice channel presence. |

  <br/>
  <img src="https://media.tenor.com/1Xz86h2t8qUAAAAC/cat-pixel.gif" alt="Command Cat" width="200" style="border-radius: 15px; margin-top: 20px;" />

</div>

---

## 🏗️ Architecture 🧶

```mermaid
graph TD
    User([User Commands]) -->|speak / chat| NLP[Ollama AI / TTS Engine]
    User -->|play| YTDL[yt-dlp Streamer]
    
    NLP --> Queue[(Async Audio Queue)]
    YTDL --> Queue
    
    Queue --> FFmpeg[FFmpeg Processor]
    FFmpeg --> Discord((Discord Voice Channel))
    
    style User fill:#F472B6,stroke:#fff,stroke-width:2px,color:#fff
    style Discord fill:#5865F2,stroke:#fff,stroke-width:2px,color:#fff
    style Queue fill:#333,stroke:#fff,stroke-width:2px,color:#fff
```

<br/>
<div align="center">
  <img src="https://media.tenor.com/7v3n4T7k9mYAAAAC/pixel-cat.gif" alt="Architecture Cat" width="250" style="border-radius: 15px; margin-bottom: 20px;" />
  <br/>
  <img src="https://media.tenor.com/T0b3i0a6L6cAAAAC/cat-cute.gif" alt="Coffee Cat" width="150" style="border-radius: 15px;" />
  <p><i>Engineered for performance, built with love. 💖🐾</i></p>
</div>
