from .database import Database
from .detection import detect
from .cameras import imgarray
from .profileClass import ProfileClass
from .lols import sym
import matplotlib.pyplot as plt
import matplotlib.patches as patches # for the rectangles we draw in our recognize function
import re
import skimage.io as io # for io.imread()
import sys # for arguments on command line
from pathlib import Path as _Path # because this is a module,
import cv2 # for cv2.imread
import os as _os # because package needs path
from .align_faces import ff # face aligner

_path = _Path(_os.path.dirname(_os.path.abspath(__file__))) # the path of this directory

def main():
    """
    Main function that calls all the other functions and classes when the user inputs commands via terminal
    This program is meant to recognize multiple faces but has some added features such as a symmetry test

    Refer to the conditional statements below to see which commands are acceptable.
    """
    db = Database("profiles.pkl") # loading database

    def loadimgs(directory, showImgs=False):
        folders = [entry for entry in os.scandir(directory)]
        for i, folder in enumerate(folders):
            print(folder.name, flush = True)
            foldPath = "./images/{}".format(folder.name)
            files = [e for e in os.scandir(foldPath)]
            for j, file in enumerate(files):
                print(file.name, flush = True)
                filePath = "{}/{}".format(foldPath, file.name)
                img = io.imread(filePath)
                if img.shape[2] == 4:
                    img = img[:, :, 0:3]
                faces = detect(img, showImg = showImgs)
                for i, face in enumerate(faces):
                    descr, (l, r, t, b) = face
                    if len(descr)>0:
                        db.addProfile(ProfileClass(folder.name.lower(), descr[0]))

            print("Loaded {}".format(folder.name), flush = True)

    if len(sys.argv)>1:
        command = sys.argv[1]
        if command == 'save':
            if sys.argv[2] and sys.argv[2] == 'camera':
                print("Please close image", flush = True)
                faces = detect(imgarray())
                camname = input("Who's in the photo? (separate names by comma space)\n").lower().split(", ")
                for i, face in enumerate(faces):
                    descr, (l, r, t, b) = face
                    profile = ProfileClass(camname[i], descr)
                    db.addProfile(profile)
        elif command == 'view':
            print(db)
        elif command == 'clear':
            db.clear()
        elif command == 'loadimgs':
            loadimgs("./images", showImgs = False)
        elif command == "remove":
            if(len(sys.argv)>=3):
                db.removeProfile(sys.argv[2].lower())
            else:
                name = input("Which person do you want to remove?\n")
                db.removeProfile(name)
        else:
            print("command not recognized")
    else:
        command = re.sub(r" ", "", input("What do you want to do?\n"))
        if command =='save':
            command2 = input("How would you like to save your photo? File or camera?\n").lower()
            if command2 == 'file':
                file = input("What file?\n")
                img = cv2.imread(str(_path) + "/" + file + ".jpg")
                img = img[:,:,::-1]

                faces = detect(img)
                for i, face in enumerate(faces):
                    fig, ax = plt.subplots()
                    plt.ion()
                    #ax.imshow(img)
                    plt.pause(0.001)
                    descr, (l, r, t, b) = face
                    rect = patches.Rectangle((l, t), r-l, b-t, fill=False)
                    ax.add_patch(rect)
                    plt.ioff()
                    plt.show()
                    #plt.pause(0.001)
                    name = input("Who is this?\n").lower()

                    profile = ProfileClass(name, descr)
                    db.addProfile(profile)
            elif command2 == 'camera':
                print("Please close image", flush = True)
                img = imgarray()
                #img = img[:,:,::-1]
                faces = detect(img)
                # camname = input("Who's in the photo? (separate names by comma space)\n").lower().split(", ")
                for i, face in enumerate(faces):
                    descr, (l, r, t, b) = face
                    name = input("Who is this?\n").lower()

                    profile = ProfileClass(name, descr)
                    db.addProfile(profile)
                    
                
        elif command == "loadimgs":
            directory = "./images"
            loadimgs(directory)
        elif command == 'recognize':
            img = imgarray()
            facesGot = detect(img, False)
            fig, ax = plt.subplots()
            ax.imshow(img)
            #ax = fig.add_axes([0, 0, 1, 1])
            for face in facesGot:
                descript, (l, r, t, b) = face
                bestMatch = db.computeMatches(descript, db.profiles)
                print(bestMatch)
                #display image
                #display rectangles
                #display text
                rect = patches.Rectangle((l, t), r-l, b-t, linewidth=2, edgecolor='r', facecolor='none', label = 'Label')
                plt.text(l,t, bestMatch, color='green', fontsize=20)
                ax.add_patch(rect)
            #ax.set_axis_off()
            plt.show()
        elif command == "clear":
            db.clear()

        elif command =='view':
            print(db)

        elif command == 'remove':
            name = input("Which person do you want to remove?\n")
            db.removeProfile(name)

        elif command == 'symtest' or command == 'symmetry' or command == 'sym_test' or command == 'sym':
            command2 = input("File or camera?\n").lower()
            if command2 == 'file' or command2 == 'f':
                command3 = input("Type file name and make sure it is in the same directory.?\n").lower()
                img = cv2.imread(str(_path) + "/" + command3 + ".jpg")
                img = img[:,:,::-1]
                print(img.shape)
            else:
                img = imgarray()
            img = ff(img)
            facesGot = detect(img, False)
            for face in facesGot:
                descript, (l, r, t, b) = face
                bestMatch = db.computeMatches(descript, db.profiles)
                print(bestMatch)
                img = img[t:b,l:r]
                sym(img, bestMatch)
        else:
            print("command is not recognized")
