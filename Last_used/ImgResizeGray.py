from tempfile import TemporaryDirectory
from PIL import Image
import os, sys
from matplotlib import image
from matplotlib.pyplot import show
import numpy as np
import pathlib
from pathlib import Path


dir_path = pathlib.Path.cwd()
dir_path = str(dir_path)
sMainPath = dir_path + '\\test1'
sNewPath = dir_path + '\\Training'
nameDrags = np.array(os.listdir(sMainPath))
print(nameDrags)

for i in nameDrags:
    FolderName = sMainPath + "\\" + str(i)
    nameInDrags = np.array(os.listdir(FolderName))
    for j in nameInDrags:
        path = FolderName + "\\" + j
        FolderBadOrGood = np.array(os.listdir(path))
        for BadOrGood in FolderBadOrGood:
            FilesInDrags = path + "\\" + BadOrGood
            files = np.array(os.listdir(FilesInDrags))
            for z in files:
                img = Image.open(FilesInDrags + "\\" + z)
                img = img.resize((300, 300))
                #img = img.convert("L")
                img.save(sNewPath + "\\" + i + "\\"  + j + "\\"  + BadOrGood + "\\"  + z)