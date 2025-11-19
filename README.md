<p align="center">
<h1 align="center">🎬 VidSnapAI – AI Powered Reel Generator</h1>
</p>

<p align="center">
A lightweight <b>Flask-based application</b> that transforms your images and text into short <b>vertical video reels</b>.  
Powered by <b>FFmpeg</b> for video creation and <b>ElevenLabs TTS</b> for AI-generated voiceovers.  
If TTS generation fails, a default background track is used automatically. 🎶
</p>

---

## 📖 About the Project

**VidSnapAI** is a simple yet powerful automated video creation tool.  
Users upload multiple images and a short description — the system converts the text into speech using the ElevenLabs API and then assembles a short-form video reel using FFmpeg.

This project is built to explore multimedia automation using Python, integrating Flask, FFmpeg, and AI-based audio synthesis.

---

## 🧠 How It Works

1. Users upload images + a short text description.  
2. Files are saved in:  
   **`user_uploads/<uuid>/`**
3. The worker script `generate_process.py` sends the description to ElevenLabs TTS.  
4. If TTS fails, fallback audio from  
   **`static/songs/1.mp3`**  
   is used.
5. FFmpeg merges the images + audio into a final video.  
6. The generated reel is stored in:  
   **`static/reels/`**

---

## 🛠 Tech Stack

<p align="center">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original-wordmark.svg" width="50" height="50" />
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/flask/flask-original-wordmark.svg" width="50" height="50" />
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original.svg" width="45" height="45" />
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original.svg" width="45" height="45" />
</p>

---

## 🚀 Features

- ✅ Upload multiple images with a description  
- ✅ AI voice-over generation (ElevenLabs TTS)  
- ✅ Automatic fallback audio when TTS fails  
- ✅ FFmpeg-based reel generation  
- ✅ Simple Flask-powered frontend  
- ✅ Structured directories for clean file management  

---
### Clone the repository
```bash
git clone https://github.com/Anushka7237/VidSnapAI.git
cd VidSnapAI

