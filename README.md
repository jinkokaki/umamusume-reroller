# umamusume-reroller

NOT DONE, STILL SUCKS

computer vision still not tested

Python script to automatically reroll on the Steam client with the 40 free rolls given initially, targeting two cards (Super Creek and Fine Motion)

Assumes that the game is running on a 1920x1080 monitor, should be relatively easy to modify for other resolutions though

Wait times can definitely be optimized (waiting for a connection-reliant menu to pop up instead of a static time, decreasing time after button presses etc.)

Uses opencv-python, PyAutoGUI, PyGetWindow, and NumPy

Scancode keypress code is taken from <https://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game>
