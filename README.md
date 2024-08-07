# Indian Sign Language Detection Application

This project is a Indian Sign Language Detection web application that allows users to upload images, videos, or use their webcam to perform object detection using YOLO models (YOLOv5 or YOLOv10). The detected objects can be translated into various Indian languages, and the translated text can be converted to speech.

## Features

- Upload images and videos or use the webcam for object detection
- Choose between YOLOv5 and YOLOv8 models
- Translate detected text into various Indian languages
- Text-to-speech conversion for translated text
- Reset button to clear results

## Requirements

- Python 3.7 or higher
- Pip (Python package installer)

## Installation

1. Clone the repository:

```sh
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment
```sh
python -m venv venv
```
3. Activate the virtual environment
```sh
venv\Scripts\activate (Windows)
venv\Scripts\activate (Mac OS)
myenv\Scripts\activate     
```
4. Install the required dependencies
```sh
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask application
```sh
python app.py
```
2. Open your web browser and go to `http://127.0.0.1:5000`.

## File Structure
.
├── app.py                # Main Flask application
├── static/               # Static files (CSS, JS, etc.)
│   └── style.css         # CSS styles
├── templates/            # HTML templates
│   └── index.html        # Main HTML template
├── trained_model/        # Trained Best models
│   ├── yolov5/best.pt    # Trained YOLOv5 model
│   └── yolov10/best.pt   # Trained YOLOv10 model
├── models/               # YOLO models
│   ├── yolov5.py         # YOLOv5 model handling
│   └── yolov10.py        # YOLOv10 model handling
├── temp/                 # Directory for uploaded files
├── requirements.txt      # List of dependencies
└── README.md             
