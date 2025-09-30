# Two-Hand-Object-Control-by-Computer-Vision-

````markdown
# Two-Hand Object Control via Computer Vision 🎯

**Two-Hand-Object-Control-by-Computer-Vision** is a computer vision project that enables manipulation of virtual or physical objects using the gestures or positions of *both hands* in real time. With deep learning, tracking, and gesture mapping, this system can interpret dual-hand input to control objects or environments intuitively.

## 🚀 Features

- **Dual-hand tracking**: Simultaneously monitor the positions and gestures of both hands.
- **Gesture-to-action mapping**: Map hand movements, orientations, and gestures to object control commands (e.g. translation, rotation, scaling).
- **Real-time feedback**: Low-latency processing to enable fluid, responsive control.
- **Modular architecture**: Easily extendable components for detection, tracking, and control logic.
- **Cross-platform compatibility**: Designed to run on Windows, Linux, and macOS (assuming compatible hardware and dependencies).

## 📦 Installation & Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/sriramsowmithri9807/Two-Hand-Object-Control-by-Computer-Vision.git
   cd Two-Hand-Object-Control-by-Computer-Vision
````

2. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. (If applicable) Download any model weights or datasets:

   ```text
   # Place pretrained weights in ./models/
   # Place sample gesture dataset in ./data/
   ```

5. Run the demo script:

   ```bash
   python demo.py
   ```

6. (Optional) Run unit tests:

   ```bash
   pytest
   ```

## 🧠 How It Works

1. **Hand detection** – Detects and landmarks key points on both hands in each camera frame.
2. **Gesture recognition & filtering** – Classifies gestures (open hand, pinch, drag, rotate, etc.).
3. **Control mapping** – Converts gestures and hand movements into object manipulation commands.
4. **Rendering / actuation** – Executes commands (simulation or physical setup) with real-time feedback.

## 🛠 Project Structure

```
.
├── data/                   # Gesture datasets or recorded hand motion logs
├── models/                 # Pretrained model weights, checkpoints
├── src/                    # Core source code (detection, tracking, control)
│   ├── detection.py
│   ├── gesture.py
│   ├── control.py
│   └── utils.py
├── demo.py                 # Demonstration / entry-point script
├── requirements.txt        # Python dependencies
├── tests/                  # Unit tests
│   └── test_gesture.py
└── README.md               # This file
```

## 🎯 Sample Usage

```bash
# Launch the system using webcam input
python demo.py --input webcam --mode interactive

# Use a video file instead
python demo.py --input videos/hand_demo.mp4 --mode playback

# Toggle visualization
python demo.py --visualize False
```

## 🎨 Supported Gestures & Controls

| Gesture / Hand Motion    | Mapped Action           |
| ------------------------ | ----------------------- |
| Pinch & drag             | Move object             |
| Twist / rotate fingers   | Rotate object           |
| Spread / close fingers   | Scale object            |
| Two-hand symmetry (both) | Complex transformations |
| Hand hold / stop gesture | Freeze / pause          |

## ✅ Dependencies / Requirements

* Python 3.7+
* OpenCV
* NumPy
* A hand detection / pose estimation library (e.g. MediaPipe, OpenPose, or custom model)
* (Optional) PyTorch / TensorFlow (if using custom neural networks)

Install via:

```bash
pip install opencv-python numpy mediapipe
```

(Or whatever is listed in your `requirements.txt`.)

## 📈 Results & Demo

Add screenshots or GIFs of your system in action here. For example:

![Demo Screenshot](path/to/screenshot.png)
*Fig: Two-hand manipulation of a virtual object*

## 🚀 Extensions & Future Work

* Gesture personalization
* Multi-object control
* Haptic / physical interface
* 3D object control
* Performance optimization

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome!

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/YourFeature`.
3. Commit changes and add tests.
4. Submit a Pull Request.

## 📝 License

[MIT License](LICENSE)

## 📞 Contact / Acknowledgments

* **Author**: [Sriram Sowmithri](https://github.com/sriramsowmithri9807)
* **Email**: [sowmithrisriram7@gmail.com](mailto:sowmithrisriram7@gmail.com)
* **Acknowledgments**: Thanks to OpenCV, MediaPipe, and other open-source tools used in this project.


