#!/bin/bash

read -p "Do you want to start the installer? [Y/N]: " UserInput
if [[ "${UserInput^^}" != "Y" ]]; then
    exit 0
fi

echo

Menu() {
    echo "Select an appropriate menu item:"
    echo "[1] Clone repository and install requirements"
    echo "[2] Only install requirements"
    read -p "Enter the number: " UserChoice
    echo

    if [[ "${UserChoice}" == "1" ]]; then
        CloneAndInstall
    elif [[ "${UserChoice}" == "2" ]]; then
        InstallDependencies
    else
        echo "Incorrect choice."
        echo
        Menu
    fi
}

CloneAndInstall() {
    echo "Cloning repository and installing requirements..."
    git clone https://github.com/OSINT-TECHNOLOGIES/dpulse
    cd dpulse || exit 1
    pip install -r requirements.txt

    echo
}

InstallDependencies() {
    echo "Installing requirements..."
    pip install -r requirements.txt

    echo
}

End() {
    echo "Installation end."
    echo
    read -p "Press Enter to continue..."
}

Menu
End
