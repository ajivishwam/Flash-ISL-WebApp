# Indian Sign Language Detection and Translation Application

This project is a Indian Sign Language Detection web application that allows users to upload static sign images, or use their webcam to perform Indian Sign Language(ISL) detection using YOLO models (YOLOv5 or YOLOv10). The detected signs can be translated into various Indian languages, and the translated text can be converted to speech.

## Features

- Upload static sign images or use the webcam for sign detection
- Choose between YOLOv5 and YOLOv10 models
- Translate detected text into various Indian languages
- Text-to-speech conversion for translated text
- Go back button to clear results

## Requirements

- Python 3.8 or higher
- Pip (Python package installer)

## Installation

1. Clone the repository:

```sh
git clone https://github.com/ajivishwam/Flash-ISL-WebApp.git
cd Flash-ISL-WebApp
```
2. Install the required dependencies
```sh
pip install -r requirements.txt
```
3. Create a virtual environment for FinalYOLOv5. 
Run the below script using Git Bash or shell that support `.sh` files
```sh
cd FinalYOLOv5/
.setup.sh
```
4. Create a virtual environment for FinalYOLOv10. 
Run the below script using Git Bash or shell that support `.sh` files
```sh
cd FinalYOLOv10/
.setup.sh
```

## Running the Application

1. Start the Flask application
```sh
python app.py
```
2. Open your web browser and go to `http://127.0.0.1:5000`.

## Folder Structure
```sh
├── app.py
├── FinalYolov5/               
│   └── run_model_v5.py 
├── FinalYolov10/               
│   └── run_model_v10.py             
├── static/               
│   └── css/ 
│       └── style.css
│   └── annotated_results/ 
│   └── uploads/          
├── templates/            
│   └── index.html 
|   └── result.html       
├── trained_model/        
│   ├── yolov5/best.pt    
│   └── yolov10/best.pt   
├── models/               
│   ├── yolov5.py        
│   └── yolov10.py        
├── temp/                 
├── requirements.txt      
└── README.md  

```
