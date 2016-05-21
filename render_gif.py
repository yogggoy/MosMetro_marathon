from PIL import Image, ImageFilter
from images2gif import writeGif

images=[]

for i in range(1,455):
    img = Image.open(r'frames\metro'+str(i)+'.png')
    images.append(img)

writeGif("images.gif",images,duration=0.3)
print('complete')