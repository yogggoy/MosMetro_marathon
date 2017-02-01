from PIL import Image, ImageFilter
from images2gif import writeGif
from progress_bar_cmd import bar

images=[]
frames = 455

print('appending...')
for i in range(1, frames):
    bar(i, frames-1)
    img = Image.open(r'frames\metro'+str(i)+'.png')
    images.append(img)


print('saving...')
writeGif("images.gif",images,duration=0.3)
print('complete')