<div align="center">

<img src="https://media.giphy.com/media/Jk4ZT6R0OEUoM/giphy.gif" alt="Bongo Cat" width="150" />

<!-- Animated Typing SVG Header -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=800&size=40&pause=1000&color=F772CA&center=true&vCenter=true&width=800&lines=Thai+TTS+%26+Music+Bot+🌸;Powered+by+Ollama+AI+🤖;Seamless+YouTube+Music+🎶;Your+Cute+Discord+Helper+✨" alt="Typing Animation" />

<p align="center">
  <b>A smart, high-performance Discord bot combining AI Chat, Thai Text-to-Speech, and Music Streaming in one cute package! 🐾</b>
</p>

<!-- Clean Tech Stack Badges -->
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Discord.py-2.4+-5865F2?style=flat-square&logo=discord&logoColor=white" alt="Discord.py" />
  <img src="https://img.shields.io/badge/Edge--TTS-Voice-0078D4?style=flat-square&logo=microsoft&logoColor=white" alt="Edge-TTS" />
  <img src="https://img.shields.io/badge/Ollama-AI-000000?style=flat-square&logo=ollama&logoColor=white" alt="Ollama" />
  <img src="https://img.shields.io/badge/yt--dlp-Stream-FF0000?style=flat-square&logo=youtube&logoColor=white" alt="yt-dlp" />
</p>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/nyan-cat.gif" width="100%" />

</div>

## 🌟 Core Features

<table width="100%" style="border-collapse: collapse;">
  <tr>
    <td width="50%" align="center">
      <h3>🗣️ Advanced Thai TTS</h3>
      <p>High-fidelity Thai text-to-speech utilizing Microsoft Edge Neural voices. Switch seamlessly between male and female voices on the fly.</p>
    </td>
    <td width="50%" align="center">
      <h3>🤖 Local AI Integration</h3>
      <p>Communicate with Ollama LLMs directly in your voice channel. The bot processes your questions and reads the AI's responses out loud.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <h3>🎵 Music Streaming</h3>
      <p>Built-in <code>yt-dlp</code> integration for high-quality YouTube audio. Supports precise start times and durations for perfect playback.</p>
    </td>
    <td width="50%" align="center">
      <h3>📋 Intelligent Audio Queue</h3>
      <p>A unified async queue system that flawlessly handles the transition between AI speech and music streams without overlapping.</p>
    </td>
  </tr>
</table>

<div align="center">
<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.gif" width="100%" />
</div>

## 🚀 Quick Setup

### Prerequisites
1. **Python 3.10+**
2. **FFmpeg** (`brew install ffmpeg`)
3. **Ollama** (`brew install ollama` and `ollama pull llama3.2`)

### Installation

```bash
git clone https://github.com/E27-25/thai-tts-bot.git
cd thai-tts-bot

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env and add your DISCORD_TOKEN
```

### Execution
```bash
python bot.py
```

<div align="center">
<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.gif" width="100%" />
</div>

## 🎀 Command Reference

<div align="center">

| Command | Arguments | Description |
|:---|:---|:---|
| `!speak` / `!s` | `<text>` | Converts Thai text to neural speech in the current voice channel. |
| `!chat` / `!c` | `<query>` | Queries Ollama and reads the response aloud. |
| `!play` / `!p` | `<url>` `[start]` `[duration]` | Streams YouTube audio. (e.g., `!play Never gonna give you up 01:30 30`) |
| `!skip` | | Skips the currently playing audio stream. |
| `!queue` / `!q` | | Displays the current pending audio queue. |
| `!voice` / `!v` | `[voice_name]` | Changes the active TTS voice. Leave blank to view options. |
| `!stop` | | Immediately halts playback and clears the entire queue. |
| `!join` / `!leave` | | Manually control the bot's voice channel presence. |

</div>

<div align="center">
<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/cloudy.gif" width="100%" />
</div>

## 🏗️ Architecture

```mermaid
graph TD
    User([User Commands]) -->|!speak / !chat| NLP[Ollama AI / TTS Engine]
    User -->|!play| YTDL[yt-dlp Streamer]
    
    NLP --> Queue[(Async Audio Queue)]
    YTDL --> Queue
    
    Queue --> FFmpeg[FFmpeg Processor]
    FFmpeg --> Discord((Discord Voice Channel))
    
    style User fill:#F772CA,stroke:#fff,stroke-width:2px,color:#fff
    style Discord fill:#5865F2,stroke:#fff,stroke-width:2px,color:#fff
    style Queue fill:#333,stroke:#fff,stroke-width:2px,color:#fff
```

<br/>
<div align="center">
  <img src="https://media.giphy.com/media/MDJ9IbxxvDUQM/giphy.gif" alt="Cute Cat" width="200" style="border-radius: 15px;" />
  <p><i>Engineered for performance, built with love. 💖</i></p>
</div>
