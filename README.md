# 😜 Gesture Detector

**Gesture Detector** is a real-time AI application that uses your webcam to detect facial expressions and hand gestures, displaying custom images/memes as reactions.

Powered by **MediaPipe** and **OpenCV** for fast, accurate, local detection - no cloud API required!

---

## Features

- 🎥 **Real-time webcam tracking** with minimal latency
- 😝 **Detects tongue out**
- 😴 **Detects eyes closed**
- ✌️ **Detects peace sign**
- 👍 **Detects thumbs up**
- ✋ **Detects open palm**
- ✊ **Detects fist**
- ❤️ **Detects heart shape** (both hands)
- 🖼️ **Shows custom reaction GIFs/images** in a separate window
- 🎨 **Toggle landmarks** on/off (press 'L')
- ⚙️ **No external AI API required** - runs 100% locally

---

## Quick Start

1. **Clone and setup:**
   ```bash
   git clone https://github.com/EmilioMonteLuna/ImageRecognition.git
   cd ImageRecognition
   setup.bat

### Controls
- **Press 'L'** - Toggle face mesh and hand skeleton on/off
- **Press 'Q'** - Quit the application

---
## Requirements

- Python 3.12.x (⚠️ MediaPipe doesn't support Python 3.13 yet)
- A webcam
- Windows, macOS, or Linux
- Conda (recommended) or Python virtual environment

---

## Folder Structure

```
ImageRecognition/
│
├── assets/
│   ├── tongue.gif
│   ├── closed_eyes.gif
│   ├── peace.gif
│   ├── thumbs_up.gif
│   ├── open_palm.gif
│   ├── fist.gif
│   └── lovely.gif
│
├── main.py
├── requirements.txt
├── setup.bat / setup.sh
├── run.bat / run.sh
├── README.md
```

---

## Supported Gestures

| Gesture | File | How To |
|---------|------|--------|
| 😝 Tongue Out | `tongue.gif` | Stick tongue out |
| 😴 Eyes Closed | `closed_eyes.gif` | Close eyes tightly |
| ✌️ Peace Sign | `peace.gif` | Index + middle fingers up |
| 👍 Thumbs Up | `thumbs_up.gif` | Thumb pointing up |
| ✋ Open Palm | `open_palm.gif` | All fingers extended |
| ✊ Fist | `fist.gif` | Closed fist |
| ❤️ Heart | `lovely.gif` | Both hands, index fingers top, thumbs bottom |

---

## 🎨 Customize Your Reactions

1. Add your own GIF/image files to the `assets/` folder
2. Name them according to the gesture (or update `main.py`)
3. Supported formats: `.gif`, `.jpg`, `.png`, `.jpeg`



---

## Troubleshooting

**Camera not opening?**
- Close other apps using the camera (Zoom, Discord, etc.)

**Gestures not detecting?**
- Press 'L' to show landmarks and verify tracking
- Ensure good lighting
- Adjust sensitivity in `main.py`
---

## Built With

- **[MediaPipe](https://mediapipe.dev/)** - Face mesh and hand tracking
- **[OpenCV](https://opencv.org/)** - Video processing
- **[imageio](https://imageio.readthedocs.io/)** - GIF animation
- **[NumPy](https://numpy.org/)** - Numerical computations

---

## License

GPL-3.0 License - Feel free to fork, modify, and share!

---

```cmd
pip install -r requirements.txt
```

Or install manually:

```cmd
pip install opencv-python mediapipe numpy
```

### Add Your Custom Images

Create an `assets` folder and add your custom images/memes:

- `tongue.gif` - Shown when you stick your tongue out
- `closed_eyes.gif` - Shown when you close your eyes
- `peace.gif` - Shown when you make a peace sign ✌️
- `thumbs_up.gif` - Shown when you give thumbs up 👍
- `open_palm.gif` - Shown when you show an open palm ✋
- `fist.gif` - Shown when you make a fist ✊

**Supported formats:** `.gif`, `.jpg`, `.png`, `.jpeg`

### Run the App

```cmd
python main.py
```

Two windows will appear:
- **Gesture Detector - Camera Feed** → Your live webcam with gesture tracking
- **Reaction** → Custom image/meme based on detected gesture

Press **Q** to quit.

##  Supported Gestures

| Gesture | Detection | Image File |
|---------|-----------|------------|
| 😝 Tongue Out | Stick your tongue out | `tongue.gif` |
| 😴 Eyes Closed | Close both eyes | `closed_eyes.gif` |
| ✌️ Peace Sign | Index & middle fingers up | `peace.gif` |
| 👍 Thumbs Up | Thumb pointing up | `thumbs_up.gif` |
| ✋ Open Palm | All fingers extended | `open_palm.gif` |
| ✊ Fist | Closed hand | `fist.gif` |

## Customize Images

Simply replace the files in the `assets/` folder with your own memes or images. The app will automatically load them when it starts.

**Tips:**
- Use funny memes or GIFs for better entertainment
- Keep images around 640x480 for best performance
- Name your files exactly as shown in the table above

## Troubleshooting

| Problem | Fix |
|---------|-----|
| No matching distribution for mediapipe | You're using Python 3.13 — use 3.12 instead |
| Image not showing | Check that images exist in `assets/` with correct names |
| Camera not opening | Close other apps using the webcam (Zoom, Discord, etc.) |
| Reaction window too small | Resize manually or adjust in code |

## 💡 Future Ideas

- 🔊 Add sound effects for each gesture
- 🎬 Support animated GIFs (frame-by-frame)
- 📊 Log gesture history
- 🌐 Web interface for remote viewing
- 🤖 Add more custom gestures
- 🎨 Overlay effects on camera feed

## 📋 Technical Details

**Powered by:**
- [MediaPipe](https://google.github.io/mediapipe/) - Face mesh and hand tracking
- [OpenCV](https://opencv.org/) - Video processing and display
- [NumPy](https://numpy.org/) - Array operations

**Detection Methods:**
- Face mesh uses 468 facial landmarks
- Hand tracking uses 21 hand landmarks per hand
- Gesture recognition based on landmark position analysis

## 🪪 License

This project is open-source. Feel free to modify and use it however you like!

