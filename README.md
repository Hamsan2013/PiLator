# PiLator v2 🚀

PiLator is a lightweight Raspberry Pi launcher to run Windows `.exe` apps using Wine.

## Features
- Simple GUI (Tkinter)
- Add & manage EXE files
- Run EXE using Wine
- System monitoring (CPU & RAM)

## Requirements
```bash
sudo apt update
sudo apt install python3-tk python3-psutil wine -y
```

## Run
```bash
python3 pilator.py
```

## Notes
- Designed for Raspberry Pi 3
- Works best with lightweight Windows apps
- For better compatibility, install Box86

## Future Plans
- Dark mode
- Game mode
- Auto Wine setup
- Better UI
