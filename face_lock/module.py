from camera import save_camera_config
from camera import take_picture
import dlib_models
from dlib_models import load_dlib_models
import matplotlib.pyplot as plt
import matplotlib.patches as patches
    
load_dlib_models()

from dlib_models import models

import numpy as np

save_camera_config(port=0, exposure=0.5)

def imgarray():
    """
    Takes picture and displays it. Returns numpy RGB value image array
    Returns: The image array
    """
    img_array = take_picture()
    return img_array


def detect(img, showImg = True):
    """
    Detects faces in an image

    Parameters:
        img: np.array
        single: bool
            whether or not there is one person in the picture

    Returns: A list of tuples where inside the tuple, it contains an image vector and the position of the face
    """
    face_detect = models["face detect"]
    face_rec_model = models["face rec"]
    upscale = 2
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
    return descrps
