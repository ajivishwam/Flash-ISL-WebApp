import os
import subprocess
import json
from pathlib import Path
from flask import Flask, request, redirect, render_template, flash, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'isl'

# Base directory
base_dir = Path(__file__).resolve().parent

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ANNOTATED_FOLDER = 'static/annotated_results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ANNOTATED_FOLDER'] = ANNOTATED_FOLDER

# Ensure upload and annotated folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ANNOTATED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run_model_v5(filepath, model='yolov5', is_webcam=False):
    try:
        if model == 'yolov5':
            model_command = [
                str(base_dir / 'FinalYolov5' / 'myenv1' / 'Scripts' / 'python.exe'),
                str(base_dir / 'FinalYolov5' / 'run_model_v5.py')
            ]
        elif model == 'yolov10':
            model_command = [
                str(base_dir / 'FinalYolov10' / 'testenv' / 'Scripts' / 'python.exe'),
                str(base_dir / 'FinalYolov10' / 'run_model_v10.py')
            ]
        else:
            flash('Invalid model selection.')
            return None, None

        if is_webcam:
            command = model_command + ['--webcam']

            result_file_json = os.path.join(app.config['ANNOTATED_FOLDER'], 'webcam_result.json')
        else:
            command = model_command + [filepath]

            result_file = os.path.join(app.config['ANNOTATED_FOLDER'], 'annotated_' + os.path.basename(filepath))
            json_filename = 'result_' + os.path.splitext(os.path.basename(filepath))[0] + '.json'
            result_file_json = os.path.join(app.config['ANNOTATED_FOLDER'], json_filename)
        
        print(f"Running command: {' '.join(command)}")

        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"Subprocess output: {result.stdout}")
        print(f"Subprocess error: {result.stderr}")

        if os.path.exists(result_file_json):
            with open(result_file_json, 'r') as f:
                result_data = json.load(f)
            
            return result_file, result_data
        else:
            flash('Output file not found.')
            return None, None

    except subprocess.CalledProcessError as e:
        print(f"Subprocess error: {e.stderr}")
        flash('Error running the model.')
        return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        model = request.form.get('model', 'yolov5')  # Default to 'yolov5'
        language = request.form.get('language', 'hi')  # Default to 'hi'

        if 'file' in request.files:
            file = request.files['file']

            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                print(f"File saved to {filepath}")

                # Run the model on the uploaded file
                result_file, result_data = run_model_v5(filepath, model=model)
                print(f"Result file: {result_file}, Result data: {result_data}")

                if result_file:
                    detected_words = result_data.get('detected_words', [])
                    translated_texts = result_data.get('translated_texts', [])
                    audio_files = result_data.get('audio_files', [])
                    
                    if detected_words or translated_texts or audio_files:
                        zipped_data = zip(detected_words, translated_texts, audio_files)
                    else:
                        zipped_data = []

                    return render_template('result.html', 
                                           filename=os.path.basename(result_file),
                                           zipped_data=zipped_data,
                                           processing_time=result_data.get('processing_time', 'N/A'))
                else:
                    return redirect(request.url)
        elif 'webcam' in request.form:
            # Run the model for webcam
            result_file, result_data = run_model_v5(is_webcam=True, model=model)
            print(f"Webcam result file: {result_file}, Result data: {result_data}")

            if result_file:
                # Prepare zipped data for the template
                zipped_data = zip(
                    result_data.get('detected_words', []),
                    result_data.get('translated_texts', []),
                    result_data.get('audio_files', [])
                )
                return render_template('result.html', 
                                       filename='webcam_output.jpg',
                                       zipped_data=zipped_data,
                                       processing_time=result_data.get('processing_time', 'N/A'))
            else:
                return redirect(request.url)

    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/annotated_results/<filename>')
def annotated_file(filename):
    return send_from_directory(app.config['ANNOTATED_FOLDER'], filename)

@app.route('/audio/<filename>')
def audio_file(filename):
    return send_from_directory(app.config['ANNOTATED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
