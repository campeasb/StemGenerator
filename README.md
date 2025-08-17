# Stems Separator Project (Demucs)

This is my first project using a Machine Learning model :)  
With this app, you can **generate up to 4 stems** from any music track directly from a YouTube link.
---

## ✨ Features

- Paste a YouTube link → Automatically downloads the audio (via `yt-dlp`)
- GPU auto-detection for Demucs
- Per-stem preview + download
- Download all stems as a ZIP

---

## 🚀 Quickstart

### 0️⃣ Prerequisites

- **Python 3.10+** (recommended)  
- **ffmpeg** in your system `PATH` (required by `yt-dlp` & audio tools)  

Install ffmpeg:

- **macOS** → `brew install ffmpeg`
- **Windows** → `choco install ffmpeg`
- **Linux (Debian/Ubuntu)** → `sudo apt-get install ffmpeg`

---

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

### 2️⃣ Create & activate a virtual environment

```bash
py -3.11 -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
# Update PIP
python -m pip install --upgrade pip setuptools wheel
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```
### ⚡ (Optional) Install PyTorch for GPU
If you have a GPU, install the PyTorch version matching your CUDA setup:\
Visit: https://pytorch.org/get-started/locally/

Example for CUDA 12.1:
```bash
pip install --index-url https://download.pytorch.org/whl/cu121 torch==2.5.1 torchaudio==2.5.1
```

### 4️⃣ Run the app

```bash
streamlit run app.py
```