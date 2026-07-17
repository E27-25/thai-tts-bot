# 🇹🇭 Thai TTS Discord Bot

บอท Discord ที่แปลงข้อความภาษาไทยเป็นเสียงพูดในห้องเสียง  
ใช้ **edge-tts** สำหรับสังเคราะห์เสียงไทย + **Ollama** สำหรับแชท AI ภาษาไทย

---

## ✨ Features

- 🔊 **`!speak`** — แปลงข้อความภาษาไทยเป็นเสียงพูดในห้องเสียง
- 🤖 **`!chat`** — ถาม AI (ผ่าน Ollama) แล้วพูดคำตอบออกเสียง
- 🎵 **`!play`** — เล่นเพลงจาก YouTube (รองรับการตั้งเวลาเริ่ม/จบ)
- 🎙️ **`!voice`** — เลือกเสียงพูด (Premwadee 👩 / Niwat 👨 / Achara 👩)
- ⏹️ **`!stop`, `!skip`, `!queue`** — จัดการคิวเสียงและเพลงได้อย่างอิสระ
- 📋 **คิวเสียงอัจฉริยะ** — เสียงพูดและเพลงเล่นต่อกันอัตโนมัติ ไม่ซ้อนทับกัน

---

## 📦 Prerequisites

### 1. Python 3.10+
```bash
python3 --version
```

### 2. ffmpeg (จำเป็นสำหรับ Discord voice)
```bash
brew install ffmpeg
```

### 3. Ollama (สำหรับคำสั่ง !chat)
```bash
brew install ollama
ollama serve          # เปิด Ollama server
ollama pull llama3.2  # ดาวน์โหลดโมเดล
```

---

## 🚀 Setup

### 1. Clone & Install
```bash
cd thai-tts-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. สร้าง Discord Bot Token

1. ไปที่ [Discord Developer Portal](https://discord.com/developers/applications)
2. กด **New Application** → ตั้งชื่อ
3. ไปที่แท็บ **Bot**
4. กด **Reset Token** → คัดลอก Token
5. เปิด **Privileged Gateway Intents**:
   - ✅ MESSAGE CONTENT INTENT
   - ✅ SERVER MEMBERS INTENT (optional)
6. ไปที่แท็บ **OAuth2** → **URL Generator**
   - Scopes: `bot`
   - Permissions: `Connect`, `Speak`, `Send Messages`, `Read Message History`
7. คัดลอก URL แล้วเปิดในเบราว์เซอร์เพื่อเชิญบอทเข้า server

### 3. ตั้งค่า .env
```bash
cp .env.example .env
# แก้ไข .env ใส่ DISCORD_TOKEN ของคุณ
```

### 4. รันบอท (Start the Bot)
```bash
python bot.py
```
> **วิธีปิดบอท (How to Stop):** กด `Ctrl + C` ในหน้าต่าง Terminal ที่บอทรันอยู่

---

## 🔁 การเปิด/ปิดบอท (Start/Stop Commands)

หากคุณปิด Terminal ไปแล้วและต้องการ **เปิดบอทใหม่**:
```bash
cd ~/Desktop/kuy/thai-tts-bot
source venv/bin/activate
python bot.py
```

หากต้องการ **ปิดบอท**:
- ไปที่หน้าต่าง Terminal ที่บอทกำลังทำงานอยู่
- กดปุ่ม `Ctrl + C` บนคีย์บอร์ดเพื่อหยุดการทำงาน

---

## 📖 Commands

| คำสั่ง | คำอธิบาย |
|--------|----------|
| `!join` | เข้าร่วมห้องเสียงที่คุณอยู่ |
| `!leave` | ออกจากห้องเสียง |
| `!speak <ข้อความ>` | แปลงข้อความเป็นเสียงพูด |
| `!chat <คำถาม>` | ถาม AI แล้วพูดคำตอบ |
| `!play <เพลง/URL>` | เล่นเพลงจาก YouTube (รองรับเวลาเริ่มและระยะเวลา เช่น `01:30 30` หรือ `start=01:30 duration=30`) |
| `!skip` | ข้ามเพลง/เสียงปัจจุบัน |
| `!queue` | ดูคิวเสียงและเพลงที่กำลังรอเล่น |
| `!voice` | แสดงรายชื่อเสียงที่มี |
| `!voice <ชื่อ>` | เปลี่ยนเสียง (premwadee/niwat/achara) |
| `!stop` | หยุดเล่นเสียงและล้างคิวทั้งหมด |
| `!help_tts` | แสดงคำสั่งทั้งหมด |

**Aliases:** `!s` = `!speak`, `!c` = `!chat`, `!v` = `!voice`, `!p` = `!play`, `!q` = `!queue`  
**ภาษาไทย:** `!พูด`, `!ถาม`, `!เสียง`, `!หยุด`, `!ช่วย`, `!เล่น`, `!ข้าม`, `!คิว`

---

## ⚙️ Configuration (.env)

| Variable | Default | Description |
|----------|---------|-------------|
| `DISCORD_TOKEN` | — | Discord bot token (required) |
| `OLLAMA_MODEL` | `llama3.2` | Ollama model for chat |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama API URL |
| `DEFAULT_VOICE` | `th-TH-PremwadeeNeural` | Default Thai voice |
| `COMMAND_PREFIX` | `!` | Command prefix |
| `MAX_TEXT_LENGTH` | `500` | Max text length for TTS |

---

## 🏗️ Architecture

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

---

## 📝 License

MIT
