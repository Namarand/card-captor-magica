import cv2
import numpy as np

def detect_card(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted([ (cv2.contourArea(i), i) for i in contours ], key=lambda a:a[0], reverse=True)
    _, card_contour = sorted_contours[1]
    _, image_contour = sorted_contours[3]
    rect = cv2.minAreaRect(card_contour)
    points = cv2.boxPoints(rect)
    points = np.int0(points)
    rect = cv2.minAreaRect(image_contour)
    points = cv2.boxPoints(rect)
    points = np.int0(points)
    capture_title(card_contour, image_contour)

def capture_title(card_contour, image_contour):
    # create a min area rectangle from our contour
    card_rect = cv2.minAreaRect(card_contour)
    image_rect = cv2.minAreaRect(image_contour)

    card_box = cv2.boxPoints(card_rect)
    cardbox = np.int0(card_box)
    image_box = cv2.boxPoints(image_rect)
    image_box = np.int0(image_box)

    # create empty initialized rectangle
    rect = np.zeros((4, 2), dtype = "float32")

    # get top points
    s = card_box.sum(axis = 1)
    rect[0] = card_box[np.argmin(s)]
    diff = np.diff(card_box, axis = 1)
    rect[1] = card_box[np.argmin(diff)]

    # get bottom points
    s = image_box.sum(axis = 1)
    rect[3] = image_box[np.argmin(s)]
    diff = np.diff(image_box, axis = 1)
    rect[2] = image_box[np.argmin(diff)]

    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(frame, M, (maxWidth, maxHeight))
    cv2.imshow('frame', warped)

while True:
    cap = cv2.VideoCapture("Untitled.png")
    ret, frame = cap.read()
    detect_card(frame)
    #cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
