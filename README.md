<div align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdW5iaTBmMG42ZHpjd2EydnEwd3Y5dWt1M2UwbG4zZnJteDFyNDRkeCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/4ilFRqgbzbx4c/giphy.gif" alt="Anime Girl Listening to Music" width="400"/>

  # 🇹🇭 Thai TTS & Music Discord Bot 🎵🤖
  
  *A magical Discord bot that speaks Thai, chats with AI, and plays your favorite YouTube tunes!*

  [![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
  [![Discord.py](https://img.shields.io/badge/Discord.py-2.4+-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discordpy.readthedocs.io/)
  [![Edge-TTS](https://img.shields.io/badge/Edge--TTS-Voice-00A4EF?style=for-the-badge&logo=microsoft&logoColor=white)](https://github.com/rany2/edge-tts)
  [![Ollama](https://img.shields.io/badge/Ollama-AI-white?style=for-the-badge&logo=ollama&logoColor=black)](https://ollama.ai)

</div>

---

## ✨ 🌟 Features

- 🔊 **`!speak`** — แปลงข้อความภาษาไทยเป็นเสียงพูดในห้องเสียงด้วยน้ำเสียงที่สมจริง
- 🤖 **`!chat`** — ถาม AI (ผ่าน Ollama) แล้วให้บอทพูดคำตอบออกเสียงทันที!
- 🎵 **`!play`** — ค้นหาและเล่นเพลงจาก YouTube พร้อมรองรับการตั้งเวลาเริ่มและจบ (`start=` / `duration=`)
- 🎙️ **`!voice`** — เลือกเปลี่ยนเสียงพูดได้ดั่งใจ (👩 **Premwadee**, 👨 **Niwat**, 👩 **Achara**)
- 📋 **คิวเสียงอัจฉริยะ** — เสียงพูดและเสียงเพลงสามารถอยู่ในคิวเดียวกันได้ เล่นต่อกันอย่างลื่นไหลไม่มีสะดุด!
- ⏹️ **การควบคุมครบครัน** — ทั้ง `!stop`, `!skip`, และ `!queue`

---

## 📦 🛠️ Prerequisites

ก่อนเริ่มใช้งาน กรุณาติดตั้งโปรแกรมเหล่านี้ในเครื่องของคุณ:

### 1. Python 3.10+
```bash
python3 --version
```

### 2. FFmpeg (จำเป็นสำหรับการสตรีมเสียง)
```bash
brew install ffmpeg
```

### 3. Ollama (สำหรับ AI Chat)
```bash
brew install ollama
ollama serve          # เปิดเซิร์ฟเวอร์
ollama pull llama3.2  # หรือใช้โมเดลที่คุณต้องการ (เช่น qwen3:8b)
```

---

## 🚀 🎮 Setup & Installation

### 1. Clone & Install
```bash
cd thai-tts-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. สร้าง Discord Bot Token
1. ไปที่ [Discord Developer Portal](https://discord.com/developers/applications)
2. สร้าง **New Application** และไปที่แท็บ **Bot**
3. กด **Reset Token** แล้วคัดลอกเก็บไว้
4. **สำคัญมาก!** เปิดใช้งาน **Privileged Gateway Intents**:
   - ✅ MESSAGE CONTENT INTENT
   - ✅ SERVER MEMBERS INTENT
5. ไปที่แท็บ **OAuth2** → **URL Generator**
   - **Scopes**: `bot`
   - **Permissions**: `Connect`, `Speak`, `Send Messages`, `Read Message History`
6. นำ URL ที่ได้ไปเปิดในเบราว์เซอร์เพื่อเชิญบอทเข้าเซิร์ฟเวอร์ของคุณ

### 3. ตั้งค่า `.env`
```bash
cp .env.example .env
```
เปิดไฟล์ `.env` แล้วใส่ `DISCORD_TOKEN` ของคุณ

### 4. รันบอท (Start the Bot)
```bash
python bot.py
```
> 💡 **วิธีปิดบอท:** กด `Ctrl + C` ในหน้าต่าง Terminal

---

## 📖 🪄 Commands (คำสั่งทั้งหมด)

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `!join` | สั่งให้บอทเข้ามาในห้องเสียงที่คุณอยู่ |
| `!leave` | เตะบอทออกจากห้องเสียง |
| `!speak <ข้อความ>` | พิมพ์ข้อความแล้วบอทจะอ่านออกเสียงให้ฟัง |
| `!chat <คำถาม>` | คุยกับ AI แล้วบอทจะอ่านคำตอบ |
| `!play <เพลง/URL>` | ค้นหาและเล่นเพลงจาก YouTube (เช่น `!play เพลงรัก 01:30 30`) |
| `!skip` | ข้ามเพลงหรือเสียงที่กำลังเล่นอยู่ |
| `!queue` | ดูคิวเสียงและเพลงทั้งหมด |
| `!voice` | ดูรายชื่อเสียงทั้งหมด |
| `!voice <ชื่อ>` | เปลี่ยนเสียง (เช่น `!voice niwat`) |
| `!stop` | หยุดเล่นเสียงและล้างคิวทิ้งทั้งหมด |
| `!help_tts` | แสดงคู่มือคำสั่ง |

**✨ คีย์ลัด (Aliases):** `!s` = `!speak`, `!c` = `!chat`, `!v` = `!voice`, `!p` = `!play`, `!q` = `!queue`  
**🗣️ ภาษาไทย:** `!พูด`, `!ถาม`, `!เสียง`, `!หยุด`, `!เล่น`, `!ข้าม`, `!คิว`, `!ช่วย`

---

## ⚙️ 🎛️ Configuration (.env)

สามารถปรับแต่งค่าต่างๆ ได้ในไฟล์ `.env`:

| ตัวแปร (Variable) | ค่าเริ่มต้น (Default) | คำอธิบาย (Description) |
|----------|---------|-------------|
| `DISCORD_TOKEN` | — | Token ของ Discord Bot (บังคับ) |
| `OLLAMA_MODEL` | `llama3.2` | โมเดล AI ที่ต้องการใช้ (ต้องโหลดในเครื่องก่อน) |
| `OLLAMA_URL` | `http://localhost:11434` | URL ของ Ollama |
| `DEFAULT_VOICE` | `th-TH-PremwadeeNeural` | เสียงเริ่มต้นของบอท |
| `COMMAND_PREFIX` | `!` | ตัวนำหน้าคำสั่ง |
| `MAX_TEXT_LENGTH` | `500` | ความยาวข้อความสูงสุดที่ให้อ่าน |

---

## 🏗️ 🗺️ System Architecture

```text
User: !speak สวัสดี     User: !chat สบายดีไหม        User: !play เพลงรัก
       │                       │                             │
       │                       ▼                             ▼
       │                 ┌──────────┐                  ┌──────────┐
       │                 │  Ollama  │                  │  yt-dlp  │
       │                 │  (LLM)   │                  │ (YouTube)│
       │                 └────┬─────┘                  └────┬─────┘
       │                      │ Thai text                   │ Stream URL
       ▼                      ▼                             │
  ┌─────────────────────────────────┐                       │
  │          edge-tts               │                       │
  │  Thai text → MP3 audio         │                       │
  └──────────────┬──────────────────┘                       │
                 │                                          │
                 ▼                                          ▼
  ┌───────────────────────────────────────────────────────────────┐
  │                   Discord Voice Channel                       │
  │                   (FFmpeg audio stream)                       │
  │              [ TTS Audio & YouTube Music Queue ]              │
  └───────────────────────────────────────────────────────────────┘
```

<div align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeGtpb21sdXhwNTdsYnpqcXkxY3Nqa2Q0anlxb3pjc3Y2aWhwaDlnNyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l4FGpP4lxGGgK5CBW/giphy.gif" alt="Dancing Anime" width="300"/>
  <p><i>Enjoy your magical audio experience! 💖</i></p>
</div>
