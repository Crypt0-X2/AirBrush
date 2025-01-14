# AirCanvas: Virtual Drawing with Hand Gestures

## Overview
AirCanvas is a computer vision-based drawing application that allows users to draw in the air using hand gestures. The application tracks hand movements through a webcam and converts them into digital drawings in real-time. It also features handwriting recognition capabilities to convert drawings into digital text.

## Features
- Real-time hand gesture tracking
- Multiple color options
- Eraser tool
- Clear canvas functionality
- Save drawings as images
- Handwriting recognition
- Keyboard shortcuts

## Requirements
- Python 3.8+
- Webcam
- Required packages listed in `requirements.txt`

## Installation
1. Clone the repository:
```

2. Create a virtual environment (recommended):
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
1. Run the main application:
```bash
python VirtualPainter.py
```

2. Hand Gestures:
- Index finger up: Drawing mode
- Index + Middle fingers up: Selection mode
- All fingers up: Clear canvas

3. Keyboard Shortcuts:
- 'S': Save current drawing
- 'T': Recognize and save text from drawing
- 'Q': Quit application

## Project Structure
```
AirCanvas/
├── HandTrackingModule.py    # Hand tracking implementation
├── VirtualPainter.py        # Main application
├── UI/                      # UI assets
│   ├── header1.png         # Red color tool
│   ├── header2.png         # Blue color tool
│   ├── header3.png         # Green color tool
│   ├── header4.png         # Yellow color tool
│   └── header5.png         # Eraser tool
├── saved_drawings/          # Directory for saved drawings
├── requirements.txt         # Project dependencies
└── README.md               # Project documentation
```

## Dependencies
See `requirements.txt` for detailed dependencies.

## Contributing
Feel free to fork the project and submit pull requests for any improvements.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
```

</rewritten_file>