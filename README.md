# 2d-uav-sim
## Running the app
In order to run the App you need to have python installed including pip and venv.
After cloning, run following commands in the project directory
### Windows
```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
### Linux
```
virtualenv -p python3 venv
source ./venv/bin/activate
pip install -r requirements.txt
python main.py
```
## Interaction
The simulator defaults to showcase mode where there is no way to interact with the app other than closing it with Escape or Ctrl+C. Debug mode can be activated using tilde ~
### Shortcuts
1. General
- / - pause the simulation
- R - reset the simulation
- 1 - toggle aircraft info
- 2 - toggle course trajectory
- 3 - toggle yaw angle trajectory
- 4 - toggle safezone
- 5 - toggle distance covered (paths)
2. Aircraft steering
- First aircraft
    - W - set 270° course
    - S - set 90° course
    - A - set 180° course
    - D - set 0° course
    - Y - decrease course by small iterator
    - U - increase course by small iterator
    - F2 - slow the aircraft down
    - F3 - speed the aircraft up
- Second aircraft
    - I - set 270° course
    - K - set 90° course
    - J - set 180° course
    - L - set 0° course
    - O - decrease course by small iterator
    - P - increase course by small iterator
    - F6 - slow the aircraft down
    - F7 - speed the aircraft up
