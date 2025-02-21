#!/bin/bash

# Check if Python 3.11 is installed
if ! command -v python3.11 &> /dev/null; then
    echo "Error: Python 3.11 is required but not found."
    echo "Please install Python 3.11 from https://www.python.org/downloads/ and try again."
    exit 1
fi

echo "Python 3.11 found."

echo "Checking for virtual environment..."

# Check if the 'venv' folder exists
if [ -d "venv" ]; then
    echo "Virtual environment found. Activating..."
    source venv/bin/activate
else
    echo "Virtual environment not found. Creating one with Python 3.11..."
    python3.11 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
fi

echo "Launching the app..."
python main.py