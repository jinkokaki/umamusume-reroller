import cv2
import pyautogui
import pygetwindow as gw
import numpy as np
from time import sleep

windowName = "Umamusume"
retryTime = 2
constants = "constants.txt"
birthInput = 199001
nameInput = "x"
agreeButton = "templates/agreeButton.png"
birthField = "templates/birthField.png"
cardBanner = "templates/cardBanner.png"
changeButton = "templates/changeButton.png"
closeButton = "templates/closeButton.png"
collectAllButton = "templates/collectAllButton.png"
deleteBox = "templates/deleteBox.png"
deleteButton = "templates/deleteButton.png"
menuButton = "templates/menuButton.png"
nameField = "templates/nameField.png"
nextButton = "templates/nextButton.png"
okButton = "templates/okButton.png"
privacyPolicy = "templates/privacyPolicy.png"
registerButton = "templates/registerButton.png"
rewardsIcon = "templates/rewardsIcon.png"
scoutAgainButton = "templates/scoutAgainButton.png"
scoutButton = "templates/scoutButton.png"
scoutIcon = "templates/scoutIcon.png"
skipButton = "templates/skipButton.png"
tenScoutButton = "templates/tenScoutButton.png"
termsOfUse = "templates/termsOfUse.png"
titleScreenButton = "templates/titleScreenButton.png"
cardOne = "targets/cardOne.png"
cardTwo = "targets/cardTwo.png"
cardOneCount = 0
cardTwoCount = 0

#thank you ChatGPT lmao
def multiScaleTemplateMatch(screenGray, templateGray, scaleRange=(0.5, 1.5), scaleSteps=30, threshold=0.7):
    bestVal = -1
    bestLoc = None
    bestScale = 1.0
    bestShape = None

    # Generate scales to test
    scales = np.linspace(scaleRange[0], scaleRange[1], scaleSteps)

    for scale in scales:
        scaledTemplate = cv2.resize(templateGray, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

        if scaledTemplate.shape[0] > screenGray.shape[0] or scaledTemplate.shape[1] > screenGray.shape[1]:
            continue  # Skip if template is larger than the screen

        result = cv2.matchTemplate(screenGray, scaledTemplate, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)

        if maxVal > bestVal:
            bestVal = maxVal
            bestLoc = maxLoc
            bestScale = scale
            bestShape = scaledTemplate.shape

    if bestVal >= threshold:
        return bestLoc, bestShape, bestScale
    else:
        return None, None, None

def grabUmamusumeWindow():
    try:
        window = gw.getWindowsWithTitle(windowName)[0]
    except IndexError:
        print(f"Umamusume not found running by application window name")
        return None
    window.activate()
    windowRegion = window._rect
    windowX, windowY = windowRegion.left, windowRegion.top
    return window, windowX, windowY

def waitFindAndClickImage(imagePath):
    window, windowX, windowY = grabUmamusumeWindow()
    template = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)

    while True:
        screenCapture = pyautogui.screenshot(region=(windowX, windowY, window.width, window.height))
        screenCapture = np.array(screenCapture)
        grayScreenCapture = cv2.cvtColor(screenCapture, cv2.COLOR_RGB2GRAY)

        matchLoc, matchShape, matchScale = multiScaleTemplateMatch(grayScreenCapture, template)
        if matchLoc is None:
            print(f"Image not found. Retrying in {retryTime}s")
            sleep(retryTime)
        else:
            print(f"Image found at {matchLoc} with size {matchShape}, clicking")
            centerX = matchLoc[0] + matchShape[1] // 2
            centerY = matchLoc[1] + matchShape[0] // 2
            centerX += windowX
            centerY += windowY
            pyautogui.click(centerX, centerY)
            break

def waitFindAndClickViewButton(imagePath):
    window, windowX, windowY = grabUmamusumeWindow()
    template = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)

    while True:
        screenCapture = pyautogui.screenshot(region=(windowX, windowY, window.width, window.height))
        screenCapture = np.array(screenCapture)
        grayScreenCapture = cv2.cvtColor(screenCapture, cv2.COLOR_RGB2GRAY)

        matchLoc, matchShape, matchScale = multiScaleTemplateMatch(grayScreenCapture, template)
        if matchLoc is None:
            print(f"Image not found. Retrying in {retryTime}s")
            sleep(retryTime)
        else:
            print(f"Image found at {matchLoc} with size {matchShape}, clicking")
            centerX = matchLoc[0] + matchShape[1] // 2
            centerY = matchLoc[1] + matchShape[0] // 2
            centerX += int(200 * matchScale)
            centerX += windowX
            centerY += windowY
            pyautogui.click(centerX, centerY)
            centerY += int(100 * matchScale)
            sleep(1)
            pyautogui.click(centerX, centerY)
            break

def tryFindAndClickImage(imagePath, click = True):
    window, windowX, windowY = grabUmamusumeWindow()
    template = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
    screenCapture = pyautogui.screenshot(region=(windowX, windowY, window.width, window.height))
    screenCapture = np.array(screenCapture)
    grayScreenCapture = cv2.cvtColor(screenCapture, cv2.COLOR_RGB2GRAY)

    matchLoc, matchShape, matchScale = multiScaleTemplateMatch(grayScreenCapture, template)
    if matchLoc is None:
        print(f"Image not found, returning false")
        return False
    else:
        print(f"Image found at {matchLoc} with size {matchShape}, returning true")
        centerX = matchLoc[0] + matchShape[1] // 2
        centerY = matchLoc[1] + matchShape[0] // 2
        centerX += windowX
        centerY += windowY
        if click:
            pyautogui.click(centerX, centerY)
        return True


def clickCenter():
    window, windowX, windowY = grabUmamusumeWindow()
    centerX = windowX + window.width // 2
    centerY = windowY + window.height // 2
    pyautogui.click(centerX, centerY)

def main():
    try:
        with open(constants, 'r') as file:
            birthInput = file.readline().strip()
            nameInput = file.readline().strip()
    except FileNotFoundError:
        print("constants.txt not found, should be placed in same directory as main.py")
    except Exception as e:
        print(f"{e}")
        print("Ensure that the first line is the birth year and month in the convention YYYYMM, and that the second line is the name")
    
    while True:
        # Click twice to get out of the opening credits and click again to start the game
        clickCenter()
        sleep(1)
        clickCenter()
        sleep(1)
        clickCenter()
        sleep(1)
        #Click on terms of use and privacy policy
        #waitFindAndClickImage(termsOfUse, True)
        #sleep(3)
        #waitFindAndClickImage(privacyPolicy, True)
        waitFindAndClickViewButton(termsOfUse)
        waitFindAndClickImage(agreeButton)
        sleep(2)
        #Click on and select default region
        waitFindAndClickImage(changeButton)
        waitFindAndClickImage(okButton)
        #Click on and enter birth YYYYMM
        waitFindAndClickImage(birthField)
        pyautogui.write(birthInput)
        waitFindAndClickImage(okButton)
        #Skip tutorial for the love of god
        waitFindAndClickImage(skipButton)
        #Click on and enter name
        waitFindAndClickImage(nameField)
        pyautogui.write(nameInput)
        waitFindAndClickImage(registerButton)
        waitFindAndClickImage(okButton)
        sleep(2)
        waitFindAndClickImage(okButton)
        #Skip like the million first rewards
        while tryFindAndClickImage(closeButton) is False:
            tryFindAndClickImage(nextButton)
            sleep(1)
        sleep(2)
        tryFindAndClickImage(closeButton)
        #Claim rewards
        waitFindAndClickImage(rewardsIcon)
        sleep(1)
        waitFindAndClickImage(collectAllButton)
        sleep(1)
        waitFindAndClickImage(closeButton)
        sleep(1)
        waitFindAndClickImage(closeButton)
        #Move to banner
        waitFindAndClickImage(scoutIcon)
        waitFindAndClickImage(cardBanner)
        #Pull baby pull
        waitFindAndClickImage(tenScoutButton)
        #Loop
        loopCount = 0
        while loopCount < 3:
            waitFindAndClickImage(scoutButton)
            waitFindAndClickImage(nextButton)
            sleep(3)
            #Scan for matching cards
            if tryFindAndClickImage(cardOne, False):
                cardOneCount += 1
            if tryFindAndClickImage(cardTwo, False):
                cardTwoCount += 1
            waitFindAndClickImage(scoutAgainButton)
            loopCount += 1
        #Finish the last (4th) pull
        waitFindAndClickImage(nextButton)
        if tryFindAndClickImage(cardOne, False):
            cardOneCount += 1
        if tryFindAndClickImage(cardTwo, False):
            cardTwoCount += 1
        #Check if card counts are sufficient
        if cardOneCount + cardTwoCount >= 2:
            return
        print(f"Card 1 count: {cardOneCount}, Card 2 count: {cardTwoCount}")
        #Insufficient, so delete data and try again
        cardOneCount = 0
        cardTwoCount = 0
        waitFindAndClickImage(titleScreenButton)
        sleep(1)
        clickCenter()
        sleep(1)
        clickCenter()
        waitFindAndClickImage(menuButton)
        waitFindAndClickImage(deleteBox)
        waitFindAndClickImage(deleteButton)
        sleep(1)
        waitFindAndClickImage(deleteButton)
        waitFindAndClickImage(closeButton)
        #Restart the main function

if __name__ == "__main__":
    main()
