# to calibrate the points for each frame using OpenCV
import cv2;
import math;
import sys;
import numpy as np;
from pathlib import Path;

if len(sys.argv) < 2:
    # the file was not included in it, ERROR
    print("Error: No file was included. Make sure its an MP4 file");

visual = cv2.VideoCapture(sys.argv[1]);
visual_fpath = Path(sys.argv[1]);

if visual_fpath.is_file() and visual_fpath.suffix.lower() != ".mp4":
    print("Error: Wrong file type. Try again");
    exit();

if not visual.isOpened():
    print("Error: file could not be opened!");
    exit();


fps = visual.get(cv2.CAP_PROP_FPS); #total framerate for the file