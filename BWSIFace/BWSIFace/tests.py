from database import Database
from detection import detect
from cameras import imgarray
from profile import Profile
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.mlab as mlab

import re
import skimage.io as io
import os 
import numpy as np

db = Database("profiles.pkl")

directory = "./images"
folders = [entry for entry in os.scandir(directory)]
distances = []
correct = []
wrong = []
for i, folder in enumerate(folders):
    print(folder.name, flush = True)
    foldPath = "./images/{}".format(folder.name)
    files = [e for e in os.scandir(foldPath)]
    for j, file in enumerate(files):
        print(file.name, flush = True)
        filePath = "{}/{}".format(foldPath, file.name)
        img = io.imread(filePath)
        if img.shape[2] == 4:
            print("Converting RGBA to RGB...", flush = True) #A is transparency
            img = img[:, :, 0:3]
        faces = detect(img, showImg = False)
        for i, face in enumerate(faces):
            descr, (l, r, t, b) = face
            if len(descr)>0:
            	for k, prof in enumerate(db.profiles):
            		curDes = descr[0]
            		profDes = prof.descr
            		dist = np.linalg.norm(profDes - curDes)
            		print(dist, flush = True)
            		distances.append(dist)
            		if prof.name == folder.name.lower():
            			correct.append(dist)
            		else:
            			wrong.append(dist)
    print("Loaded {}".format(folder.name), flush = True)

print("Correct upper bound: {}".format(np.max(correct)), flush = True)
print("Wrong lower bound: {}".format(np.min(wrong)), flush = True)
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.hist(correct)
ax1.set_title("Correct")
ax2.hist(wrong)
ax2.set_title("Wrong")
plt.show()