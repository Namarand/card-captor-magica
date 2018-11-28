import cv2
import numpy as np
import os

def detect_card(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted([ (cv2.contourArea(i), i) for i in contours ], key=lambda a:a[0], reverse=True)
    _, card_contour = sorted_contours[1]
    rect = cv2.minAreaRect(card_contour)
    points = cv2.boxPoints(rect)
    points = np.int0(points)
    return card_contour

def cut_top_half(frame, card_contour):
    rect = create_rectangle(card_contour)
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
    wraped = cv2.warpPerspective(frame, M, (maxWidth, maxHeight))
    return wraped

def create_rectangle(card_contour):
    # create a min area rectangle from our contour
    rect = cv2.minAreaRect(card_contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # create empty initialized rectangle
    rect = np.zeros((4, 2), dtype = "float32")

    # get top left and bottom right points
    s = box.sum(axis = 1)
    rect[0] = box[np.argmin(s)]
    rect[2] = box[np.argmax(s)]

    # get top right and bottom left points
    diff = np.diff(box, axis = 1)
    rect[1] = box[np.argmin(diff)]
    rect[3] = box[np.argmax(diff)]

    rect[3][1] = (rect[0][1] + rect[3][1]) / 2
    rect[2][1] = (rect[1][1] + rect[2][1]) / 2

    return rect
