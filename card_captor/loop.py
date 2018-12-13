import cv2
import os
from tempfile import mkdtemp

from card_tools import detect_card, cut_top_half, identify_card
from trie import Trie
from output_handler import Output

def launch_program(video_stream, folder):
    cap = cv2.VideoCapture(video_stream)
    database = Trie()
    output = Output()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = process_frame(frame, database, folder, output)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    output.print_list()
    cap.release()
    cv2.destroyAllWindows()

def process_frame(frame, database, folder, output):
    card_contour = detect_card(frame)
    if card_contour is not None:
        cv2.drawContours(frame, [card_contour], -1, (0, 255, 0), 2)
        wraped = cut_top_half(frame, card_contour)
        filename = _save_image(wraped, folder)
        name = identify_card(filename, database)
        if name != 'X':
            output.add_card(name)
    return frame

def _save_image(frame, folder, name="image"):
    if not hasattr(_save_image, "x"):
         _save_image.x = 0
    filename = folder + '/' + name +  str(_save_image.x) + ".jpg"
    cv2.imwrite(filename, frame)
    _save_image.x += 1
    return filename

