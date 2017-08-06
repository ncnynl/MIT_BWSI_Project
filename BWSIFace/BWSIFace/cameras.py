from camera import save_camera_config
from camera import take_picture
import matplotlib.pyplot as plt

save_camera_config(port=1, exposure=0.5)


"""
Takes picture and displays it. Returns numpy RGB value image array
"""

def imgarray():
    img_array = take_picture()
    return img_array