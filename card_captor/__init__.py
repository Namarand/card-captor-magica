from optparse import OptionParser

import cv2
import os
from tempfile import mkdtemp

from card_tools import detect_card, cut_top_half, identify_card
from trie import Trie
from output_handler import Output

def launch_program(video_stream, folder, json_path):
    cap = cv2.VideoCapture(video_stream)
    database = Trie()
    output = Output()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        card_contour = detect_card(frame)
        if card_contour is not None:
            cv2.drawContours(frame, [card_contour], -1, (0, 255, 0), 2)
            wraped = cut_top_half(frame, card_contour)
            filename = save_image(wraped, folder)
            name = identify_card(filename, database, sets=[ "GNR" ])
            if name and name != 'X':
                output.add_card(name)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    output.print_list()
    cap.release()
    cv2.destroyAllWindows()

def save_image(frame, folder, name="image"):
    if not hasattr(save_image, "x"):
         save_image.x = 0
    filename = folder + '/' + name +  str(save_image.x) + ".jpg"
    cv2.imwrite(filename, frame)
    save_image.x += 1
    return filename

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="analyse FILE video file", metavar="FILE")
    parser.add_option("--save-title", dest="save_folder",
                      help="save temporary file in a FOLDER folder", metavar="FOLDER")
    parser.add_option("--load-json", dest="json_path",
                      help="load a new database from FILE", metavar="FILE")
    (options, args) = parser.parse_args()
    input_type = 0
    save_folder = options.save_folder
    if options.filename is not None:
        input_type = options.filename
    if save_folder is None:
        save_folder = mkdtemp()
    launch_program(input_type, save_folder, options.json_path)
