import cv2
import numpy as np
import os
import HandTrackingModule as htm
from datetime import datetime
import easyocr # for text recognition
import keyboard # for keyboard shortcuts

# Define the Size of the Brush and Eraser Thickness
brushThickness = 15
eraserThickness = 50

folderPath = "UI"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))
header = overlayList[0]
drawColor = (255, 0, 255)

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.65,maxHands=1)
xp, yp = 0, 0

# Create a Canva to Draw
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

# Add these after your existing initializations
reader = easyocr.Reader(['en']) # Initialize EasyOCR
save_directory = "saved_drawings"
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Add these functions
def save_canvas(canvas):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{save_directory}/drawing_{timestamp}.png"
    cv2.imwrite(filename, canvas)
    return filename

def recognize_text(image):
    # Convert to grayscale if not already
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Improve image quality for text recognition
    gray = cv2.GaussianBlur(gray, (3,3), 0)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Perform text recognition
    results = reader.readtext(binary)
    recognized_text = ' '.join([text[1] for text in results])
    return recognized_text

while True:

    # Import UI (Paint Tool Bar)
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Find Hand Landmarks on the Image
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:

        # Detect the Tip of the Index and Middle Finger
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Check which fingers are up
        fingers = detector.fingersUp()
        # print(fingers)

        # If Selection Mode - Two finger are up
        if fingers[1] and fingers[2]:
            # xp, yp = 0, 0
            print("Selection Mode")
            # # Checking for the click
            if y1 < 125:
                if 350 < x1 < 440:
                    header = overlayList[0]
                    drawColor = (0, 0, 255)
                elif 530 < x1 < 650:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                elif 700 < x1 < 820:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                elif 880 < x1 < 1000:
                    header = overlayList[3]
                    drawColor = (255, 255, 0)
                elif 1050 < x1 < 1170:
                    header = overlayList[4]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # If Drawing Mode - Index finger is up
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing Mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)

            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)

            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1


        # Clear Canvas when all fingers are up
        if all (x >= 1 for x in fingers):
            imgCanvas = np.zeros((720, 1280, 3), np.uint8)

    # To avoid the transperacy of the colours in canva
    # Convert Image to Gray
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    # Convert Image into Binary Image and Inverse to Previous
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)

    # Add and operation to change the binary colors of the brushes
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)


    # Setting the header image
    img[0:137, 0:1280] = header
    img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("Image", img)
    # cv2.imshow("Canvas", imgCanvas)
    # cv2.imshow("Inv", imgInv)
    cv2.waitKey(1)

    # Add these keyboard shortcuts
    if keyboard.is_pressed('s'):  # Press 's' to save
        saved_file = save_canvas(imgCanvas)
        print(f"Saved drawing to {saved_file}")
    
    if keyboard.is_pressed('t'):  # Press 't' to recognize text
        recognized_text = recognize_text(imgCanvas)
        print(f"Recognized Text: {recognized_text}")
        # Optionally save the text to a file
        with open(f"{save_directory}/recognized_text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", 'w') as f:
            f.write(recognized_text)