import dlib_models
from dlib_models import load_dlib_models
import matplotlib.pyplot as plt
import matplotlib.patches as patches # for drawing the rectangles
    
load_dlib_models()
from dlib_models import models

import numpy as np

def detect(img, showImg = True):
    """
    Detects faces in an image

    Parameters:
        img: np.array of the image
        showImg: bool, we use a conditional to show the image if the boolean is true
    :return: descrps, a list of descriptors and lrtb coordinates for each face detected
    """
    face_detect = models["face detect"] # get the model from dlib
    face_rec_model = models["face rec"] # get the model from dlib
    upscale = 2 #increases image size to detect smaller faces
    detections = list(face_detect(img, upscale))
    descrps = []
    if showImg:
        fig, ax = plt.subplots()
        ax.imshow(img)
    for i, det in enumerate(detections):
        l, r, t, b = det.left(), det.right(), det.top(), det.bottom()  
        if showImg:
            ax.add_patch(
                patches.Rectangle(
                    (l, t),
                    r-l ,
                    b-t,
                    fill=False    
                )
            )
            ax.text(l, t, i, color = "red", fontsize = 24)
        shape_predictor = models["shape predict"]
        shape = shape_predictor(img, det)
        descriptor = np.array(face_rec_model.compute_face_descriptor(img, shape))
        descrps.append((descriptor, (l, r, t, b)))
    if showImg:
        plt.show()
    #print(descrps) ########################test######################
    return descrps


