# Two-Hand Object Control via Computer Vision

Control objects using your hands in real time with Computer Vision & AI.  
Dual-hand gesture tracking • Real-time object manipulation • Modular & Extensible

---

## 🚀 Features

- Dual-hand tracking to monitor the positions and gestures of both hands  
- Gesture-to-action mapping for translation, rotation, and scaling of objects  
- Real-time feedback for fluid, responsive control  
- Modular architecture for easy extension  
- Cross-platform compatibility (Windows, Linux, macOS)  

---

## 📦 Installation & Setup

1. Clone this repository:
   git clone https://github.com/sriramsowmithri9807/Two-Hand-Object-Control-by-Computer-Vision.git
   cd Two-Hand-Object-Control-by-Computer-Vision

2. (Optional) Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run the demo:
   python demo.py

---

## 🧠 How It Works

1. Hand detection – Detects and landmarks key points on both hands in each camera frame  
2. Gesture recognition – Classifies gestures such as open hand, pinch, drag, rotate, etc.  
3. Control mapping – Converts gestures into commands for manipulating objects  
4. Rendering / actuation – Executes commands to control virtual or physical objects  

---

## 🛠 Project Structure

.
├── data/                   # Gesture datasets or recordings
├── models/                 # Pretrained model weights
├── src/                    # Core source code
│   ├── detection.py
│   ├── gesture.py
│   ├── control.py
│   └── utils.py
├── demo.py                 # Main demo script
├── requirements.txt        # Dependencies
├── tests/                  # Unit tests
└── README.md               # Project docs

---

## 🎯 Sample Usage

# Launch with webcam
python demo.py --input webcam

# Run on a video file
python demo.py --input videos/demo.mp4

---

## 🎨 Supported Gestures & Controls

Gesture / Motion           | Action              
---------------------------|----------------------
Pinch & drag               | Move object         
Twist / rotate fingers     | Rotate object       
Spread / close fingers     | Scale object        
Two-hand symmetry          | Complex transforms  
Stop gesture               | Pause / Freeze      

---

## ✅ Requirements

- Python 3.7+  
- OpenCV  
- NumPy  
- MediaPipe / OpenPose  
- (Optional) PyTorch or TensorFlow (for custom models)  

Install:
   pip install opencv-python numpy mediapipe

---

## 📈 Demo & Results

(Add screenshots or GIFs of the system in action here)  

Example: Controlling a virtual object with two hands in real time.

---

## 🚀 Future Improvements

- Gesture personalization  
- Multi-object control  
- 3D object manipulation  
- Haptic feedback integration  
- Performance optimization  

---

## 🤝 Contributing

Contributions are welcome!  

1. Fork the repo  
2. Create a branch: git checkout -b feature/YourFeature  
3. Commit & push your changes  
4. Submit a PR  

---

## 📝 License

MIT License

---

## 📞 Contact

- Author: Sriram Sowmithri (https://github.com/sriramsowmithri9807)  
- Email: sowmithrisriram7@gmail.com  
- Acknowledgments: Thanks to OpenCV, MediaPipe, and open-source tools  
