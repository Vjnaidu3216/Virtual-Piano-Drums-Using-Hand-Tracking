🎹🪘Virtual Piano & Drums Using Hand Tracking
This mini-project allows users to play a virtual piano and drum set using only their fingers
and a webcam. Built with Python, OpenCV, MediaPipe, and PyGame, the system detects
finger movement and plays sound based on where and how fast the finger moves. It
supports two instruments — piano and drums — and lets the user switch between them
using hand gestures.
🎯Features
• • Hand gesture-controlled virtual piano and drum set
• • 13 piano keys with real piano note sounds
• • 7 drums visually laid out like a real drum kit
• • Tap detection: only plays sound when finger moves (not just hovering)
• • Only index finger triggers drum sounds (realistic drumstick behavior)
• • Gesture-based switching between piano and drum mode
🛠️Technologies Used
• • Python 3.x
• • OpenCV
• • MediaPipe
• • PyGame
• • NumPy (optional)
🚀How to Run
1. Clone the repository:
git clone https://github.com/yourusername/virtual-instrument.git
2. Navigate into the project folder:
cd virtual-instrument
3. Set up a virtual environment (optional but recommended):
python -m venv venv
venv\Scripts\activate # Windows
# OR
source venv/bin/activate # Mac/Linux
4. Install dependencies:
pip install -r requirements.txt
5. Run the project:
python main.py
🎵Sounds
All sounds used in this project are stored in `.wav` format inside the `sounds/` folder for
piano notes and `drums/` folder for drum samples. You may replace or add more sounds if
needed.
🧠How It Works
The system uses MediaPipe to track hand landmarks from your webcam feed. It detects
your finger position, monitors movement speed, and determines if you're 'tapping' a piano
key or drum pad. Piano allows any finger for interaction, while drums are triggered only by
the index finger. Mode switching is done by moving a hand to the top of the screen.
📁Folder Structure
 virtual-instrument/
├── main.py
├── README.md
├── sounds/
│ └── c1.wav, d1.wav, ...
├── drums/
│ └── snare.wav, tom.wav, ...
├── requirements.txt
📌Requirements
• • Python 3.10 or 3.11 (do not use Python 3.13 as some packages may not install)
• • Webcam
• • Well-lit environment for better gesture detection
🙌Credits
• • MediaPipe (Google) - for hand tracking
• • PyGame - for playing .wav sounds
• • parisjava/wav-piano-sound - for piano note samples
• • freesound.org - for free drum sound samples
📃License
This project is open-source and free to use for personal and educational purposes.
