# owenBot Server
PySide6 app to control owenBot over a websocket server. The server feeds commands to the robot based on user input through the custom Joystick and D-Pad widgets.

<img width="597" height="505" alt="image" src="https://github.com/user-attachments/assets/d26df61a-37c6-4edf-a277-8f378e48c89b" />

## Download
Get the latest build [here](https://github.com/WilliamFlinchbaugh/owenbot_server/releases/latest)

## Setup Guide
This was built and tested for Python 3.13.5, but should work on earlier versions. You can use either conda/miniforge or virtualenv for your environment.

Clone the repository and open a terminal in it's directory.

### Conda/miniforge: 

```
conda env create -f environment.yml
conda activate owenbot
```

### Virtualenv: 
Windows:
```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Linux/MacOS:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Build Guide
Build the executable with:

`pyinstaller main.py --onefile -w -i owen.ico -n owenbot_server`

The executable will be available in the dist folder.

