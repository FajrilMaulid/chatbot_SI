#!/bin/bash
# Chatbot SI - Quick Setup for Linux/Mac
# This script will:
# - Check Python installation
# - Install dependencies
# - Setup database
# - Run migration
# - Start the application

echo "============================================================"
echo "   Chatbot SI - Automated Setup for Linux/Mac"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ from your package manager"
    exit 1
fi

echo "[OK] Python found: $(python3 --version)"
echo ""

# Check if MySQL/MariaDB is running
if command -v mysql &> /dev/null; then
    echo "[OK] MySQL found"
else
    echo "[WARN] MySQL not detected. Please ensure MySQL is installed"
fi
echo ""

# Run the main setup script
echo "Running setup.py..."
echo ""
python3 setup.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Setup failed!"
    echo "Please check the error messages above"
    exit 1
fi

echo ""
echo "============================================================"
echo "   Setup Complete!"
echo "============================================================"
echo ""
echo "Would you like to start the application now? (y/N)"
read -r choice

if [[ "$choice" =~ ^[Yy]$ ]]; then
    echo ""
    echo "Starting application..."
    python3 app.py
else
    echo ""
    echo "To start the application later, run: python3 app.py"
    echo ""
fi
