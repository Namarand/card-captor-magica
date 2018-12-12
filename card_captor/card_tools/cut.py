import cv2
import numpy as np
import os

def detect_card(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    negate = cv2.bitwise_not(gray)
    _, thresh = cv2.threshold(negate, 130, 255, cv2.THRESH_BINARY)
    hierarchy = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = _pruned_contours(hierarchy)
    return contours

def cut_top_half(frame, card_contour):
    rect = _create_rectangle(card_contour)
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

def _create_rectangle(card_contour):
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

    return _center_rectangle(rect)

def _center_rectangle(rect):
    # remove the bottom part
    rect[3][0] = (rect[0][0] * 8 + rect[3][0]) / 9
    rect[3][1] = (rect[0][1] * 8 + rect[3][1]) / 9
    rect[2][0] = (rect[1][0] * 8 + rect[2][0]) / 9
    rect[2][1] = (rect[1][1] * 8 + rect[2][1]) / 9

    # remove the top part
    rect[0][0] = (rect[0][0] * 2 + rect[3][0]) / 3
    rect[0][1] = (rect[0][1] * 2 + rect[3][1]) / 3
    rect[1][0] = (rect[1][0] * 2 + rect[2][0]) / 3
    rect[1][1] = (rect[1][1] * 2 + rect[2][1]) / 3

    # remove the left part
    rect[0][0] = (rect[0][0] * 13 + rect[1][0]) / 14
    rect[0][1] = (rect[0][1] * 13 + rect[1][1]) / 14
    rect[3][0] = (rect[3][0] * 13 + rect[2][0]) / 14
    rect[3][1] = (rect[3][1] * 13 + rect[2][1]) / 14

    # remove the right part
    rect[1][0] = (rect[0][0] * 2 + rect[1][0] * 8) / 10
    rect[1][1] = (rect[0][1] * 2 + rect[1][1] * 8) / 10
    rect[2][0] = (rect[3][0] * 2 + rect[2][0] * 8) / 10
    rect[2][1] = (rect[3][1] * 2 + rect[2][1] * 8) / 10

    return rect

def _pruned_contours(hierarchy):
    contours = []
    for index in range(0, len(hierarchy) - 1):
        if hierarchy[0][index][3] != -1:
            contours += [hierarchy[1][index]]
    return contours
