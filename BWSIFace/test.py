from BWSIFace.database import Database
from whispers.algorithm import run, plot_graph, generate_adj
import networkx as nx
import numpy as np
import matplotlib.cm as cm
from BWSIFace.profileClass import ProfileClass

from BWSIFace.detection import detect
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.mlab as mlab

import re
import skimage.io as io
import os 
import numpy as np
from whispers.graph import Graph
db = Database("profiles.pkl")


directory = "./images"
folders = [entry for entry in os.scandir(directory)]
profiles = []
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
            if(i == 0):
                descr, (l, r, t, b) = face
                if(len(descr)>0):
                    prof = ProfileClass(folder.name, np.asarray(descr))
                    profiles.append(prof)

    print("Loaded {}".format(folder.name), flush = True)

g = Graph(profiles)
pres, acs = run(g.nodes)
fig, ax = plot_graph(tuple(g.nodes), *generate_adj(g.nodes))
plt.show()

fig1, (ax1, ax2) = plt.subplots(1,2)
print(pres)
print(acs)
ax1.plot(pres)
ax1.set_title("Precision")
ax2.plot(acs)
ax2.set_title("Recall")
plt.show()