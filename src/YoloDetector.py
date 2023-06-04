import os
import numpy as np

import torch 

from PIL import Image
import cv2


class YoloDetector():
    """Bird detector class. Add docstring here"""
    def __init__(self):
        self.yolo = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    
    def detect(self, img):
        """img is a PIL image
        Returns Bool and tuple of boudning boxes - i.e. True, (xmin, ymin, w, h ) or False, None  """
        # Get yolo output as pandas dataframe w/: xmin, ymin, xmax, ymax, confidence, class, name
        yolo_output = self.yolo(img)
        yolo_output_pd = yolo_output.pandas().xyxy[0]
        # Check how many objects were detected and if any of them are birds
        N_obj = len(yolo_output_pd)
        yolo_names = yolo_output_pd["name"]
        if N_obj > 0:
            for n in range(N_obj):
                if yolo_names[n] == "bird":
                    print("BIRD DETECTED!") 
                    # Save this output
                    x1, y1 = (int(yolo_output_pd["xmin"][n]), int(yolo_output_pd["ymin"][n])) 
                    x2, y2 = (int(yolo_output_pd["xmax"][n]), int(yolo_output_pd["ymax"][n]))
                    w = x2 - x1
                    h = y2 - y1
                    return (True, (x1, y1, w, h))
        return (False, None) 
                    
