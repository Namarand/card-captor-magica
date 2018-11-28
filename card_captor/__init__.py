from optparse import OptionParser

import cv2
import os

def launch_program(video_stream):
    cap = cv2.VideoCapture(video_stream)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        #detect_card(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="analyse FILE video file", metavar="FILE")
    (options, args) = parser.parse_args()
    input_type = 0
    if options.filename is not None:
        input_type = options.filename
    launch_program(input_type)
