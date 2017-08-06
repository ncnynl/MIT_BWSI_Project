import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
from pathlib import Path as _Path
import os as _os

_path = _Path(_os.path.dirname(_os.path.abspath(__file__)))


def sym(im, bM):
    """
    displays the asymmetric properties on the left side of your face. does this by dividing the image in half and compare 2 by 2 groupings of RGB
    arrays (averages them) by seeing if any one of the R, G, or B values differs more than a certain threshold.
    :param im: the image array of RGB values
    :param bM: the best match that we got by the computeMatches function in the database class
    """
    ################################################################
    # printing image properties just for knowledge for the user to know
    ################################################################
    height = im.shape[0]
    length = im.shape[1]
    print("height is ", height)
    print("length is ", length)
    print("shape is ", im.shape)
    ################################################################
    # slices the image using broadcasting to make 2 by 2 img pixel on both halves of the image possible
    ################################################################
    if length%2 != 0.0:
        im = im[:, :-1, :]
        length = im.shape[1]
    if (length/2)%2 != 0.0:
        im = im[:, 1:-1, :]
        length = im.shape[1]
    if height%2 != 0.0:
        im = im[1:, :, :]
        height = im.shape[0]
    #################################################################
    # print the new img properties to see how the slicing has changed them
    ################################################################
    print("new height is ", height)
    print("new length is ", length)
    print("new shape is ", im.shape)


    ################################################################
    # appends colors to two lists of colors
    ################################################################
    r = 0
    c = 0
    colors1 = []
    im = im.astype("int")
    for r in range(0, height, 2):
        tempc = []
        for c in range(0, int(length/2), 2):
            bgr1 = im[r][c]
            bgr2 = im[r][c + 1]
            bgr3 = im[r+1][c]
            bgr4 = im[r+1][c+1]

            totBGR = bgr1+bgr2+bgr3+bgr4
            totBGR = totBGR/4

            tempc.append(totBGR)
        colors1.append(tempc)

    print("first r is ", r)
    print("first c is ", c)

    r = 0
    colors2 = []
    for r in range(0, height, 2):
        tempc = []
        for c in range(int(length/2), length, 2):

            bgr1 = im[r][c]
            bgr2 = im[r][c + 1]
            bgr3 = im[r+1][c]
            bgr4 = im[r+1][c+1]

            totBGR = bgr1+bgr2+bgr3+bgr4
            totBGR = totBGR / 4

            tempc.append(totBGR)
        colors2.append(tempc)
    ##################################################################
    # print the traverse variables to help determine any bugs
    # change the color lists into arrays to prepare for broadcasting
    # flip the colors2 array because it is originally a mirror of the left side
    # so that we can to compare the corresponding elements of the two color array using the same index
    ##################################################################
    print("second r is ", r)
    print("second c is ", c)

    print("length of colors1 is", len(colors1))
    print("length of colors2 is ", len(colors2))

    colors1 = np.array(colors1)
    colors2 = np.array(colors2)

    colors2 = np.fliplr(colors2)
    print(colors1.shape)
    print(colors2.shape)
    ##################################################################
    # compare the two colors arrays and add the r,c coordinates to a list
    # if their RGB values differ by a certain threshold
    ##################################################################
    IO_diffs = []

    cheight = colors1.shape[0]
    clength = colors1.shape[1]

    for r in range(cheight):
        for c in range(clength):
            diffAbs = np.abs(colors1[r][c] - colors2[r][c])
            for v in diffAbs:
                if v > 40:
                    IO_diffs.append(np.array([r,c]))
                    break

    ##################################################################
    # plots the red rectangles on the left side of the face using the
    # r,c coordinates of from the list
    # Also plots the original sliced image with a half line to see if
    # the program is able to cut the image in half perfectly
    ##################################################################
    im = np.array(im, dtype=np.uint8)
    fig1,(ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(im)
    for i in IO_diffs:
        # Create a Rectangle patch
        row = i[0]
        col = i[1]
        rect = patches.Rectangle((col*2,row*2),2,2,linewidth=1,edgecolor='r',facecolor='none')

        # Add the patch to the Axes
        ax1.add_patch(rect)

    ax2.imshow(im)
    ax2.vlines(length/2, 0, height)
    plt.title(bM, loc='left', fontsize=45)



    plt.show()
