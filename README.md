# umamusume-reroller

NOT DONE, STILL SUCKS

```
pip install .
```

```
python main_monitor.py
```

# Attempts to run the game. If it's alreadt open it skips the step, feel free to change the path or just open it yourself before running. To work properly it should be at the main menu with no user data set (trainer ID: 0 if clicking it on the top left of the login screen)

delete user data step not working, I don't think the image recognition is working well. manually check and delete. hopefully the main repo will pick up the changes.

computer vision still not tested

Python script to automatically reroll on the Steam client with the 40 free rolls given initially, targeting two cards (Super Creek and Fine Motion)

Assumes that the game is running on a 1920x1080 monitor, should be relatively easy to modify for other resolutions though

Wait times can definitely be optimized (waiting for a connection-reliant menu to pop up instead of a static time, decreasing time after button presses etc.)

Uses opencv-python, PyAutoGUI, PyGetWindow, NumPy, keyboard, psutil

Scancode keypress code is taken from <https://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game>
