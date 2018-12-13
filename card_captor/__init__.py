import sys
from optparse import OptionParser
from tempfile import mkdtemp

from PyQt5.QtWidgets import QApplication

from loop import launch_program
from gui import App

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
'''
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
'''
