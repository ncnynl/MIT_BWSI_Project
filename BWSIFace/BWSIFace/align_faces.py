# USAGE
# python align_faces.py --shape-predictor shape_predictor_68_face_landmarks.dat --image images/example_01.jpg
# Author credit to Adrian at PyImageSearch
# import the necessary packages
from imutils.face_utils import FaceAligner
from imutils.face_utils import rect_to_bb
import argparse
import imutils
import dlib
import cv2
from pathlib import Path as _Path
import os as _os

_path = _Path(_os.path.dirname(_os.path.abspath(__file__)))

def ff(img):
    """
    :param img:
    :return: faceAligned[0] the aligned face version of the original input image
    """
    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor and the face aligner
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(str(_path) + "/shape_predictor_68_face_landmarks.dat") ########################
    fa = FaceAligner(predictor, desiredFaceWidth=256)

    # load the input image, resize it, and convert it to grayscale
    image = img ##########################################################
    image = imutils.resize(image, width=800)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # show the original input image and detect faces in the grayscale
    # image
    #cv2.imshow("Input", image)
    rects = detector(gray, 2)

    lst = []
    # loop over the face detections
    for rect in rects:
        # extract the ROI of the *original* face, then align the face
        # using facial landmarks
        (x, y, w, h) = rect_to_bb(rect)
        faceOrig = imutils.resize(image[y:y + h, x:x + w], width=256)
        faceAligned = fa.align(image, gray, rect)

        import uuid
        f = str(uuid.uuid4())
        cv2.imwrite("foo/" + f + ".png", faceAligned)

        # display the output images
        #cv2.imshow("Original", faceOrig)
        #cv2.imshow("Aligned", faceAligned)
        #cv2.waitKey(0)
        lst.append(faceAligned)

    return lst[0]

