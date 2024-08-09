import cv2
import os
import sys
import torch
import argparse
import pathlib
import json
import time
from googletrans import Translator
from gtts import gTTS

base_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(base_dir, os.pardir))

# Fix for PosixPath on Windows
pathlib.PosixPath = pathlib.WindowsPath

# Configuration
model_path = os.path.join(base_dir, 'trained_model', 'best.pt')
resize_size = (256, 256)  # Resize images to 256x256
output_path = os.path.join(root_dir, 'static', 'annotated_results') 

# Create output directory if it doesn't exist
os.makedirs(output_path, exist_ok=True)

# Load model
try:
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)
    translator = Translator()
except Exception as e:
    print(f"Error initializing YOLOv5 model: {e}")
    raise

def translate_text(text, lang_code):
    """Translate text to the specified language."""
    translation = translator.translate(text, dest=lang_code)
    return translation.text

def text_to_speech(text, file_path):
    """Convert text to speech and save as an audio file."""
    tts = gTTS(text=text, lang=language_args)
    tts.save(file_path)

def process_frame(frame, language_args):
    """Perform inference on a single frame and draw bounding boxes."""

    results = model(frame)
    detections = results.xyxy[0].cpu().numpy()  # x1, y1, x2, y2, conf, cls
    detected_words = []
    translated_texts = []
    audio_files = []

    for *box, conf, cls in detections:
        x1, y1, x2, y2 = map(int, box)
        label = f"{model.names[int(cls)]} {conf:.2f}"
        detected_words.append(model.names[int(cls)])
        
        # Translate detected text
        translated_text = translate_text(model.names[int(cls)], language_args)
        translated_texts.append(translated_text)

        # Generate audio for translated text
        audio_file_name = f"{model.names[int(cls)]}.mp3"
        audio_file_path = os.path.join(output_path, audio_file_name)
        text_to_speech(translated_text, audio_file_path)
        audio_files.append(audio_file_name)
        
        # Draw bounding box with red color
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # Put label inside the bounding box
        label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        label_x1 = x1
        label_y1 = y1 - 10 if y1 - 10 > 10 else y1 + label_size[1] + 10
        cv2.rectangle(frame, (x1, label_y1 - label_size[1]), (x1 + label_size[0], label_y1), (0, 255, 0), -1)
        cv2.putText(frame, label, (x1, label_y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    return frame, detected_words, translated_texts, audio_files

def run_image_file(image_path):
    """Run object detection on a single image."""
    if not os.path.isfile(image_path):
        print(f"Error: Image file {image_path} not found.")
        return None

    # Start timing
    start_time = time.time()

    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image {image_path}.")
        return None

    # Resize the image
    image = cv2.resize(image, resize_size)

    # Process the image
    annotated_image, detected_words, translated_texts, audio_files = process_frame(image, language_args)

    # Save the result with a new name
    save_path = os.path.join(output_path, 'annotated_' + os.path.basename(image_path))
    cv2.imwrite(save_path, annotated_image)

    # End timing
    end_time = time.time()
    processing_time = round(end_time - start_time, 2)

    result = {
        'filename': os.path.basename(save_path),
        'detected_words': detected_words,
        'translated_texts': translated_texts,
        'audio_files': audio_files,
        'processing_time': processing_time
    }

    # Save the result as a JSON file
    try:
        json_save_path = os.path.join(output_path, 'result_' + os.path.splitext(os.path.basename(image_path))[0] + '.json')
        with open(json_save_path, 'w') as f:
            json.dump(result, f)
        print(f"JSON file saved successfully at {json_save_path}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")

    return result  # Return the path to the annotated image and additional data

def run_webcam():
    """Run object detection on webcam feed."""
    cap = cv2.VideoCapture(0)

    # Start timing
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from webcam.")
            break

        # Resize the frame
        frame = cv2.resize(frame, resize_size)

        # Process the frame
        try:
            processed_frame, detected_words, translated_texts, audio_files = process_frame(frame, language_args)
        except Exception as e:
            print(f"Error processing frame in YOLOv5: {e}")
            continue

        # Save the result with a fixed name
        save_path = os.path.join(output_path, f'webcam_output_{int(time.time())}.jpg')
        cv2.imwrite(save_path, processed_frame)
        print(f"Saving results to: {save_path}")

        # Save additional data
        result = {
            'filename': 'webcam_output.jpg',
            'detected_words': detected_words,
            'translated_texts': translated_texts,
            'audio_files': audio_files
        }

        # Save the result as a JSON file
        try:
            json_save_path = os.path.join(output_path, 'webcam_result.json')
            with open(json_save_path, 'w') as f:
                json.dump(result, f)
            print(f"JSON file saved successfully at {json_save_path}")
        except Exception as e:
            print(f"Error saving JSON file: {e}")

        # Display the resulting frame
        cv2.imshow('Webcam YOLOv5 Detection', processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # End timing
    end_time = time.time()
    processing_time = round(end_time - start_time, 2)

    # Update result with processing time
    result['processing_time'] = processing_time
    try:
        json_save_path = os.path.join(output_path, 'webcam_result.json')
        with open(json_save_path, 'w') as f:
            json.dump(result, f)
        print(f"JSON file updated with processing time at {json_save_path}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run YOLOv5 model')
    parser.add_argument('--webcam', action='store_true', help='Run webcam feed')
    parser.add_argument('image_file', nargs='?', help='Path to the image file')
    parser.add_argument('--lang', default='hi', help='Language code for translation')
    args = parser.parse_args()

    # Update language code for translation
    language_args = args.lang
    print(f"Selected language: {language_args}")

    if args.webcam:
        run_webcam()
    elif args.image_file:
        result = run_image_file(args.image_file)
        if result:
            print(json.dumps(result, indent=4))  # Output the result as JSON
    else:
        print("Please provide an image file or use --webcam for webcam mode.")
