import cv2
import pyautogui
import pygetwindow as gw
import numpy as np
import keyboard
import sys
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
orbTemplate = cv2.ORB_create(250, float(1.2), 8, 1)
orbScreen = cv2.ORB_create(5000)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

#this is bad programming
try:
    window = gw.getWindowsWithTitle(windowName)[0]
except IndexError:
    print(f"Umamusume not found running by application window name")
window.activate()
windowRegion = window._rect
windowX, windowY = windowRegion.left, windowRegion.top

#thank you ChatGPT lmao
def orbTemplateMatch(screenGray, templateGray, ratio=0.95, minMatchCount=50):
    templateKeypoints, templateDescriptors = orbTemplate.detectAndCompute(templateGray, None)
    screenKeypoints, screenDescriptors = orbScreen.detectAndCompute(screenGray, None)
    outputTemplateImage = cv2.drawKeypoints(templateGray, templateKeypoints, 0, (0, 0, 255), flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
    outputScreenImage = cv2.drawKeypoints(screenGray, screenKeypoints, 0, (0, 0, 255), flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
    cv2.imwrite("templateKeypoints.png", outputTemplateImage)
    cv2.imwrite("screenKeypoints.png", outputScreenImage)

    matches = bf.knnMatch(templateDescriptors, screenDescriptors, k=2)
    goodMatches = []

    for m, n in matches:
        if m.distance < ratio * n.distance:
            goodMatches.append(m)

    if len(goodMatches) >= minMatchCount:
        templateMatchPoints = np.float32([templateKeypoints[m.queryIdx].pt for m in goodMatches]).reshape(-1, 1, 2)
        screenMatchPoints = np.float32([screenKeypoints[m.trainIdx].pt for m in goodMatches]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(templateMatchPoints, screenMatchPoints, cv2.RANSAC, 5.0)
        if M is None:
            print("Homography could not be computed")
            return None, None, None
        else:
            h, w = templateGray.shape
            templateCorners = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
            templateCornersTransformed = cv2.perspectiveTransform(templateCorners, M)

            center = templateCornersTransformed.mean(axis=0).flatten()
            centerX, centerY = int(center[0]), int(center[1])

            templateWidth = np.linalg.norm(templateCorners[0] - templateCorners[3])
            transformedWidth = np.linalg.norm(templateCornersTransformed[0] - templateCornersTransformed[3])
            scaleRatio = transformedWidth / templateWidth

            print(f"Match found. Center: ({centerX}, {centerY})")
            return centerX, centerY, scaleRatio
    else:
        print("Not enough matches")
        return None, None, None

def waitFindAndClickImage(imagePath, viewButton=False):
    template = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)

    while True:
        window.activate()

        screenCapture = pyautogui.screenshot(region=(windowX, windowY, window.width, window.height))
        screenCapture = np.array(screenCapture)
        grayScreenCapture = cv2.cvtColor(screenCapture, cv2.COLOR_RGB2GRAY)

        centerX, centerY, scaleRatio = orbTemplateMatch(grayScreenCapture, template)
        if centerX is None:
            print(f"Image not found. Retrying in {retryTime}s")
            sleep(retryTime)
        else:
            centerX += windowX
            centerY += windowY
            if viewButton:
                centerX += int(200 * scaleRatio)
            pyautogui.click(centerX, centerY)
            break

def tryFindAndClickImage(imagePath, click=True, nameField=False):
    template = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
    window.activate()
    screenCapture = pyautogui.screenshot(region=(windowX, windowY, window.width, window.height))
    screenCapture = np.array(screenCapture)
    grayScreenCapture = cv2.cvtColor(screenCapture, cv2.COLOR_RGB2GRAY)

    centerX, centerY, scaleRatio = orbTemplateMatch(grayScreenCapture, template)
    if centerX is None:
        print(f"Image not found. Returning false")
        return False
    else:
        centerX += windowX
        centerY += windowY
        if nameField:
            centerX += int(50 * scaleRatio)
        if click:
            pyautogui.click(centerX, centerY)
        return True

def clickCenter():
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
    
    print("Hold spacebar to kill the script")
    while not keyboard.is_pressed('space'):
        # Click twice to get out of the opening credits and click again to start the game
        clickCenter()
        sleep(1)
        clickCenter()
        sleep(1)
        clickCenter()
        sleep(1)
        #Click on terms of use and privacy policy
        waitFindAndClickImage(termsOfUse, True)
        waitFindAndClickImage(privacyPolicy, True)
        sleep(1)
        waitFindAndClickImage(agreeButton)
        sleep(2)
        #Click on and select default region
        waitFindAndClickImage(changeButton)
        sleep(1)
        waitFindAndClickImage(okButton)
        sleep(1)
        waitFindAndClickImage(okButton)
        sleep(1)
        #Click on and enter birth YYYYMM
        waitFindAndClickImage(birthField)
        pyautogui.write(birthInput)
        sleep(2)
        waitFindAndClickImage(okButton)
        sleep(5)
        #Skip tutorial for the love of god
        waitFindAndClickImage(skipButton)
        sleep(1)
        #Click on and enter name
        waitFindAndClickImage(nameField, True, True)
        pyautogui.write(nameInput)
        waitFindAndClickImage(registerButton)
        sleep(1)
        waitFindAndClickImage(okButton)
        sleep(2)
        waitFindAndClickImage(okButton)
        #Skip like the million first rewards
        while tryFindAndClickImage(closeButton) is False:
            tryFindAndClickImage(nextButton)
            sleep(1)
        sleep(2)
        tryFindAndClickImage(closeButton)
        sleep(1)
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
        sleep(2)
        waitFindAndClickImage(cardBanner)
        sleep(2)
        #Pull baby pull
        waitFindAndClickImage(tenScoutButton)
        #Loop
        loopCount = 0
        while loopCount < 3:
            waitFindAndClickImage(scoutButton)
            sleep(1)
            waitFindAndClickImage(nextButton)
            sleep(3)
            #Scan for matching cards
            if tryFindAndClickImage(cardOne, False):
                cardOneCount += 1
            if tryFindAndClickImage(cardTwo, False):
                cardTwoCount += 1
            waitFindAndClickImage(scoutAgainButton)
            sleep(1)
            loopCount += 1
        #Finish the last (4th) pull
        waitFindAndClickImage(nextButton)
        sleep(1)
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
        sleep(1)
        waitFindAndClickImage(deleteBox)
        sleep(1)
        waitFindAndClickImage(deleteButton)
        sleep(1)
        waitFindAndClickImage(deleteButton)
        sleep(1)
        waitFindAndClickImage(closeButton)
        #Restart the main function
    sys.exit()

if __name__ == "__main__":
    main()
