#Most of this code is shamelessly stolen from https://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
#In case the link dies at some point, the question was asked by user573949 and answered by hodka
#Not sure why I can't find a python module that specifically does scancode hardware inputs instead of virtual keyboard inputs?
#Umamusume seems to hook into keyboard inputs at a lower level so the keyboard module which relies on virtual keyboard inputs doesn't work

import ctypes
import time

# Scancode map for common characters on US QWERTY layout
CHAR_TO_SCANCODE = {
    'a': 0x1E, 'b': 0x30, 'c': 0x2E, 'd': 0x20, 'e': 0x12,
    'f': 0x21, 'g': 0x22, 'h': 0x23, 'i': 0x17, 'j': 0x24,
    'k': 0x25, 'l': 0x26, 'm': 0x32, 'n': 0x31, 'o': 0x18,
    'p': 0x19, 'q': 0x10, 'r': 0x13, 's': 0x1F, 't': 0x14,
    'u': 0x16, 'v': 0x2F, 'w': 0x11, 'x': 0x2D, 'y': 0x15,
    'z': 0x2C, '0': 0x0B, '1': 0x02, '2': 0x03, '3': 0x04,
    '4': 0x05, '5': 0x06, '6': 0x07, '7': 0x08, '8': 0x09,
    '9': 0x0A, ' ': 0x39, '\n': 0x1C
}

import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def pressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def releaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def tapKey(scancode, delay=0.05):
    pressKey(scancode)
    time.sleep(delay)
    releaseKey(scancode)

def tapChar(char):
    char = char.lower()
    if char in CHAR_TO_SCANCODE:
        scancode = CHAR_TO_SCANCODE[char]
        tapKey(scancode)
    else:
        raise ValueError(f"Character '{char}' not in scancode map.")
