import numpy as np 
from PIL import Image
count = 1
newWidth = 1920
newHeight = 1080
folderDirectory = ""
def resize(input_im, width, height):
    resized = input_im.resize((width, height))
    return np.array(resized)
while (count <= 1000) :
    fileString = folderDirectory + "/" + str(count)
    pil_im = Image.open(fileString)
    resize(pil_im, newWidth, newHeight)
    count += 1