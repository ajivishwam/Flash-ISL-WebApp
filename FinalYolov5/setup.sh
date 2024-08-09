#!/bin/bash

# Check OS and set the appropriate commands
if [[ "$OSTYPE" == "msys" ]]; then
    # For Windows
    VENV_ACTIVATE="myenv1\\Scripts\\activate"
    PIP="pip"
else
    # For macOS/Linux
    VENV_ACTIVATE="source myenv1/bin/activate"
    PIP="pip3"
fi

# Create a virtual environment
python -m venv myenv1

# Activate the virtual environment
echo "Activating virtual environment..."
eval $VENV_ACTIVATE

# Install dependencies
echo "Installing dependencies..."
$PIP install gtts
$PIP install googletrans==4.0.0-rc1
$PIP install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0
$PIP install opencv-python
$PIP install opencv-python-headless
$PIP install pandas

echo "Setup completed!"
