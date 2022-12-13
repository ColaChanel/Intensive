from PIL import Image
import os, sys

path = "Drinks/Water/Good"
dirs = os.listdir(path)
newFolder = "New Drinks/Water/Good"

for item in dirs:
    #i = 1
    img = Image.open(os.path.join(path, item))
    img = img.resize((300, 300))
    img = img.convert("L")
    img.save(os.path.join(newFolder, item))
    #i+=1