import cv2
import pyautogui
import pygetwindow
import numpy as np
import time
import os
import threading
import keyboard
import psutil
import sys
from time import sleep
from scancodeinput import tapChar
from pywinauto.application import Application

constants = "constants.txt"
try:
    with open(constants, 'r') as file:
        birthInput = file.readline().strip()
        nameInput = file.readline().strip()
except FileNotFoundError:
    print("constants.txt not found, should be placed in same directory as main.py")
except Exception as e:
    print(f"{e}")
    print("Ensure that the first line is the birth year and month in the convention YYYYMM, and that the second line is the name")

cardRegion = (296, 112, 800, 900)
cardOne = "targets/cardOne.png"
cardTwo = "targets/cardTwo.png"
cardOneCount = 0
cardTwoCount = 0

# Global control
glbl_window = None
running = True
window_title = "Umamusume"

def grabUmamusumeWindow(wait_for_stability=True):
    global glbl_window

    if glbl_window is not None:
        return glbl_window

    last_window = None
    stable_count = 0

    print("Waiting for game window to appear and stabilize...")

    while True:
        windows = [
            w for w in pygetwindow.getWindowsWithTitle("Umamusume")
            if "Visual Studio Code" not in w.title and "main_monitor.py" not in w.title and len(w.title) <= 50
        ]

        if windows:
            current = windows[0]
            if last_window and current._hWnd == last_window._hWnd:
                stable_count += 1
            else:
                stable_count = 0
                last_window = current

            if not wait_for_stability or stable_count >= 5:
                try:
                    print(f"Found window: {current.title}")
                    # Use pywinauto to force focus
                    app = Application().connect(handle=current._hWnd)
                    app_window = app.window(handle=current._hWnd)
                    app_window.set_focus()
                    print("Window activated with pywinauto.")
                except Exception as e:
                    print(f"Window focus error: {e}")
                glbl_window = current
                return current

        else:
            print("Waiting for game window...")
            stable_count = 0
            last_window = None

        time.sleep(0.5)


def monitorWindow():
    global running, glbl_window
    while running:
        if glbl_window is None:
            time.sleep(5)
            continue
        try:
            if not glbl_window.isActive:
                print("Window lost focus. Re-activating...")
                glbl_window.activate()

            if not glbl_window.isActive:
                print("Window lost focus. Re-activating...")
                glbl_window.activate()
        except Exception as e:
            print(f"Monitor error: {e}")
        time.sleep(1)

def handle_exit(sig, frame):
    global running
    print("\n[!] Ctrl+C received. Exiting cleanly.")
    running = False
    sys.exit(0)

def multiScaleTemplateMatch(template):
    scaleRange = (0.75, 1.25)
    scaleSteps = 16
    threshold = 0.7
    bestVal = -1

    window = grabUmamusumeWindow()
    templateGrayscale = cv2.imread(template, cv2.IMREAD_GRAYSCALE)
    screenCapture = pyautogui.screenshot(region=cardRegion)
    screenGrayscale = cv2.cvtColor(np.array(screenCapture), cv2.COLOR_RGB2GRAY)

    for scale in np.linspace(scaleRange[0], scaleRange[1], scaleSteps):
        scaledTemplate = cv2.resize(templateGrayscale, (0, 0), fx=scale, fy=scale)
        if scaledTemplate.shape[0] > screenGrayscale.shape[0] or scaledTemplate.shape[1] > screenGrayscale.shape[1]:
            continue
        result = cv2.matchTemplate(screenGrayscale, scaledTemplate, cv2.TM_CCOEFF_NORMED)
        _, maxVal, _, _ = cv2.minMaxLoc(result)
        if maxVal > bestVal:
            bestVal = maxVal

    print(f"Template match confidence: {bestVal}")
    return bestVal >= threshold

def keyboard_listener():
    global running
    keyboard.wait('ctrl+c')
    print("\n[!] Ctrl+C pressed. Exiting cleanly.")
    running = False
    os._exit(0)  # force exit because input may hang

def is_game_running(process_name="UmamusumePrettyDerby.exe"):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False

def main():
    global glbl_window

    threading.Thread(target=keyboard_listener, daemon=True).start()

    exe_path = r"C:\\Program Files (x86)\\Steam\\steamapps\\common\\UmamusumePrettyDerby\\UmamusumePrettyDerby.exe"
    if not is_game_running():
        os.startfile(exe_path)
        print("Game launched.")
    else:
        print("Game already running. Skipping launch.")
    sleep(5)
    glbl_window = grabUmamusumeWindow()
    sleep(2)
    glbl_window.activate()
    sleep(2)
    threading.Thread(target=monitorWindow, daemon=True).start()
    sleep(3)

    # Insert the original game automation logic here
    reroll_loop()

def skip_opening_scenes():
    glbl_window.activate()
    sleep(2)
    pyautogui.click(1920 // 2, 1080 // 2)
    sleep(2)
    tapChar(' ')
    sleep(2)
    tapChar(' ')

def accept_terms_and_policy():
    sleep(3)
    tapChar('d')
    sleep(0.5)
    tapChar('w')
    sleep(0.3)
    tapChar(' ')
    sleep(0.3)
    pyautogui.hotkey('ctrl', 'w')  # Close Terms of Use

    sleep(1)
    glbl_window.activate()
    tapChar('s')
    sleep(0.5)
    tapChar(' ')
    sleep(0.3)
    pyautogui.hotkey('ctrl', 'w')  # Close Privacy Policy

    sleep(1)
    glbl_window.activate()
    tapChar('s')
    sleep(0.3)
    tapChar(' ')

def agree_and_set_birth():
    sleep(1)
    tapChar('w')
    sleep(0.3)
    tapChar('w')
    sleep(0.3)
    tapChar(' ')

    sleep(1)
    tapChar('s')
    sleep(0.3)
    tapChar('s')
    sleep(0.3)
    tapChar('s')
    sleep(0.3)
    tapChar(' ')

    sleep(1)
    tapChar('w')
    sleep(0.3)
    tapChar(' ')

    sleep(1)
    tapChar('w')
    sleep(0.3)
    tapChar(' ')
    sleep(0.3)
    pyautogui.write(birthInput)
    sleep(0.1)
    tapChar('\n')
    sleep(0.3)
    tapChar('s')
    sleep(0.3)
    tapChar('d')
    sleep(0.7)
    tapChar(' ')

def skip_tutorial():
    sleep(3)
    tapChar('s')
    sleep(0.5)
    tapChar(' ')

def input_name():
    sleep(3)
    tapChar('w')
    sleep(0.5)
    tapChar('w')
    sleep(0.5)
    tapChar(' ')
    sleep(1)
    pyautogui.write(nameInput)
    sleep(1)
    tapChar('\n')
    sleep(0.5)
    tapChar('s')
    sleep(0.5)
    tapChar('s')
    sleep(0.5)
    tapChar(' ')

def wait_for_download():
    sleep(7)
    tapChar('d')
    sleep(0.5)
    tapChar(' ')
    sleep(5)
    tapChar('s')
    sleep(0.5)
    tapChar('d')
    sleep(0.5)
    tapChar(' ')
    sleep(5)
    tapChar('s')
    sleep(1)
    tapChar('s')
    timeMarker = time.time()
    while (time.time() - timeMarker < 15):
        sleep(0.05)
        tapChar(' ')

def collect_rewards():
    tapChar('w')
    sleep(0.5)
    tapChar('w')
    sleep(0.5)
    tapChar(' ')
    sleep(3)
    tapChar('s')
    sleep(0.5)
    tapChar('s')
    sleep(0.5)
    tapChar('s')
    sleep(0.5)
    tapChar(' ')
    sleep(3)
    tapChar('a')
    sleep(0.5)
    tapChar(' ')
    sleep(2)
    tapChar('a')
    sleep(0.5)
    tapChar(' ')

def go_to_banner():
    sleep(2)
    tapChar('d')
    sleep(0.5)
    tapChar('d')
    sleep(0.5)
    tapChar('d')
    sleep(0.5)
    tapChar(' ')
    sleep(2)
    tapChar('w')
    sleep(0.5)
    tapChar('w')
    sleep(0.5)
    tapChar('w')
    sleep(0.5)
    tapChar('a')
    sleep(0.5)
    tapChar(' ')
    sleep(2)
    tapChar('s')
    sleep(0.5)
    tapChar('d')
    sleep(0.5)
    tapChar('d')
    sleep(0.5)
    tapChar(' ')
    sleep(0.5)
    sleep(2)
    tapChar('w')
    sleep(0.5)
    tapChar(' ')

def run_pull_loop():
    global cardOneCount, cardTwoCount
    pullCount = 1
    while pullCount < 4:
        sleep(3)
        tapChar('s')
        sleep(0.5)
        timeMarker = time.time()
        while (time.time() - timeMarker < 5):
            sleep(0.05)
            tapChar(' ')
        if multiScaleTemplateMatch(cardOne):
            cardOneCount += 1
            print("Card One detected")
        if multiScaleTemplateMatch(cardTwo):
            cardTwoCount += 1
            print("Card Two detected")
        sleep(0.5)
        pullCount += 1
        # Hit the scout again button
        tapChar('a')
        sleep(0.5)
        tapChar(' ')
        sleep(0.5)
        tapChar('w')
        sleep(0.5)
        tapChar(' ')

def check_result_or_reset():
    global cardOneCount, cardTwoCount
    if cardOneCount + cardTwoCount >= 2:
        print("Sufficient target cards pulled, stopping script")
        return True
    else:
        cardOneCount = 0
        cardTwoCount = 0
        return False

def reset_game_data():
    sleep(8)
    tapChar('d')
    sleep(0.9)
    tapChar('d')
    sleep(2)
    tapChar('d')
    sleep(0.9)
    tapChar('d')
    sleep(0.9)
    pyautogui.click(1920 // 2, 1080 // 2)
    sleep(6)
    tapChar(' ')
    sleep(0.5)
    tapChar('d')
    sleep(1)
    tapChar('w')
    sleep(1)
    tapChar(' ')
    sleep(0.5)
    tapChar('d')
    sleep(0.5)
    tapChar(' ')
    sleep(0.5)
    tapChar(' ')
    sleep(0.5)
    tapChar('a')
    sleep(0.5)
    tapChar(' ')
    sleep(0.5)
    tapChar('s')
    sleep(0.5)
    tapChar(' ')

def reroll_loop():
    while True:
        skip_opening_scenes()
        accept_terms_and_policy()
        agree_and_set_birth()
        skip_tutorial()
        input_name()
        wait_for_download()
        collect_rewards()
        go_to_banner()
        run_pull_loop()
        #Finish off the last bit of skipping
        sleep(3)
        tapChar('s')
        sleep(0.5)
        tapChar('s')
        sleep(0.5)
        timeMarker = time.time()
        while (time.time() - timeMarker < 5):
            sleep(0.05)
            tapChar(' ')
        if check_result_or_reset():
            import winsound
            for _ in range(10):
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
                sleep(0.5)  # small pause so it doesn't overlap
        
        # Needs work
        reset_game_data()

if __name__ == "__main__":
    main()
