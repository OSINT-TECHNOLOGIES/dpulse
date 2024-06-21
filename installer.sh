#!/bin/bash

echo "Select appropriate menu item"
echo "[1] Clone repository and install requirements"
echo "[2] Only install requirements"
read -p "Enter the number: " UserChoice

if [ "$UserChoice" == "1" ]; then
    echo "Cloning repository and installing requirements..."
    git clone https://github.com/OSINT-TECHNOLOGIES/dpulse
    cd dpulse
    pip install -r requirements.txt
elif [ "$UserChoice" == "2" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
else
    echo "Incorrect choice."
fi

echo "Installation end."
