#!/bin/bash
# Quick Start Script for RAG PDF Assistant (Linux/Mac)

echo "====================================="
echo "RAG PDF Assistant - Quick Start"
echo "====================================="
echo

echo "Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python not found! Please install Python 3.8 or higher."
    exit 1
fi

echo
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

echo
echo "Activating virtual environment..."
source venv/bin/activate

echo
echo "Installing dependencies..."
pip install -r requirements.txt

echo
echo "====================================="
echo "Installation complete!"
echo "====================================="
echo
echo "To run the application:"
echo "  1. Backend: python main.py"
echo "  2. Frontend: streamlit run app.py"
echo
