# 2D UAV Flight Simulator
Project implements simple Python3 application simulating flight of two independent UAVs utilizing collision avoidance algorithm in order to prevent aircraft crashing into each other. GUI is represented using PySide6[^1] library.
> [!NOTE]
> Project considers two aircrafts only.
## Running the app
In order to run the App you need to have Python3 installed including pip and PyQt6. This instruction makes use of venv/virtualenv avoiding need of installing whole PyQt library.
After cloning, run following commands in the project directory
### Windows
```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
> [!NOTE]
> Using venv in Windows requires accepting script running policy.
### Linux
```
virtualenv -p python3 venv
source ./venv/bin/activate
pip install -r requirements.txt
python main.py
```
> [!IMPORTANT]
> This process may vary depending on the OS used.
## Interaction
The simulator defaults to showcase mode where there is no way to interact with the app other than closing it with Escape or Ctrl+C. Debug mode can be activated using tilde ~
### Shortcuts
1. General
    - / - pause the simulation
    - R - reset the simulation
    - 1 - toggle aircraft info
    - 2 - toggle app info
    - 3 - toggle course trajectory
    - 4 - toggle yaw angle trajectory
    - 5 - toggle safezone
    - 6 - toggle distance covered (paths)
    - 7 - toggle second aircraft targeting first to crash
    - 8 - toggle hitboxes
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
## Progress
- [x] Run simulation and Gui separately
- [x] Add smooth angle transition
- [x] Add safezones and its handling
- [ ] Transition from PyQt6 to PySide6
- [ ] Add flight control computer (FCC) to handle setting destination and vectors
- [ ] Implement collision avoidance algorithm
[^1]: https://doc.qt.io/qtforpython-6/
