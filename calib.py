# to calibrate the points for each frame using OpenCV
import cv2;
import math;
import sys;
import numpy as np;
from pathlib import Path;

CALIB = {
    "projection" : "equirectangular",
    "lat_max": 90.0,
    "lon_max": 180.0,
    "lat_min": -90.0,
    "lon_min":-180.0
}

if len(sys.argv) < 2:
    # the file was not included in it, ERROR
    print("Error: No file was included. Make sure its an MP4 file");
    exit();

visual = cv2.VideoCapture(sys.argv[1]);
visual_fpath = Path(sys.argv[1]);

if visual_fpath.is_file() and visual_fpath.suffix.lower() != ".mp4":
    print("Error: Wrong file type. Try again");
    exit();

if not visual.isOpened():
    print("Error: file could not be opened!");
    exit();


fps = visual.get(cv2.CAP_PROP_FPS); #total framerate for the file

def lines_to_coor(lat,lon):

    x_coor = int(((lon - CALIB["lon_min"])/ (CALIB["lon_max"] - CALIB["lon_min"]) * (visual.get(cv2.CAP_PROP_FRAME_WIDTH))));
    if CALIB["projection"] == "equirectangular":
        y_coor = int(((CALIB["lat_max"] - lat)/ (CALIB["lat_max"] - CALIB["lat_min"]) * (visual.get(cv2.CAP_PROP_FRAME_HEIGHT))));

    else:
        def defacto_ycoor(degree): # so the curves of lat/lon are accurately represented
            return math.log(math.tan(math.pi/4 + math.radians(degree)/2));

        y_coor= (defacto_ycoor(CALIB["lat_max"]) - defacto_ycoor(lat)) / ((defacto_ycoor(CALIB["lat_max"]) - defacto_ycoor(CALIB["lat_min"])) * visual.get(cv2.PROP_FRAME_HEIGHT));

    return x_coor,y_coor;


#TODO: generating the temporary folder of the different frames, maybe with the overlay?
tempfolder = Path(f"{visual_fpath.stem}_frames");
tempfolder.mkdir(exist_ok=True);

i=0;
frame_saves = 30;

while True:
    success, frame = visual.read()
    if not success:
        break;

    if i%frame_saves == 0:
        # TODO: overlay should be added, then saved to tempfolder, increment i
        # so possibly a helper function for the overlay to be added