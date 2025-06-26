import cv2
import pyautogui
import pygetwindow
import numpy as np
import time
from time import sleep
from scancodeinput import tapChar

constants = "constants.txt"
birthInput = 199001
nameInput = "x"
cardRegion = (296, 112, 800, 900)
cardOne = "targets/cardOne.png"
cardTwo = "targets/cardTwo.png"
cardOneCount = 0
cardTwoCount = 0

def grabUmamusumeWindow():
    umamusumeWindow = None
    try:
        #For some reason getWindowsWithTitle does a search for windows containing the parameter and not exact matches
        windows = pygetwindow.getWindowsWithTitle("Umamusume")
        for window in windows:
            #Check for exact match
            if window.title == "Umamusume":
                umamusumeWindow = window
        if umamusumeWindow is None:
            raise TypeError
    except TypeError:
        print(f"Umamusume not found running by application window name")
        return None
    umamusumeWindow.maximize()
    umamusumeWindow.activate()
    return umamusumeWindow

#Thanks ChatGPT lmao
def multiScaleTemplateMatch(template):
    scaleRange = (0.75, 1.25)
    scaleSteps = 16
    threshold = 0.7
    bestVal = -1
    bestLoc = None
    bestScale = 1.0
    bestShape = None

    window = grabUmamusumeWindow()
    templateGrayscale = cv2.imread(template, cv2.IMREAD_GRAYSCALE)
    screenCapture = pyautogui.screenshot(region = (cardRegion[0], cardRegion[1], cardRegion[2], cardRegion[3]))
    screenCapture = np.array(screenCapture)
    screenGrayscale = cv2.cvtColor(screenCapture, cv2.COLOR_RGB2GRAY)

    scales = np.linspace(scaleRange[0], scaleRange[1], scaleSteps)

    for scale in scales:
        scaledTemplate = cv2.resize(templateGrayscale, (0, 0), fx = scale, fy = scale, interpolation = cv2.INTER_AREA)

        if scaledTemplate.shape[0] > screenGrayscale.shape[0] or scaledTemplate.shape[1] > screenGrayscale.shape[1]:
            continue

        result = cv2.matchTemplate(screenGrayscale, scaledTemplate, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)

        if maxVal > bestVal:
            bestVal = maxVal
            bestLoc = maxLoc
            bestScale = scale
            bestShape = scaledTemplate.shape
    
    if bestVal >= threshold:
        return True
    else:
        return False

def main():
    window = grabUmamusumeWindow()

    try:
        with open(constants, 'r') as file:
            birthInput = file.readline().strip()
            nameInput = file.readline().strip()
    except FileNotFoundError:
        print("constants.txt not found, should be placed in same directory as main.py")
    except Exception as e:
        print(f"{e}")
        print("Ensure that the first line is the birth year and month in the convention YYYYMM, and that the second line is the name")

    #while True:
    #    sleep(1)
    #    cursorX, cursorY = pyautogui.position()
    #    print(f"cursorX: {cursorX}, cursorY: {cursorY}")

    while True:
        window.activate()
        #Skip opening scenes
        sleep(2)
        pyautogui.click(1920 // 2, 1080 // 2)
        sleep(2)
        tapChar(' ')
        #Tap to start
        sleep(2)
        tapChar(' ')
        #Move to terms of use
        sleep(3)
        tapChar('d')
        sleep(0.5)
        tapChar('w')
        sleep(0.5)
        tapChar(' ')
        #Refocus and move to privacy policy
        sleep(2)
        window.activate()
        tapChar('s')
        sleep(0.5)
        tapChar(' ')
        #Refocus and move to agree
        sleep(2)
        window.activate()
        tapChar('s')
        sleep(0.5)
        tapChar(' ')
        #Move to change
        sleep(2)
        tapChar('w')
        sleep(0.5)
        tapChar('w')
        sleep(0.5)
        tapChar(' ')
        #Move to ok
        sleep(2)
        tapChar('s')
        sleep(0.5)
        tapChar('s')
        sleep(0.5)
        tapChar('s')
        sleep(0.5)
        tapChar(' ')
        #Move to ok
        sleep(2)
        tapChar('w')
        sleep(0.5)
        tapChar(' ')
        #Move to input birth
        sleep(2)
        tapChar('w')
        sleep(0.5)
        tapChar(' ')
        sleep(0.5)
        pyautogui.write(birthInput)
        sleep(0.5)
        tapChar('\n')
        sleep(0.5)
        tapChar('s')
        sleep(0.5)
        tapChar('d')
        sleep(0.5)
        tapChar(' ')
        #Wait and skip tutorial
        sleep(5)
        tapChar('s')
        sleep(0.5)
        tapChar(' ')
        #Move to input name
        sleep(2)
        tapChar('w')
        sleep(0.5)
        tapChar('w')
        sleep(0.5)
        tapChar(' ')
        sleep(0.5)
        pyautogui.write(nameInput)
        sleep(0.5)
        tapChar('\n')
        sleep(0.5)
        tapChar('s')
        sleep(0.5)
        tapChar('s')
        sleep(0.5)
        tapChar(' ')
        #Move to ok
        sleep(2)
        tapChar('d')
        sleep(0.5)
        tapChar(' ')
        #Wait for download
        sleep(5)
        tapChar('s')
        sleep(0.5)
        tapChar('d')
        sleep(0.5)
        tapChar(' ')
        #Wait for download to finish, then mash to skip
        sleep(5)
        tapChar('s')
        timeMarker = time.time()
        while (time.time() - timeMarker < 10):
            sleep(0.05)
            tapChar(' ')
        #Move to rewards
        tapChar('w')
        sleep(0.5)
        tapChar('w')
        sleep(0.5)
        tapChar(' ')
        #Move to collect all
        sleep(3)
        tapChar('s')
        sleep(0.5)
        tapChar('s')
        sleep(0.5)
        tapChar('s')
        sleep(0.5)
        tapChar(' ')
        #Move to close
        sleep(3)
        tapChar('a')
        sleep(0.5)
        tapChar(' ')
        #Move to close
        sleep(2)
        tapChar('a')
        sleep(0.5)
        tapChar(' ')
        #Move to banners
        sleep(2)
        tapChar('d')
        sleep(0.5)
        tapChar('d')
        sleep(0.5)
        tapChar('d')
        sleep(0.5)
        tapChar(' ')
        #Move to card banner
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
        #Move to 10x scout
        sleep(2)
        tapChar('s')
        sleep(0.5)
        tapChar('d')
        sleep(0.5)
        tapChar('d')
        sleep(0.5)
        tapChar(' ')
        sleep(0.5)
        #Move to scout
        sleep(2)
        tapChar('w')
        sleep(0.5)
        tapChar(' ')
        #Pull loop
        pullCount = 1
        while pullCount <= 4:
            sleep(3)
            tapChar('s')
            sleep(0.5)
            timeMarker = time.time()
            while (time.time() - timeMarker > 5):
                sleep(0.05)
                tapChar(' ')
            #Computer vision time
            if multiScaleTemplateMatch(cardOne):
                cardOneCount += 1
                print("Card One detected")
            if multiScaleTemplateMatch(cardTwo):
                cardTwoCount += 1
                print("Card Two detected")
            sleep(0.5)
            pullCount += 1
            tapChar('a')
            sleep(0.5)
            tapChar(' ')
            sleep(0.5)
            tapChar('w')
            sleep(0.5)
            tapChar(' ')
        #Move to title screen
        sleep(0.5)
        tapChar('d')
        sleep(0.5)
        tapChar('d')
        #Skip opening scenes
        sleep(2)
        pyautogui.click(1920 // 2, 1080 // 2)
        sleep(2)
        tapChar(' ')
        #Move to menu
        sleep(0.5)
        tapChar('d')
        sleep(0.5)
        tapChar('w')
        sleep(0.5)
        tapChar(' ')
        #Delete data
        sleep(0.5)
        tapChar('d')
        sleep(0.5)
        tapChar(' ')
        sleep(0.5)
        tapChar(' ')
        sleep(0.5)
        tapChar('s')
        sleep(0.5)
        tapChar(' ')
        #Return to beginning of loop


if __name__ == "__main__":
    main()
